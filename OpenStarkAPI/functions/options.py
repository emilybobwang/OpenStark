from functions.custom.config import encrypt, decrypt, customs_func
from modules.setting import SettingModule
from modules.project import ProjectModule
from modules.testing import TestingModule
from modules.option import OptionModule
from tornado.web import app_log as log
from tornado import gen
from munch import munchify
from settings import static_path, report_mail_cc
from Crypto.Hash import MD5
from datetime import datetime
from xml.etree import cElementTree as ET
from pyecharts.charts import Pie, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
import json
import re
import os
import time


# 获取配置类
class OptionsFunction(object):
    def __init__(self):
        self.setting = SettingModule()
        self.option = OptionModule()
        self.project = ProjectModule()

    # 通过名称获取系统配置值
    @gen.coroutine
    def get_option_by_name(self, name):
        option = yield self.option.get_option(name=name)
        if option:
            return option.value
        else:
            return ''

    # 通过类型获取系统配置值
    @gen.coroutine
    def get_option_by_type(self, o_type):
        options = yield self.option.get_options_list(o_type=o_type)
        config = dict()
        for op in options:
            config[op.name] = op.value
        return config

    # 获取加解密参数
    @gen.coroutine
    def get_crypt_info(self, pid, do='encrypt'):
        setting, total = yield self.setting.get_settings_list(pid=pid, s_type='crypt', limit=None)
        setting = setting[0] if len(setting) > 0 else None
        if setting:
            flag = False
            crypt = json.loads(setting.value)
            if do == 'encrypt':
                crypt = crypt['encrypt']
                for info in encrypt:
                    if info['name'] == crypt['name']:
                        crypt['mode'] = info['mode']
                        crypt['function'] = info['function']
                        flag = True
                        break
            elif do == 'decrypt':
                crypt = crypt['decrypt']
                for info in decrypt:
                    if info['name'] == crypt['name']:
                        crypt['mode'] = info['mode']
                        crypt['function'] = info['function']
                        flag = True
                        break
            if not flag:
                crypt = None
            return munchify(crypt)
        else:
            return None

    # 获取自定义参数配置
    @gen.coroutine
    def get_custom_param(self, pid, correlation={}):
        setting, total = yield self.setting.get_settings_list(pid=pid, s_type='param', limit=None)
        setting = setting[0] if len(setting) > 0 else None
        if setting:
            params_str = []
            params_data = []
            params_func = []
            for row in json.loads(setting.value):
                row = json.loads(row)
                if row['type'] == 'Function':
                    for func in customs_func:
                        if row['value'] == func['name']:
                            row['function'] = func['function']
                            break
                    params_func.append(row)
                elif row['type'] == 'Data':
                    params_data.append(row)
                else:
                    params_str.append(row)
            for key in correlation:
                if not isinstance(correlation[key], str):
                    correlation[key] = str(correlation[key])
            for param in params_str:
                for key in correlation:
                    if param['value'].find(key) != -1:
                        param['value'] = param['value'].replace(key, correlation[key])
            for param in params_data:
                for row in params_str:
                    if param['value'].find('{%s}' % row['name']) != -1:
                        param['value'] = param['value'].replace('{%s}' % row['name'], row['value'])
                for key in correlation:
                    if param['value'].find(key) != -1:
                        param['value'] = param['value'].replace(key, correlation[key])
                argv, do = yield self.parse_sql_argv(param['value'], pid=pid)
                if argv:
                    try:
                        test = TestingModule(**argv)
                        if do == 'SELECT':
                            result = yield test.get_one_result()
                            if result:
                                param['value'] = result[0]
                            else:
                                param['value'] = ''
                        else:
                            raise Exception('目前只支持SELECT方法', do)
                    except Exception as e:
                        log.warning(e)
                        param['value'] = ''
                else:
                    param['value'] = ''
            return params_str + params_data + params_func
        else:
            return []

    # 解析sql参数
    @gen.coroutine
    def parse_sql_argv(self, sql_params, pid=0):
        sql_params = sql_params.splitlines()
        do = ''
        sql_argv = dict()
        if len(sql_params) == 5:
            for line in sql_params:
                line = line.strip().split(sep='=', maxsplit=1)
                if len(line) != 2:
                    return dict(), do
                elif line[0].strip() not in ['mysql', 'user', 'password', 'database', 'sql']:
                    return dict(), do
                elif line[1].strip() == '':
                    return dict(), do
                elif line[0] == 'sql' and re.match(r'^SELECT\s+', line[1].strip().upper()) is not None:
                    do = 'SELECT'
                elif line[0] == 'sql' and re.match(r'^DELETE\s+', line[1].strip().upper()) is not None:
                    do = 'DELETE'
                elif line[0] == 'sql' and re.match(r'^UPDATE\s+', line[1].strip().upper()) is not None:
                    do = 'UPDATE'
                elif line[0] == 'sql' and re.match(r'^INSERT\s+', line[1].strip().upper()) is not None:
                    do = 'INSERT'
                if line[0].strip() in ['mysql']:
                    sql_argv['engine'] = line[0].strip()
                    line[1] = line[1].split(':', maxsplit=1)
                    sql_argv['host'] = line[1][0].strip()
                    ips, total = yield self.setting.get_settings_list(
                        pid=pid, s_type='host', name=sql_argv['host'], pj_status=1, status=1, limit=None)
                    if ips:
                        sql_argv['host'] = ips[0].value
                    sql_argv['port'] = line[1][1].strip() if len(line[1]) == 2 else 3306
                elif line[0].strip() == 'user':
                    sql_argv['user'] = line[1].strip()
                elif line[0].strip() == 'password':
                    sql_argv['password'] = line[1].strip()
                elif line[0].strip() == 'database':
                    sql_argv['database'] = line[1].strip()
                elif line[0].strip() == 'sql':
                    sql_argv['sql'] = line[1].strip()
        if len(sql_argv) == 7 and do in ['SELECT', 'DELETE', 'UPDATE', 'INSERT']:
            return sql_argv, do
        else:
            return dict(), do

    # 获取接口完整性检查配置
    @gen.coroutine
    def get_check_key(self, pid, url):
        setting, total = yield self.setting.get_settings_list(pid=pid, s_type='url', limit=None)
        check_key = ''
        if setting:
            for row in setting:
                row = json.loads(row.value)
                if row['url'] == url:
                    check_key = row['check_key']
                    break
        return check_key

    # 通过环境编号获取环境信息
    @gen.coroutine
    def get_env_info(self, eid, ip=None, mark=None):
        if not isinstance(eid, list) and not eid:
            return list()
        env_info, total = yield self.project.get_projects_list(name=eid, p_type='env')
        env_info_parse = list()
        for env in env_info:
            details, total = yield self.setting.get_settings_list(s_type='env', name=env.name)
            data = list()
            for detail in details:
                desc = json.loads(detail.value)
                if (ip is None or (ip and desc.get('ip').strip() == ip.strip())) and (
                    mark is None or (mark and desc.get('description').find(mark) != -1)
                ):
                    data.append(dict(title=desc.get('title'), type=desc.get('type'), description=desc.get('description'),
                                     ip=desc.get('ip').strip(), port=desc.get('port').strip(), host=desc.get('host').strip(),
                                     username=desc.get('user').strip(), password=desc.get('password').strip()))
            desc = json.loads(env.config)
            env_info_parse.append(munchify(dict(eid=env.name, title=desc.get('title'), type=desc.get('type'), details=data)))
        return env_info_parse

    # 获取Hosts信息
    @gen.coroutine
    def get_hosts_info(self, data):
        env_list, total = yield self.setting.get_settings_list(
            s_type='env', name=data.get('env'))
        data_hosts = list()
        hosts = list()
        for env in env_list:
            desc = json.loads(env.value)
            host = (desc.get('ip').strip(), desc.get('host').strip())
            if desc.get('host').strip() and desc.get('ip').strip() and host not in hosts:
                data_hosts.append('{}\t\t{}\t\t# {}'.format(
                    desc.get('ip').strip(), desc.get('host').strip(), desc.get('title').strip()))
                hosts.append(host)
        hosts_path = os.path.join(static_path, 'files', 'hosts', data.get('type'), data.get('exec'))
        if not os.path.isdir(hosts_path):
            os.makedirs(hosts_path)
        with open(os.path.join(hosts_path, 'hosts'), 'w', encoding='utf8') as fp:
            fp.write('\n'.join(data_hosts))
        return os.path.join(hosts_path, 'hosts')

    # 获取Mysql信息
    @gen.coroutine
    def get_mysql_jdbc(self, eid, data):
        env_info = yield self.get_env_info(eid)
        env_list = list()
        for env in env_info[0].details:
            if env.type == 'APPLICATION' and env.title.upper().find('MYSQL') != -1:
                username = 'jdbcusername={}\n'.format(env.username)
                password = 'jdbcpsword={}\n'.format(env.password)
                jdbcurl = 'jdbc:mysql://{}:{}/'.format(env.host, env.port)
                if jdbcurl.find('database2') != -1:
                    jdbcurl = 'jdbcurl3307={}\n'.format(jdbcurl)
                elif jdbcurl.find('database3') != -1:
                    jdbcurl = 'jdbcurl3308={}\n'.format(jdbcurl)
                else:
                    jdbcurl = 'jdbcurl={}\n'.format(jdbcurl)
                if username not in env_list: env_list.append(username)
                if password not in env_list: env_list.append(password)
                if jdbcurl not in env_list: env_list.append(jdbcurl)
        hosts_path = os.path.join(static_path, 'files', 'hosts', data.type, data.exec)
        if not os.path.isdir(hosts_path):
            os.makedirs(hosts_path)
        with open(os.path.join(hosts_path, 'user.properties'), 'w', encoding='utf8') as fp:
            fp.writelines(env_list)
        return os.path.join(hosts_path, 'user.properties')

    # 获取指定用例信息
    @gen.coroutine
    def get_cases_info(self, job, data):
        desc = json.loads(job.value)
        selected_cases = desc.get('selectedCases') or list()
        function_list = list()
        for case in selected_cases:
            func = case.get('function')
            func and function_list.append(func.strip())
        cases_path = os.path.join(static_path, 'files', 'testCase', data.type, data.exec)
        if not os.path.isdir(cases_path):
            os.makedirs(cases_path)
        with open(os.path.join(cases_path, 'be_run_cases.txt'), 'w', encoding='utf8') as fp:
            fp.write('\n'.join(function_list))
        return os.path.join(cases_path, 'be_run_cases.txt')

    @gen.coroutine
    def get_job_logs(self, job_type=None):
        jobs, total = yield self.setting.get_settings_list(s_type='jobA' if job_type == 'api' else 'jobG')
        path = os.path.join(static_path, 'files', 'apiTest' if job_type == 'api' else 'guiTest', 'logs')
        if not os.path.exists(path):
            os.makedirs(path)
        date_list = list()
        for f in os.listdir(path):
            file = f.split('_', 1)
            if len(file) == 2:
                date = str(file[1]).split('.', 1)[0]
                date not in date_list and date_list.append(date)
        old_reports, total = yield self.setting.get_settings_list(s_type='reportA' if job_type == 'api' else 'reportG')
        for job in jobs:
            for date in date_list:
                file_path = os.path.join(path, '{}_{}.jsons'.format(job.name, date))
                last_path = os.path.join(path, '{}_{}.last.jsons'.format(job.name, date))
                if os.path.isfile(file_path):
                    sid = None
                    description = ''
                    old_logs_md5 = None
                    old_report_md5 = None
                    for old in old_reports:
                        desc = json.loads(old.value)
                        if job.name == old.name and date == old.createTime.strftime('%Y-%m-%d'):
                            sid = old.id
                            description = desc.get('description')
                            old_logs_md5 = desc.get('logs_md5')
                            old_report_md5 = desc.get('report_md5')
                            break
                    try:
                        with open(file_path, 'rb') as fp:
                            logs_md5 = MD5.new(fp.read()).hexdigest()
                    except Exception as e:
                        log.error(e)
                    all_exist_urls = list()
                    if not os.path.isfile(last_path) or logs_md5 != old_logs_md5:
                        reports = dict()
                        try:
                            with open(file_path, 'rb') as fp:
                                lines = fp.readlines()
                                for line in lines:
                                    case = json.loads(line.decode('utf8'))
                                    test_details = case.get('test_details')
                                    if not isinstance(test_details, list):
                                        continue
                                    exist_urls = list()
                                    case['runCases'] = 0
                                    key = 0
                                    for detail in test_details:
                                        if not isinstance(detail, dict):
                                            continue
                                        key += 1
                                        detail['key'] = key
                                        url = (detail.get('url') or '').split('?', maxsplit=1)[0]
                                        if url not in all_exist_urls:
                                            all_exist_urls.append(url)
                                        if url not in exist_urls:
                                            case['runCases'] += 1
                                            exist_urls.append(url)
                                    case['test_details'] = test_details
                                    test_start_time = case.get('test_start_time') or '1980-01-01 00:00:00.000'
                                    test_end_time = case.get('test_end_time') or '1980-01-01 00:00:00.000'
                                    split_time = test_start_time.split('.', maxsplit=1)
                                    test_start_time = case['test_start_time'] = test_start_time if len(split_time) < 2 else '{}.{}'.format(split_time[0], split_time[1].zfill(3))
                                    split_time = test_end_time.split('.', maxsplit=1)
                                    test_end_time = case['test_end_time'] = test_end_time if len(split_time) < 2 else '{}.{}'.format(split_time[0], split_time[1].zfill(3))
                                    test_start_time = datetime.strptime(test_start_time, '%Y-%m-%d %H:%M:%S.%f')
                                    test_end_time = datetime.strptime(test_end_time, '%Y-%m-%d %H:%M:%S.%f')
                                    case['test_time'] = round((test_end_time - test_start_time).total_seconds() * 1000, 3) if job_type == 'api' else round((test_end_time - test_start_time).total_seconds(), 3)
                                    if case.get('case_id') not in reports.keys():
                                        case['runTimes'] = 1
                                        case['maxTestTime'] = case['test_time']
                                        case['minTestTime'] = case['test_time']
                                        case['TotalTestTime'] = case['test_time']
                                        case['avgTestTime'] = case['test_time']
                                        if (case.get('test_result') or '').lower() == 'pass':
                                            case['passTimes'] = 1
                                        else:
                                            case['passTimes'] = 0
                                        case['runPassRate'] = round(case.get('passTimes')/case.get('runTimes'), 4)
                                        reports[case.get('case_id')] = case
                                    else:
                                        reports[case.get('case_id')]['runTimes'] += 1
                                        if (case.get('test_result') or '').lower() == 'pass':
                                            reports[case.get('case_id')]['passTimes'] += 1
                                        if reports.get(case.get('case_id')).get('maxTestTime') < case.get('test_time'):
                                            reports[case.get('case_id')]['maxTestTime'] = case.get('test_time')
                                        if reports.get(case.get('case_id')).get('minTestTime') > case.get('test_time'):
                                            reports[case.get('case_id')]['minTestTime'] = case.get('test_time')
                                        reports[case.get('case_id')]['TotalTestTime'] +=  case.get('test_time')
                                        reports[case.get('case_id')]['avgTestTime'] = round(reports.get(case.get('case_id')).get('TotalTestTime') / reports.get(case.get('case_id')).get('runTimes'), 4)
                                        reports[case.get('case_id')]['runPassRate'] = round(reports.get(case.get('case_id')).get('passTimes')/reports.get(case.get('case_id')).get('runTimes'), 4)
                                        if (reports.get(case.get('case_id')).get('timestamp') or 0) < (
                                                case.get('timestamp') or 0):
                                            case['runTimes'] = reports[case.get('case_id')].get('runTimes')
                                            case['passTimes'] = reports[case.get('case_id')].get('passTimes')
                                            case['maxTestTime'] = reports[case.get('case_id')].get('maxTestTime')
                                            case['minTestTime'] = reports[case.get('case_id')].get('minTestTime')
                                            case['TotalTestTime'] = reports[case.get('case_id')].get('TotalTestTime')
                                            case['avgTestTime'] = reports[case.get('case_id')].get('avgTestTime')
                                            case['runPassRate'] = reports[case.get('case_id')].get('runPassRate')
                                            reports[case.get('case_id')] = case
                        except Exception as e:
                            log.error(e)
                        lines = list()
                        key = 0
                        for report in reports:
                            key += 1
                            report = reports.get(report)
                            report['key'] = key
                            lines.append('{}\n'.format(json.dumps(report, ensure_ascii=False)).encode('utf8'))
                        try:
                            with open(last_path, 'wb') as fp:
                                fp.writelines(lines)
                        except Exception as e:
                            log.error(e)
                    try:
                        with open(last_path, 'rb') as fp:
                            report_md5 = MD5.new(fp.read()).hexdigest()
                    except Exception as e:
                        log.error(e)
                    if report_md5 != old_report_md5:
                        report_info = dict(runCases=0, passCases=0, failCases=0, runTime=0,
                                           errorCases=0, startTime=None, endTime=None, urlCases=0)
                        try:
                            with open(last_path, 'rb') as fp:
                                reports = fp.readlines()
                                for report in reports:
                                    report = json.loads(report.decode('utf8'))
                                    report_info['runCases'] += 1
                                    report_info['urlCases'] = len(all_exist_urls)
                                    if report_info['startTime'] is None:
                                        report_info['startTime'] = report.get('test_start_time')
                                    elif report_info['startTime'] > (report.get('test_start_time') or '1980-01-01 00:00:00.000'):
                                        report_info['startTime'] = report.get('test_start_time')
                                    if report_info['endTime'] is None:
                                        report_info['endTime'] = report.get('test_end_time')
                                    elif report_info['endTime'] < (report.get('test_end_time') or '1980-01-01 00:00:00.000'):
                                        report_info['endTime'] = report.get('test_end_time')
                                    if (report.get('test_result') or '').lower() == 'pass':
                                        report_info['passCases'] += 1
                                    elif (report.get('test_result') or '').lower() == 'error':
                                        report_info['errorCases'] += 1
                                    else:
                                        report_info['failCases'] += 1
                        except Exception as e:
                            log.error(e)
                        desc = json.loads(job.value)
                        desc['startTime'] = report_info.get('startTime')
                        desc['endTime'] = report_info.get('endTime')
                        start_time = report_info.get('startTime') or '1980-01-01 00:00:00.000'
                        end_time = report_info.get('endTime') or '1980-01-01 00:00:00.000'
                        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
                        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
                        desc['time'] = round((end_time - start_time).total_seconds(), 3)
                        yield self.setting.edit_setting(sid=job.id, value=desc)
                        report_info['runTime'] = desc['time']
                        report_info['logs_md5'] = logs_md5
                        report_info['report_md5'] = report_md5
                        report_info['title'] = desc.get('title')
                        report_info['description'] = desc.get('description')
                        report_info['userId'] = desc.get('userId')
                        report_info['email'] = desc.get('email')
                        report_info['sendMail'] = desc.get('sendMail')
                        report_info['passRate'] = round(
                            float(report_info.get('passCases') or 0)/float(report_info.get('runCases') or 1), 4)
                        if sid:
                            report_info['description'] = description
                            yield self.setting.edit_setting(
                                sid=sid, value=report_info,
                                status=2 if report_info['passRate'] == 1 else 0 if report_info['passRate'] == 0 else 1)
                        else:
                            yield self.setting.add_setting(
                                s_type='reportA' if job_type == 'api' else 'reportG', pid=job.project_id, name=job.name, value=report_info,
                                status=2 if report_info['passRate'] == 1 else 0 if report_info['passRate'] == 0 else 1,
                            create_time='{} {}'.format(date, time.strftime('%H:%M:%S')))
                        yield self.render_chart_image(title='用例执行结果统计', series_name='状态', job_id=job.name, job_date=date, data=dict(
                            PASS=report_info['passCases'], FAIL=report_info['failCases'], ERROR=report_info['errorCases']))

    @gen.coroutine
    def get_jacoco_report(self, job_type, job_id, job_date):
        jacoco_report = os.path.join(static_path, 'files', 'jacoco', job_id, job_date, 'report.xml')
        if os.path.isfile(jacoco_report):
            doc_root = ET.parse(jacoco_report)
            root = doc_root.getroot()
            counter = dict(branch=0, line=0, method=0, classes=0)
            for child in root.getchildren():
                if child.tag != 'counter':
                    continue
                if child.get('type') == 'BRANCH':
                    counter['branch'] = round(int(child.get('covered') or 0) / (int(child.get('covered') or 0) + int(child.get('missed') or 1)), 4)
                elif child.get('type') == 'LINE':
                    counter['line'] = round(int(child.get('covered') or 0) / (int(child.get('covered') or 0) + int(child.get('missed') or 1)), 4)
                elif child.get('type') == 'METHOD':
                    counter['method'] = round(int(child.get('covered') or 0) / (int(child.get('covered') or 0) + int(child.get('missed') or 1)), 4)
                elif child.get('type') == 'CLASS':
                    counter['classes'] = round(int(child.get('covered') or 0) / (int(child.get('covered') or 0) + int(child.get('missed') or 1)), 4)
            report = yield self.setting.get_setting(s_type=job_type, name=job_id, create_time=job_date)
            if report:
                desc = json.loads(report.value)
                desc['line'] = counter['line']
                desc['branch'] = counter['branch']
                desc['method'] = counter['method']
                desc['classes'] = counter['classes']
                if not desc.get('runTime'):
                    desc['endTime'] = desc.get('endTime') or time.strftime('%Y-%m-%d %H:%M:%S')
                    start_time = datetime.strptime(desc['startTime'], '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.strptime(desc['endTime'], '%Y-%m-%d %H:%M:%S')
                    desc['runTime'] = round((end_time - start_time).total_seconds(), 3)
                yield self.setting.edit_setting(sid=report.id, value=desc)
                yield self.render_chart_image(title='JaCoCo测试覆盖率统计', series_name='覆盖率', job_id=job_id, job_date=job_date, data=dict(
                    LINE=round(desc.get('line', 0) * 100, 2), BRANCH=round(desc.get('branch', 0) * 100, 2), 
                    METHOD=round(desc.get('method', 0) * 100, 2), CLASS=round(desc.get('classes', 0) * 100, 2)), cate='bar')
            elif job_type == 'report':
                job = yield self.setting.get_setting(s_type='job', name=job_id)
                if job:
                    desc = json.loads(job.value)
                    report_info = dict(**counter)
                    report_info['title'] = desc.get('title')
                    report_info['description'] = desc.get('description')
                    report_info['startTime'] = desc.get('startTime')
                    report_info['endTime'] = desc.get('endTime')
                    report_info['runTime'] = desc.get('time')
                    report_info['userId'] = desc.get('userId')
                    yield self.setting.add_setting(
                        s_type=job_type, pid=job.project_id, name=job.name, value=report_info,
                    create_time='{} {}'.format(job_date, time.strftime('%H:%M:%S')))
            jacoco_report = os.path.join(static_path, 'files', 'jacoco', job_id, job_date, 'analysis')
            if not os.path.isdir(jacoco_report):
                os.makedirs(jacoco_report)
            for package in root.iter('package'):
                package_name = package.get('name', '').replace('/', '.')
                if package_name.find('$') >= 0:
                    continue
                self.project.add_project(name=package_name, p_type='package', config=dict(package=package_name))
                counter = dict(branch=dict(missed=0, covered=0), line=dict(missed=0, covered=0), method=dict(missed=0, covered=0), classes=dict(missed=0, covered=0), complexity=dict(missed=0, covered=0))
                for count in package.iterfind('counter'):
                    if count.get('type') == 'BRANCH':
                        counter['branch'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                    elif count.get('type') == 'LINE':
                        counter['line'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                    elif count.get('type') == 'METHOD':
                        counter['method'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                    elif count.get('type') == 'CLASS':
                        counter['classes'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                    elif count.get('type') == 'COMPLEXITY':
                        counter['complexity'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                with open(os.path.join(jacoco_report, '{}.json'.format(package_name)), 'w', encoding='utf8') as fp:
                    fp.write(json.dumps(counter))
                for ele in package.getchildren():
                    for cls in ele.iter('class'):
                        class_name = cls.get('name', '').replace('/', '.')
                        if class_name.find('$') >= 0:
                            continue
                        self.project.add_project(name=class_name, p_type='class', config=dict(package=package_name, classes=class_name[len(package_name)+1:]))
                        counter = dict(branch=dict(missed=0, covered=0), line=dict(missed=0, covered=0), method=dict(missed=0, covered=0), classes=dict(missed=0, covered=0), complexity=dict(missed=0, covered=0))
                        for count in cls.iterfind('counter'):
                            if count.get('type') == 'BRANCH':
                                counter['branch'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                            elif count.get('type') == 'LINE':
                                counter['line'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                            elif count.get('type') == 'METHOD':
                                counter['method'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                            elif count.get('type') == 'CLASS':
                                counter['classes'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                            elif count.get('type') == 'COMPLEXITY':
                                counter['complexity'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                        with open(os.path.join(jacoco_report, '{}.json'.format(class_name)), 'w', encoding='utf8') as fp:
                            fp.write(json.dumps(counter))
                        for elm in cls.getchildren():
                            for method in elm.iter('method'):
                                method_name = method.get('name', '')
                                if not re.match(r'^\w', method_name) or method_name.find('$') >= 0:
                                    continue
                                method_name = '{}.{}'.format(class_name, method_name)
                                self.project.add_project(name=method_name, p_type='method',
                                                               config=dict(package=package_name, classes=class_name[len(package_name)+1:], method=method_name[len(class_name)+1:]))
                                counter = dict(branch=dict(missed=0, covered=0), line=dict(missed=0, covered=0), method=dict(missed=0, covered=0), classes=dict(missed=0, covered=0), complexity=dict(missed=0, covered=0))
                                for count in method.iterfind('counter'):
                                    if count.get('type') == 'BRANCH':
                                        counter['branch'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                                    elif count.get('type') == 'LINE':
                                        counter['line'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                                    elif count.get('type') == 'METHOD':
                                        counter['method'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                                    elif count.get('type') == 'CLASS':
                                        counter['classes'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                                    elif count.get('type') == 'COMPLEXITY':
                                        counter['complexity'] = dict(missed=int(count.get('missed', 0)), covered=int(count.get('covered', 0)))
                                log.info('METHOD# {}: {}'.format(method_name, counter))
                                with open(os.path.join(jacoco_report, '{}.json'.format(method_name)), 'w', encoding='utf8') as fp:
                                    fp.write(json.dumps(counter))
            return True, report
        else:
            return False, None

    @gen.coroutine
    def render_chart_image(self, title, series_name, job_id, job_date, data, cate='pie'):
        chart_path = os.path.join(static_path, 'files', 'jacoco', job_id, job_date, 'charts')
        if not os.path.isdir(chart_path):
            os.makedirs(chart_path)
        if cate == 'pie':
            pie = (
                Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT)).add(series_name=series_name, data_pair=[(key, data[key]) for key in data])
                .set_global_opts(title_opts=opts.TitleOpts(title=title))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            )
            make_snapshot(snapshot, pie.render(os.path.join(chart_path, 'render_pie.html')), os.path.join(chart_path, 'case.png'), is_remove_html=True)
            return os.path.join(chart_path, 'case.png')
        elif cate == 'bar':
            bar = (
                Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT)).add_xaxis(list(data.keys())).add_yaxis(series_name, list(data.values()))
                .set_global_opts(title_opts=opts.TitleOpts(title=title))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{c} %"))
            )
            make_snapshot(snapshot, bar.render(os.path.join(chart_path, 'render_bar.html')), os.path.join(chart_path, 'jacoco.png'), is_remove_html=True)
            return os.path.join(chart_path, 'jacoco.png')
        return None

    @gen.coroutine
    def send_test_report(self, test_report):
        test_desc = json.loads(test_report.value)
        path = os.path.join(static_path, 'files', 'apiTest' if test_report.type == 'reportA' else 'guiTest', 'logs')
        last_path = os.path.join(path, '{}_{}.last.jsons'.format(test_report.name, test_report.createTime.strftime('%Y-%m-%d')))
        if not os.path.isfile(last_path):
            return None
        try:
            with open(last_path, 'rb') as fp:
                reports = fp.readlines()
        except Exception as e:
            log.error(e)
            return None
        data = list()
        no = 0
        for report in reports:
            no += 1
            desc = json.loads(report.decode('utf8'))
            data.append('''<tr {style}>
								<td>{no}</td>
								<td>{cid}</td>
								<td style="text-align:left;">{title}</td>
								<td>{avgRunTime}</td>
								<td>{result}</td>
							</tr>'''.format(**dict(no=no, title=desc.get('case_title'),  avgRunTime=desc.get('avgTestTime'),
                        cid=desc.get('case_id'), result=desc.get('test_result', '').upper(), 
                        style='' if desc.get('test_result', '').upper() == 'PASS' else 'style="background-color: rgb(130, 145, 68)"'))
                )
        html = '''<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<meta name="renderer" content="webkit">  
		<meta name="force-rendering" content="webkit">
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<title>小牛在线自动化测试报告</title>	 
		<style>
			body{
				background-color:#eff4fa;
				font:12px '微软雅黑',Arial,'宋体'
			}
			th{
				font:14px '微软雅黑',Arial,'宋体';
				font-weight:bold
			}
			a{
				color:#266298;
				text-decoration:none
			}
			table{
				border-collapse:collapse;
				border-spacing:0;
				table-layout:auto
			}
			td,th{
				padding:0;
				margin:0;
				border:0
			}
            .details td, .details th{
                border: 1px solid #ccc;
                text-align: center;
            }
		</style>
	</head>
	<body>
		<table width="100%%"> 
			<tr>
				<td bgcolor="#4068AE" style="background-color:#4068AE;color:#fff;font-size:16px;font-weight:bold;padding:12px 20px;">		
					%(jobName)s 测试报告				
				</td>
			</tr>	
			<tr>
				<td style="padding:12px 20px;font-size:14px;color:#000;line-height: 24px;">		
						<b>报告日期：</b>%(reportTime)s</br>
						<b>任务名称：</b>%(jobName)s</br>
						<b>所属组：</b>%(team)s</br>
						<b>所属项目：</b>%(project)s</br>
						<b>测试用例数：</b>%(totalCase)s</br>
						<b>测试耗时(分钟)：</b>%(time)s</br>
						<b>测试结果：<span style="color:rgb(139, 104, 13)">%(result)s</span></b></br>
                        <b>报告详情地址:</b> <a href="%(url)s/%(tesType)s/reports/detail/%(jobId)s/%(jobDate)s">%(url)s/%(tesType)s/reports/detail/%(jobId)s/%(jobDate)s</a></br>
                        <b>覆盖率报告地址:</b> <a href="%(url)s/%(tesType)s/reports/jacoco/%(jobId)s/%(jobDate)s">%(url)s/%(tesType)s/reports/jacoco/%(jobId)s/%(jobDate)s</a>
				</td>
			</tr>		
		</table>	
		<table> 		
			<tr>
				<td bgcolor="#4068AE" width="150" style="background-color:#4068AE;color:#fff;font-weight:bold;padding:3px 20px;font-size:14px;">	
					一、结果汇总
				</td>
			</tr>		
		</table>	
		<table> 
			<tr>
				<td style="padding: 12px 0 0 20px">
                    <img src="%(url)s/static/files/jacoco/%(jobId)s/%(jobDate)s/charts/case.png" width="900" />
                </td>
                <td style="padding: 12px 0 0 10px">
                    <img src="%(url)s/static/files/jacoco/%(jobId)s/%(jobDate)s/charts/jacoco.png" width="900" />
				</td>
			</tr>
		</table>	
        <table> 		
            <tr>
				<td bgcolor="#4068AE" width="150" style="background-color:#4068AE;color:#fff;font-size:14px;font-weight:bold;padding:3px 20px;">		
					二、结果明细
				</td>
			</tr>	
		</table>
        <br/>
        <table class="details" width="95%%" style="margin:0 20px;font-size:14px;color:#000; min-width: 1000px;">
            <tr>
                <th width='100'>#</th>
                <th width='200'>用例编号</th>
                <th>用例标题</th>
                <th width='150'>平均耗时 (%(timeType)s)</th>
                <th width='100'>结果</th>
            </tr>
            %(caseDetail)s
        </table>
	</body>
</html>''' % (dict(caseDetail='\n'.join(data), reportTime=test_report.createTime.strftime('%Y-%m-%d %H:%M:%S'), jobName=test_desc.get('title'), 
            team=json.loads(test_report.team).get('name'), project=test_report.project_name, url='http://172.20.20.160:8090',
            totalCase=test_desc.get('runCases'), time=round(test_desc.get('runTime', 0)/60, 3), 
            result='未通过' if test_desc.get('passRate') < 1 else '通过', jobId=test_report.name, jobDate=test_report.createTime.strftime('%Y-%m-%d'),
            timeType='毫秒' if test_report.type == 'reportA' else '秒', tesType='api' if test_report.type == 'reportA' else 'gui'))
        try:
            from functions.common import CommonFunction
            report_mail_to = []
            for mail in test_desc.get('email', []):
                if mail.strip():
                    report_mail_to.append(mail.strip())
            send_mail = test_desc.get('sendMail')
            if send_mail and report_mail_to: CommonFunction().send_email(subject='[自动化测试报告]{} 测试报告'.format(test_desc.get('title')), content=html, to=report_mail_to, cc=report_mail_cc)
        except Exception as e:
            log.error(e)
        save_path = os.path.join(static_path, 'files', 'jacoco', test_report.name, test_report.createTime.strftime('%Y-%m-%d'), 'charts', 'report.html')
        with open(save_path, 'w', encoding='utf8') as fp:
            fp.write(html)
        return save_path