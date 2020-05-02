from handlers.common import BaseHandler, authenticated_async
from tornado import gen
from tornado.web import app_log as log
from handlers.common import AddLogs
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from datetime import datetime
from settings import jenkins_url, jenkins_user, jenkins_password, db_host, db_name, db_name_other, db_user, db_password, jenkins_jacoco, jenkins_docker
from modules.testing import TestingModule
import jenkins
import json
import os
import time
import base64
import uuid
import shutil


"""
GUI测试相关接口
"""


# GUI自动化测试相关
class GUITestHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op=None, do=None):
        AddLogs().add_logs(ip=self.request.remote_ip)
        if op == 'testCase':
            if do == 'list':
                page = int(self.get_argument('page', 1))
                size = int(self.get_argument('size', 10))
                key_word = self.get_argument('keyWord', '').strip()
                pid = self.get_argument('pid', '').strip()
                tid = self.get_argument('tid', '').strip()
                status = self.get_argument('status', '').strip()
                test_type = self.get_argument('test_type', 'caseG')
                cases, total = yield self.setting.get_settings_list(
                    s_type=test_type, page=page, limit=size, pj_status=1, pid=pid or None,
                    team_id=tid or None, status=status or None,
                    order_by=['s.projectId', 's.sort DESC', 's.name', 's.id'], search=key_word or None)
                data = []
                no = 0
                for case in cases:
                    desc = json.loads(case.value) if case.value else dict(
                        description='', expected='', actual='', title='',
                        author='', executor='', function='', module='', userId=self.current_user.id)
                    no += 1
                    data.append(
                        dict(no=no + page * size - size, key=case.id, title=desc.get('title'), tid=case.team_id,
                             team=json.loads(case.team).get('name'), description=desc.get('description'),
                             pid=case.project_id, project=case.project_name, cid=case.name,
                             expected=desc.get('expected'), author=desc.get('author'), status=case.status,
                             executor=desc.get('executor'), function=desc.get('function'),
                             userId=desc.get('userId'), module=desc.get('module')))
                msg = dict(status='SUCCESS', message='', data=dict(data=data, page=page, size=size, total=total))
            else:
                msg = dict(status='FAIL', message='操作类型错误!', data='')
        elif op == 'jobs':
            if do == 'list':
                page = int(self.get_argument('page', 1))
                size = int(self.get_argument('size', 10))
                key_word = self.get_argument('keyWord', '').strip()
                pid = self.get_argument('pid', '').strip()
                tid = self.get_argument('tid', '').strip()
                status = self.get_argument('status', '').strip()
                test_type = self.get_argument('test_type', 'jobG')
                jobs, total = yield self.setting.get_settings_list(
                    s_type=test_type, page=page, limit=size, pj_status=1, pid=pid or None,
                    team_id=tid or None, status=status or None,
                    order_by=['s.sort DESC', 's.createTime DESC'], search=key_word or None)
                data = []
                no = 0
                for job in jobs:
                    desc = json.loads(job.value) if job.value else dict(
                        description='', cycle='once', startTime='', title='', url='', queueId='',
                        endTime='', time='', userId=self.current_user.id, jobName='', dayBuild='')
                    no += 1
                    data.append(
                        dict(no=no + page * size - size, key=job.id, title=desc.get('title'), tid=job.team_id,
                             team=json.loads(job.team).get('name'), description=desc.get('description'), dayBuild=desc.get('dayBuild'),
                             pid=job.project_id, project=job.project_name, jid=job.name, status=job.status, queueId=desc.get('queueId'), sendMail=desc.get('sendMail', False),
                             cycle=desc.get('cycle'), startTime=desc.get('startTime'), time=round(float(desc.get('time') or 0)/60, 3), docker=desc.get('docker') or list(),
                             planTime=job.createTime.strftime('%Y-%m-%d %H:%M:%S'), jobName=desc.get('jobName'), runApps=desc.get('runApps'), email=desc.get('email', []), 
                             endTime=desc.get('endTime'), userId=desc.get('userId'), url=desc.get('url'), selectedCases=desc.get('selectedCases') or list()))
                msg = dict(status='SUCCESS', message='', data=dict(data=data, page=page, size=size, total=total))
            else:
                msg = dict(status='FAIL', message='操作类型错误!', data='')
        elif op == 'reports':
            if do == 'list':
                page = int(self.get_argument('page', 1))
                size = int(self.get_argument('size', 10))
                key_word = self.get_argument('keyWord', '').strip()
                pid = self.get_argument('pid', '').strip()
                tid = self.get_argument('tid', '').strip()
                status = self.get_argument('status', '').strip()
                yield self.option_func.get_job_logs(job_type='gui')
                reports, total = yield self.setting.get_settings_list(
                    s_type='reportG', page=page, limit=size, pj_status=1, pid=pid or None,
                    team_id=tid or None, status=status or None,
                    order_by=['s.createTime DESC', 's.sort DESC'], search=key_word or None)
                data = []
                no = 0
                for report in reports:
                    desc = json.loads(report.value) if report.value else dict(
                        description='', runCases=0, passCases=0, title='', startTime='', endTime='', runTime='',
                        errorCases=0, failCases=0, passRate=0, userId=self.current_user.id)
                    no += 1
                    data.append(
                        dict(no=no + page * size - size, key=report.id, title=desc.get('title'), tid=report.team_id,
                             team=json.loads(report.team).get('name'), description=desc.get('description'),
                             pid=report.project_id, project=report.project_name, jid=report.name, status=report.status,
                             runCases=desc.get('runCases'), passCases=desc.get('passCases'),
                             runTime=round(float(desc.get('runTime') or 0)/60, 3), passRate=desc.get('passRate'),
                             failCases=desc.get('failCases'), userId=desc.get('userId'), endTime=desc.get('endTime'),
                             errorCases=desc.get('errorCases'), startTime=desc.get('startTime'),
                             date=report.createTime.strftime('%Y-%m-%d')))
                msg = dict(status='SUCCESS', message='', data=dict(data=data, page=page, size=size, total=total))
            else:
                msg = dict(status='FAIL', message='操作类型错误!', data='')
        elif op == 'detail':
            if do == 'list':
                page = int(self.get_argument('page', 1))
                size = int(self.get_argument('size', 10))
                key_word = self.get_argument('keyWord', '').strip()
                jid = self.get_argument('jid', '').strip()
                date = self.get_argument('date', '').strip()
                result = self.get_argument('result', '').strip()
                path = os.path.join(self.settings.get('static_path'), 'files', 'guiTest', 'logs')
                last_path = os.path.join(path, '{}_{}.last.jsons'.format(jid, date))
                if not os.path.isfile(last_path):
                    return self.write_json(dict(status='FAIL', message='日志文件不存在!',
                                                data=dict(data=[], page=page, size=size, total=0)))
                reports = list()
                try:
                    with open(last_path, 'rb') as fp:
                        reports = fp.readlines()
                except Exception as e:
                    log.error(e)
                data = list()
                user_id = None
                for report in reports:
                    desc = json.loads(report.decode('utf8'))
                    result = result and result.upper() or ''
                    if result:
                        filter_flag = result.find((desc.get('test_result') or '').upper()) >= 0
                    else:
                        filter_flag = True
                    if not filter_flag or (
                            (desc.get('test_description') or '').find(key_word) == -1 and
                            (desc.get('actual') or '').find(key_word) == -1 and
                            (desc.get('case_id') or '').find(key_word) == -1 and
                            (desc.get('case_title') or '').find(key_word) == -1
                    ):
                        continue
                    if user_id is None:
                        user = yield self.user.get_user_info(
                            base64.b64decode(base64.b16decode((desc.get('token') or '').encode('utf8'))).decode('utf8'))
                        user_id = user and user.id
                    data.append(
                        dict(title=desc.get('case_title'), runTime=desc.get('test_time'),
                             description=desc.get('test_description'), lastResult=(desc.get('test_result') or '').upper(),
                             actual=desc.get('actual'), userId=user_id, executor=desc.get('executor'),
                             startTime=desc.get('test_start_time'), endTime=desc.get('test_end_time'), key=desc.get('key'),
                             timestamp=desc.get('timestamp'), date=date, avgRunTime=desc.get('avgTestTime'),
                             maxRunTime=desc.get('maxTestTime'),  runPassRate=desc.get('runPassRate'),
                             minRunTime=desc.get('minTestTime'), cid=desc.get('case_id'),
                             runTimes=desc.get('runTimes'), passTimes=desc.get('passTimes'),
                             result=(desc.get('test_result') or '').upper()))
                total = len(data)
                data = sorted(data, key=lambda k: k['cid'])[page*size-size:size*page]
                no = 0
                for d in data:
                    no += 1
                    d['no'] = no + page * size - size
                msg = dict(status='SUCCESS', message='', data=dict(data=data, page=page, size=size, total=total))
            else:
                msg = dict(status='FAIL', message='操作类型错误!', data='')
        else:
            msg = dict(status='FAIL', message='操作类型错误!', data='')
        self.write_json(msg)

    @authenticated_async
    @gen.coroutine
    def post(self, op=None, do=None):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        data = yield self.get_request_body_to_json()
        if op == 'testCase':
            if do == 'edit':
                desc = dict(description=data.get('description'), expected=data.get('expected'), actual=data.get('actual'),
                            function=data.get('function'), title=data.get('title'),
                            executor=data.get('executor'), author=data.get('author') or self.current_user.realname,
                            module=data.get('module'), userId=data.get('userId') or self.current_user.id)
                if str(data.key).find('NEW_TEMP_KEY') != -1:
                    key, msg = yield self.setting.add_setting(s_type=data.get('test_type') or 'caseG', name=data.cid, value=desc,
                                                              status=data.status or 1, pid=data.pid)
                    if key:
                        ret_msg = dict(status='SUCCESS', message='新增成功!', data=dict(type=do, key=key))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
                else:
                    res, msg = yield self.setting.edit_setting(sid=data.key, pid=data.pid, name=data.cid,
                                                               value=desc, status=data.status or None)
                    if res:
                        ret_msg = dict(status='SUCCESS', message='编辑成功!', data=dict(type=do, key=data.key))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
            elif do == 'delete':
                case = yield self.setting.get_settings_by_id(sid=data.key)
                exist_url = list()
                for c in case:
                    urls = json.loads(c.value).get('urls') or list()
                    exist_url += urls
                yield self.setting.delete_setting(sid=exist_url or None)
                res, msg = yield self.setting.delete_setting(sid=data.key)
                if res:
                    ret_msg = dict(status='SUCCESS', message='删除成功!', data=dict(type=do))
                else:
                    ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
            elif do == 'template':
                filename = '测试用例模板_{}.xlsx'.format(time.strftime('%Y%m%dT%H%M%S'))
                case_file = yield self.__get_test_cases_file(filename, do, data)
                ret_msg = dict(status='SUCCESS', message='下载用例模板成功!', data=dict(type=do, url=case_file))
            elif do == 'export':
                filename = '测试用例_{}.xlsx'.format(time.strftime('%Y%m%dT%H%M%S'))
                case_file = yield self.__get_test_cases_file(filename, do, data)
                ret_msg = dict(status='SUCCESS', message='导出用例成功!', data=dict(type=do, url=case_file))
            else:
                ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        elif op == 'jobs':
            if do == 'edit':
                desc = dict(description=data.get('description'), time=data.get('time'), startTime=data.get('startTime'),
                            endTime=data.get('endTime'), title=data.get('title'), url=data.get('url'), selectedCases=data.get('selectedCases'),
                            jobName=data.get('jobName'), dayBuild=data.get('dayBuild'), queueId=data.get('queueId'), docker=data.get('docker') or list(),
                            cycle=data.get('cycle'), userId=data.get('userId') or self.current_user.id, runApps=data.get('runApps'), 
                            email=data.get('email', [self.current_user.email]), sendMail=data.get('sendMail', False))
                status = data.status
                if int(time.time()) < int(time.mktime(time.strptime(data.planTime, '%Y-%m-%d %H:%M:%S'))): status = 0
                if str(data.key).find('NEW_TEMP_KEY') != -1:
                    jid = str(uuid.uuid1())
                    key, msg = yield self.setting.add_setting(
                        s_type=data.get('test_type') or 'jobG', name=jid, value=desc, status=status,
                        pid=data.pid, create_time=data.planTime)
                    if key:
                        content = dict(group=dict(name=data.title), project=dict(name=data.project),
                                       comment=dict(name='功能测试' if data.get('test_type') == 'job' else 'GUI自动化测试'),
                                       template='新建了 @{comment} 任务 @{group}, 所属项目 @{project}')
                        self.msg.add_message(user_id=self.current_user.id, m_type='active', content=content)
                        ret_msg = dict(status='SUCCESS', message='新增成功!', data=dict(type=do, key=key, jid=jid))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
                else:
                    res, msg = yield self.setting.edit_setting(sid=data.key, pid=data.pid, create_time=data.planTime,
                                                               value=desc, status=status)
                    if res:
                        ret_msg = dict(status='SUCCESS', message='编辑成功!', data=dict(type=do, key=data.key, jid=data.jid))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
            elif do == 'delete':
                jobs = yield self.setting.get_settings_by_id(sid=data.key)
                res, msg = yield self.setting.delete_setting(sid=data.key)
                if res:
                    if not isinstance(data.key, list):
                        content = dict(group=dict(name=data.title), project=dict(name=data.project),
                                       comment=dict(name='功能测试' if data.get('test_type') == 'job' else 'GUI自动化测试'),
                                       template='删除了 @{comment} 任务 @{group}, 所属项目 @{project}')
                    else:
                        content = dict(group=dict(), project=dict(),
                                       comment=dict(name='功能测试' if data.get('test_type') == 'job' else 'GUI自动化测试'),
                                       template='批量删除了 @{comment} 任务')
                    self.msg.add_message(user_id=self.current_user.id, m_type='active', content=content)
                    ret_msg = dict(status='SUCCESS', message='删除成功!', data=dict(type=do))
                    path = os.path.join(self.settings.get('static_path'), 'files', 'guiTest', 'logs')
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    file_list = os.listdir(path)
                    for job in jobs:
                        yield self.setting.delete_settings_by_type(s_type='report' if data.get('test_type') == 'job' else 'reportG', name=job.name)
                        jacoco_report = os.path.join(self.settings.get('static_path'), 'files', 'jacoco', job.name)
                        if os.path.isdir(jacoco_report):
                            shutil.rmtree(jacoco_report)
                        for file in file_list:
                            if file.find(job.name) != -1:
                                file_path = os.path.join(path, file)
                                last_path = os.path.join(path, file)
                                if os.path.isfile(file_path):
                                    os.remove(file_path)
                                if os.path.isfile(last_path):
                                    os.remove(last_path)
                else:
                    ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
            else:
                ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        elif op == 'reports':
            if do == 'edit':
                report = yield self.setting.get_settings_by_id(sid=data.key)
                if report:
                    desc = json.loads(report[0].value)
                    desc['description'] = data.get('description')
                    res, msg = yield self.setting.edit_setting(sid=data.key, value=desc)
                    if res:
                        ret_msg = dict(status='SUCCESS', message='编辑成功!', data=dict(type=do))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
                else:
                    ret_msg = dict(status='FAIL', message='所要编辑的报告不存在!', data=dict(type=do))
            elif do == 'delete':
                res, msg = yield self.setting.delete_setting(sid=data.key)
                if res:
                    ret_msg = dict(status='SUCCESS', message='删除成功!', data=dict(type=do))
                    path = os.path.join(self.settings.get('static_path'), 'files', 'guiTest', 'logs')
                    if data.get('jsonFiles'):
                        json_files = [(file.jid, file.date) for file in data.jsonFiles]
                    else:
                        json_files = [(data.jid, data.date)]
                    for file in json_files:
                        file_path = os.path.join(path, '{}_{}.jsons'.format(file[0], file[1]))
                        last_path = os.path.join(path, '{}_{}.last.jsons'.format(file[0], file[1]))
                        jacoco_report = os.path.join(self.settings.get('static_path'), 'files', 'jacoco', file[0], file[1])
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        if os.path.isfile(last_path):
                            os.remove(last_path)
                        if os.path.isdir(jacoco_report):
                            shutil.rmtree(jacoco_report)
                else:
                    ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
            else:
                ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        elif op == 'detail':
            if do == 'edit':
                path = os.path.join(self.settings.get('static_path'), 'files', 'guiTest', 'logs')
                last_path = os.path.join(path, '{}_{}.last.jsons'.format(data.jid, data.date))
                if not os.path.isfile(last_path):
                    return self.write_json(dict(status='FAIL', message='日志文件不存在!',
                                                data=dict(type=do)))
                reports = list()
                edit_reports = list()
                try:
                    with open(last_path, 'rb') as fp:
                        reports = fp.readlines()
                except Exception as e:
                    log.error(e)
                if reports:
                    for report in reports:
                        desc = json.loads(report.decode('utf8'))
                        if desc.get('key') == data.key:
                            desc['test_description'] = data.description
                            edit_reports.append('{}\n'.format(json.dumps(desc, ensure_ascii=False)).encode('utf8'))
                        else:
                            edit_reports.append(report)
                    try:
                        with open(last_path, 'wb') as fp:
                            fp.writelines(edit_reports)
                        ret_msg = dict(status='SUCCESS', message='编辑成功!', data=dict(type=do))
                    except Exception as e:
                        log.error(e)
                        ret_msg = dict(status='FAIL', message=str(e), data=dict(type=do))
                else:
                    ret_msg = dict(status='FAIL', message='所要编辑的日志不存在!', data=dict(type=do))
            else:
                ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        else:
            ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        self.write_json(ret_msg)

    @gen.coroutine
    def __get_test_cases_file(self, filename, do, data):
        path = os.path.join(self.settings.get('static_path'), 'files', 'testCase')
        if not os.path.isdir(path):
            os.makedirs(path)
        case_file = os.path.join(path, filename)
        wb = Workbook()
        try:
            ws = wb.active
            ws.title = 'Sheet1'
            tab_head = ['序号', '用例编号', '所属组', '所属项目', '系统模块', '用例标题',
                        '用例描述', '预期结果', '状态', '作者', '执行者']
            ws.append(tab_head)
            tab_body = []
            if do == 'export':
                cases = yield self.setting.get_settings_by_id(data.sid, order_by=['s.projectId', 's.sort DESC', 's.name', 's.id'])
                for i in range(len(cases)):
                    desc = json.loads(cases[i].value)
                    rows = list()
                    rows.append(i+1)
                    rows.append(cases[i].name)
                    rows.append((json.loads(cases[i].team).get('name') or '').strip())
                    rows.append(cases[i].project_name)
                    rows.append((desc.get('module') or '').strip())
                    rows.append((desc.get('title') or '').strip())
                    rows.append((desc.get('description') or '').strip())
                    rows.append((desc.get('expected') or '').strip())
                    if data.get('test_type') == 'case':
                        rows.append('已转自动化' if cases[i].status == 2 else '手动执行' if cases[i].status == 1 else '已废弃')
                    else:
                        rows.append('已实现' if cases[i].status == 2 else '开发中' if cases[i].status == 1 else '已废弃')
                    rows.append((desc.get('author') or '').strip())
                    rows.append((desc.get('executor') or '').strip())
                    tab_body.append(rows)
                for row in tab_body:
                    ws.append(row)
            style = TableStyleInfo(name="TableStyleMedium13", showFirstColumn=False,
                                   showLastColumn=False, showRowStripes=True, showColumnStripes=False)
            tab = Table(displayName="测试用例", ref="A1:K{}".format(len(tab_body)+12), tableStyleInfo=style, dataCellStyle='center')
            ws.add_table(tab)
            if data.get('test_type') == 'case':
                dv_status = DataValidation(type="list", formula1='"已转自动化,手动执行,已废弃"', allow_blank=False)
            else:
                dv_status = DataValidation(type="list", formula1='"已实现,开发中,已废弃"', allow_blank=False)
            ws.add_data_validation(dv_status)
            dv_status.add('I2:I{}'.format(len(tab_body)+12))
            projects, total = yield self.project.get_projects_list(p_type='project', status=1)
            projects = [p.name for p in projects]
            if projects:
                dv_projects = DataValidation(
                    type='list', formula1='"{}"'.format(','.join(projects)), allow_blank=False)
                ws.add_data_validation(dv_projects)
                dv_projects.add('D2:D{}'.format(len(tab_body)+12))
            teams = yield self.option.get_options_list(o_type='teams', name='team')
            teams = [json.loads(t.value)['name'] for t in teams]
            if teams:
                dv_teams = DataValidation(
                    type='list', formula1='"{}"'.format(','.join(teams)), allow_blank=False)
                ws.add_data_validation(dv_teams)
                dv_teams.add('C2:C{}'.format(len(tab_body)+12))
            ws.column_dimensions['B'].width = ws.column_dimensions['C'].width = ws.column_dimensions['D'].width = ws.column_dimensions['E'].width = 15
            ws.column_dimensions['F'].width = ws.column_dimensions['G'].width = ws.column_dimensions['H'].width = 30
        except Exception as e:
            log.error(e)
        wb.save(case_file)
        wb.close()
        return self.static_url('files/testCase/{}'.format(filename))


# Jenkins接口调用
class JenkinsHandler(BaseHandler):
    @gen.coroutine
    def prepare(self):
        super(JenkinsHandler, self).prepare()
        self.jenkins_server = jenkins.Jenkins(url=jenkins_url, username=jenkins_user, password=jenkins_password, timeout=5)

    @authenticated_async
    @gen.coroutine
    def get(self, op=None):
        if op == 'jobs':
            mysql = TestingModule(engine='mysql', host=db_host, user=db_user, password=db_password,
                                  database=db_name, sql="SELECT s.value FROM t_settings s WHERE s.type='env' AND s.`value` LIKE '%Linux_APP%' AND s.`status`=1 GROUP BY s.`name`;")
            envs = yield mysql.get_all_result()
            envs = [json.loads(env.get('value')).get('ip') for env in envs]
            path = os.path.join(self.settings.get('static_path'), 'files', 'hosts')
            if not os.path.isdir(path):
                os.makedirs(path)
            with open(os.path.join(path, 'ENVS.txt'), 'w', encoding='utf8') as fp:
                fp.write('ENVS={}'.format(','.join([(env or '').strip() for env in sorted(envs)])))
            try:
                jobs = self.jenkins_server.get_all_jobs()
                data = []
                for job in jobs:
                    if (job.get('fullname') or 'INNER').startswith('INNER'):
                        continue
                    data.append(dict(key=str(uuid.uuid1()), id=job['name'], title=job['fullname'], description=job['color']))
                ret_msg = dict(status='SUCCESS', message='', data=data)
            except Exception as e:
                log.error(e)
                ret_msg = dict(status='FAIL', message=str(e), data='')
        elif op == 'apps':
            mysql = TestingModule(engine='mysql', host=db_host, user=db_user, password=db_password,
                                  database=db_name_other, sql="SELECT jr.deliver_match FROM jenkins_record jr WHERE jr.deliver_match LIKE 'app%' GROUP BY jr.deliver_match;")
            apps = yield mysql.get_all_result()
            apps = [app.get('deliver_match') for app in apps]
            path = os.path.join(self.settings.get('static_path'), 'files', 'hosts')
            if not os.path.isdir(path):
                os.makedirs(path)
            with open(os.path.join(path, 'PACKAGES.txt'), 'w', encoding='utf8') as fp:
                fp.write('PACKAGES={}'.format(','.join(sorted(apps))))
            ret_msg = dict(status='SUCCESS', message='',
                           data=[dict(key=str(uuid.uuid1()), id=app, title=app, description=app) for app in apps])
        elif op == 'version':
            apps = self.get_arguments('apps')
            data = dict()
            for app in apps:
                data[app] = [dict(key=str(uuid.uuid1()), id='allVersions', title='All Versions', description='统计全部')]
                version_file = os.path.join(self.settings.get('static_path'), 'diffAPP', '{}_version.txt'.format(app))
                if os.path.isfile(version_file):
                    with open(version_file, 'r', encoding='utf8') as fp:
                        versions = fp.readlines()
                    for version in versions:
                        version = version.strip().split(',', maxsplit=1)
                        if len(version) > 1:
                            data[app].append(dict(key=str(uuid.uuid1()), id=version[1], title=version[0], description=version[0]))
                if data[app]: data[app] = sorted(data[app], key=lambda k: k['title'])
            ret_msg = dict(status='SUCCESS', message='', data=data)
        elif op == 'jacoco':
            page = int(self.get_argument('page', 1))
            size = int(self.get_argument('size', 10))
            key_word = self.get_argument('keyWord', '')
            pid = self.get_argument('pid', '')
            tid = self.get_argument('tid', '')
            r_type = self.get_argument('type', 'test')
            reports, total = yield self.setting.get_settings_list(
                s_type='reportG' if r_type == 'gui' else 'reportA' if r_type == 'api' else 'report', page=page,
                limit=size, pj_status=1, pid=pid or None, team_id=tid or None, sort=1,
                order_by=['s.createTime DESC', 's.sort DESC'], search=key_word or None)
            data = []
            no = 0
            for report in reports:
                desc = json.loads(report.value) if report.value else dict(
                    description='', line=0, branch=0, title='', startTime='', endTime='', runTime='',
                    method=0, classes=0, userId=self.current_user.id)
                no += 1
                data.append(
                    dict(no=no + page * size - size, key=report.id, title=desc.get('title'), tid=report.team_id,
                         team=json.loads(report.team).get('name'), description=desc.get('description'),
                         pid=report.project_id, project=report.project_name, jid=report.name,
                         line=desc.get('line') or 0, branch=desc.get('branch') or 0, startTime=desc.get('startTime'),
                         runTime=round(float(desc.get('runTime') or 0) / 60, 3), method=desc.get('method') or 0,
                         classes=desc.get('classes') or 0, userId=desc.get('userId'), endTime=desc.get('endTime'),
                         date=report.createTime.strftime('%Y-%m-%d')))
            ret_msg = dict(status='SUCCESS', message='', data=dict(data=data, page=page, size=size, total=total))
        else:
            ret_msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(ret_msg)

    @authenticated_async
    @gen.coroutine
    def post(self, op=None):
        if op == 'jobs':
            data = yield self.get_request_body_to_json()
            if data.get('type') != 'test' and not data.exec:
                ret_msg = dict(status='FAIL', message='执行器不能为空!', data='')
            elif not data.env:
                ret_msg = dict(status='FAIL', message='测试环境不能为空!', data='')
            else:
                if data.get('type') != 'test':
                    yield self.option_func.get_hosts_info(data)
                    yield self.option_func.get_mysql_jdbc(eid=data.env, data=data)
                try:
                    job = yield self.setting.get_setting(name=data.jobId, s_type='jobG' if data.type == 'gui' else 'jobA' if data.type == 'api' else 'job')
                    env, total = yield self.project.get_projects_list(name=data.env, p_type='env')
                    if job and env:
                        queue_id = None
                        jacoco_id = None
                        if data.get('type') != 'test': yield self.option_func.get_cases_info(job, data)
                        desc = json.loads(job.value)
                        if not data.saveOnly:
                            if data.get('type') != 'test': queue_id = self.jenkins_server.build_job(data.exec, parameters=dict(JOB_ID=data.jobId))
                            apps = yield self.option_func.get_env_info(eid=[e.name for e in env])
                            if data.get('type') != 'test':
                                stop_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 3600 * 24))
                            else:
                                stop_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 3600 * 24 * 14))
                            parameters = [('ACTION', 'Monitoring'), ('STOPTIME', stop_time),
                                          ('CLEAN', 'Yes' if data.clean else 'No'), ('JOB_ID', data.jobId)]
                            for app in [a.get('details') for a in apps]:
                                for ap in app:
                                    if ap.get('title').lower().find('linux_app') != -1:
                                        parameters.append(('ENV', ap.get('ip')))
                            if len(parameters) > 4:
                                version_file = os.path.join(self.settings.get('static_path'), 'diffAPP', data.jobId)
                                if not os.path.isdir(version_file):
                                    os.makedirs(version_file)
                                version_file = os.path.join(version_file, 'jacoco_app_version.txt')
                                if os.path.isfile(version_file): os.remove(version_file)
                                version_apps = list()
                                for app in (data.get('runApps') or []):
                                    parameters.append(('APP', app))
                                    version_apps.append('{},{}\n'.format(app, data.get('checkVersion', dict()).get(app, 'earliest')))
                                if version_apps:
                                    with open(version_file, 'w', encoding='utf8') as fp:
                                        fp.writelines(version_apps)
                                jacoco_id = self.jenkins_server.build_job(jenkins_jacoco, parameters=parameters)
                                desc['startTime'] = time.strftime('%Y-%m-%d %H:%M:%S')
                                desc['endTime'] = ''
                                desc['time'] = ''
                                desc['buildEnv'] = data.env
                            content = dict(group=dict(name='GUI自动化测试' if data.type == 'gui' else 'API自动化测试' if data.type == 'api' else '功能测试'),
                                           project=dict(name='{}({})'.format(data.name, data.exec) if data.type != 'test' else '{}'.format(data.name), link=desc['url']),
                                           comment=dict(name=', '.join([json.loads(e.config).get('title') for e in env])),
                                           template='在测试环境 @{comment} 启动了 @{group} 任务 @{project}')
                            self.msg.add_message(user_id=self.current_user.id, m_type='active', content=content)
                        if data.get('type') != 'test':
                            desc['jobName'] = data.exec
                            desc['queueId'] = queue_id or ''
                        desc['jacocoId'] = jacoco_id or ''
                        desc['runApps'] = data.get('runApps')
                        if data.get('type') != 'test' and data.dayBuild: desc['dayBuild'] = data.env
                        if data.get('type') != 'test':
                            desc['url'] = self.jenkins_server.get_job_info(data.exec).get('url')
                        else:
                            desc['dayBuild'] = data.env
                            desc['url'] = self.jenkins_server.get_job_info(jenkins_jacoco).get('url')
                        desc['email'] = data.get('mailList')
                        desc['sendMail'] = data.get('sendMail')
                        yield self.setting.edit_setting(sid=job.id, value=desc, status=None if data.saveOnly else 2)
                        ret_msg = dict(status='SUCCESS', message='任务配置保存成功!' if data.saveOnly else '任务启动成功!', data='')
                    else:
                        ret_msg = dict(status='FAIL', message='任务或测试环境不存在!', data='')
                except Exception as e:
                    log.error(e)
                    ret_msg = dict(status='FAIL', message=str(e), data='')
        elif op == 'docker':
            data = yield self.get_request_body_to_json()
            if data:
                job = yield self.setting.get_setting(name=data.jobId, s_type=['job', 'jobG', 'jobA'])
                path = os.path.join(self.settings.get('static_path'), 'files', 'docker.txt')
                if job:
                    desc = json.loads(job.value)
                    docker = desc.get('docker') or list()
                    for dc in data.docker:
                        if dc.id not in [d['id'] for d in docker]:
                            docker.append(dict(id=dc.id, name=dc.name, url=dc.url, type='系统创建'))
                            with open(path, 'a', encoding='utf8') as fp:
                                fp.write('{}\t{}\t{}\t{}\n'.format(data.jobId, dc.id, 'system', time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time() + 3600 * 24))))
                    desc['docker'] = docker
                    res, msg = yield self.setting.edit_setting(sid=job.id, value=desc)
                    if res:
                        ret_msg = dict(status='SUCCESS', message='保存成功!', data='')
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data='')
                else:
                    ret_msg = dict(status='FAIL', message='任务不存在!', data='')
            else:
                ret_msg = dict(status='FAIL', message='请求数据不能为空!', data='')
        elif op == 'delete':
            data = yield self.get_request_body_to_json()
            if data:
                job = yield self.setting.get_setting(name=data.jobId, s_type=['job', 'jobG', 'jobA', 'env.auto'])
                path = os.path.join(self.settings.get('static_path'), 'files', 'docker.txt')
                if job:
                    if not data.get('type'):
                        self.jenkins_server.build_job(jenkins_docker, parameters=dict(DOCKER_ID=data.dockerId))
                    elif os.path.isfile(path):
                        with open(path, 'r', encoding='utf8') as fp:
                            lines = fp.readlines()
                        for line in lines:
                            if line.find('{}\t{}'.format(data.jobId, data.dockerId)) >= 0:
                                lines.remove(line)
                        with open(path, 'w', encoding='utf8') as fp:
                            fp.writelines(lines)
                    desc = json.loads(job.value)
                    if job.type == 'env.auto':
                        docker = desc.get('docker') or dict()
                        for u in docker.keys():
                            for d in docker[u]:
                                if d['id'] == data.dockerId:
                                    docker[u].remove(d)
                    else:
                        docker = desc.get('docker') or list()
                        for d in docker:
                            if d['id'] == data.dockerId:
                                docker.remove(d)
                    desc['docker'] = docker
                    res, msg = yield self.setting.edit_setting(sid=job.id, value=desc)
                    if res:
                        ret_msg = dict(status='SUCCESS', message='删除成功!', data='')
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data='')
                else:
                    ret_msg = dict(status='FAIL', message='任务不存在!', data='')
            else:
                ret_msg = dict(status='FAIL', message='请求数据不能为空!', data='')
        elif op == 'env':
            data = yield self.get_request_body_to_json()
            if data:
                env = yield self.project.get_project(name=data.envId, p_type='env')
                if env:
                    if not data.get('type'):
                        data['env'] = data.envId
                        data['type'] = 'auto'
                        data['exec'] = jenkins_docker
                        yield self.option_func.get_hosts_info(data)
                        self.jenkins_server.build_job(jenkins_docker, parameters=dict(ENV_ID=data.envId, ENV_TYPE=data.testType))
                        ret_msg = dict(status='SUCCESS', message='调试环境创建中, 此过程大约需要1~5分钟, 请稍后刷新列表...', data='')
                    else:
                        path = os.path.join(self.settings.get('static_path'), 'files', 'docker.txt')
                        custom = yield self.setting.get_setting(s_type='env.auto', pid=env.id, name=env.name)
                        uid = str(self.current_user.id)
                        if custom:
                            docker = json.loads(custom.value).get('docker')
                        else:
                            docker = {uid: list()}
                        for dc in data.docker:
                            docker[uid].append(dict(
                                id=dc.id, name=dc.name, url=dc.url, type='手动创建({})'.format(data.get('type'))))
                            with open(path, 'a', encoding='utf8') as fp:
                               fp.write('{}\t{}\t{}\t{}\n'.format(data.envId, dc.id, 'auto', time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time() + 3600 * 24))))
                        if custom:
                            desc = json.loads(custom.value)
                            desc['docker'] = docker
                            res, msg = yield self.setting.edit_setting(sid=custom.id, value=desc)
                        else:
                            desc = dict(title=json.loads(env.config).get('title'), docker=docker)
                            res, msg = yield self.setting.add_setting(s_type='env.auto', pid=env.id, name=data.envId, value=desc)
                        if res:
                            ret_msg = dict(status='SUCCESS', message='保存成功!', data='')
                        else:
                            ret_msg = dict(status='FAIL', message=msg, data='')
                else:
                    ret_msg = dict(status='FAIL', message='环境不存在!', data='')
            else:
                ret_msg = dict(status='FAIL', message='请求数据不能为空!', data='')
        elif op == 'jacoco':
            data = yield self.get_request_body_to_json()
            action = data.get('action')
            if action == 'delete':
                if data.type == 'test':
                    yield self.setting.delete_setting(sid=data.key)
                try:
                    if not isinstance(data.key, list):
                        jacoco_report = os.path.join(self.settings.get('static_path'), 'files', 'jacoco', data.jid, data.date)
                        if os.path.isdir(jacoco_report):
                            shutil.rmtree(jacoco_report)
                        yield self.setting.edit_setting(sid=data.key, sort=0)
                    else:
                        jacoco = yield self.setting.get_settings_by_id(sid=data.key)
                        for report in jacoco:
                            jacoco_report = os.path.join(self.settings.get('static_path'), 'files', 'jacoco', report.name, report.createTime.strftime('%Y-%m-%d'))
                            if os.path.isdir(jacoco_report):
                                shutil.rmtree(jacoco_report)
                            yield self.setting.edit_setting(sid=report.id, sort=0)
                    ret_msg = dict(status='SUCCESS', message='删除成功!', data='')
                except Exception as e:
                    log.warning(e)
                    ret_msg = dict(status='FAIL', message='删除失败!', data='')
            elif action == 'refresh':
                if data.type == 'gui':
                    res, report = yield self.option_func.get_jacoco_report(job_type='reportG', job_id=data.jid, job_date=data.date)
                elif data.type == 'api':
                    res, report = yield self.option_func.get_jacoco_report(job_type='reportA', job_id=data.jid, job_date=data.date)
                else:
                    res, report = yield self.option_func.get_jacoco_report(job_type='report', job_id=data.jid, job_date=data.date)
                if res:
                    ret_msg = dict(status='SUCCESS', message='刷新成功!', data='')
                else:
                    ret_msg = dict(status='FAIL', message='报告文件不存在, 刷新失败!', data='')
            else:
                job = yield self.setting.get_setting(name=data.jobId, s_type=['jobG', 'jobA', 'job'])
                if job and job.type == 'jobG':
                    yield self.option_func.get_job_logs(job_type='gui')
                    res, report = yield self.option_func.get_jacoco_report(job_type='reportG', job_id=data.jobId, job_date=data.date)
                    if report:
                        self.option_func.send_test_report(report)
                elif job and job.type == 'jobA':
                    yield self.option_func.get_job_logs(job_type='api')
                    res, report = yield self.option_func.get_jacoco_report(job_type='reportA', job_id=data.jobId, job_date=data.date)
                    if report:
                        self.option_func.send_test_report(report)
                else:
                    yield self.option_func.get_jacoco_report(job_type='report', job_id=data.jobId, job_date=data.date)
                ret_msg = dict(status='SUCCESS', message='', data='')
        elif op == 'stopJob':
            data = yield self.get_request_body_to_json()
            job = yield self.setting.get_setting(name=data.jobId, s_type=['jobG', 'jobA', 'job'])
            if job:
                desc = json.loads(job.value)
                jacoco_job = self.jenkins_server.get_job_info(jenkins_jacoco)
                last_completed_build_number = jacoco_job.get('lastCompletedBuild').get('number')
                last_build_number = jacoco_job.get('lastBuild').get('number')
                jacoco = self.jenkins_server.get_build_info(jenkins_jacoco, last_completed_build_number)
                if jacoco.get('queueId') > desc.get('jacocoId'):
                    last_completed_build_number -= (jacoco.get('queueId') - desc.get('jacocoId'))
                    if last_completed_build_number < 0:last_completed_build_number = 0
                for num in range(last_completed_build_number, last_build_number + 1):
                    try:
                        jacoco = self.jenkins_server.get_build_info(jenkins_jacoco, num)
                        if jacoco.get('queueId') != desc.get('jacocoId'):
                            continue
                        self.jenkins_server.stop_build(jenkins_jacoco, num)
                    except Exception as e:
                        log.error(e)
                        continue
                    apps = yield self.option_func.get_env_info(eid=desc.get('buildEnv') or desc.get('dayBuild'))
                    parameters = [('ACTION', 'Reporting'), ('HIS_BUILD_ID', num),
                                  ('CLEAN', 'Yes'), ('JOB_ID', job.name)]
                    for app in [a.get('details') for a in apps]:
                        for ap in app:
                            if ap.get('title').lower().find('linux_app') != -1:
                                parameters.append(('ENV', ap.get('ip')))
                    if len(parameters) > 4:
                        for app in (desc.get('runApps') or []):
                            parameters.append(('APP', app))
                        self.jenkins_server.build_job(jenkins_jacoco, parameters=parameters)
                desc['endTime'] = time.strftime('%Y-%m-%d %H:%M:%S')
                start_time = desc['startTime'] or '1980-01-01 00:00:00'
                end_time = desc['endTime'] or '1980-01-01 00:00:00'
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                desc['time'] = round((end_time - start_time).total_seconds(), 3)
                env, total = yield self.project.get_projects_list(name=desc.get('buildEnv') or desc.get('dayBuild'), p_type='env')
                desc['buildEnv'] = ''
                yield self.setting.edit_setting(sid=job.id, value=desc, status=3)
                content = dict(group=dict(name='功能测试'),
                               project=dict(name='{}'.format(data.name), link=desc['url']),
                               comment=dict(name=', '.join([json.loads(e.config).get('title') for e in env])),
                               template='在测试环境 @{comment} 停止了 @{group} 任务 @{project}')
                self.msg.add_message(user_id=self.current_user.id, m_type='active', content=content)
                ret_msg = dict(status='SUCCESS', message='任务已停止!', data='')
            else:
                ret_msg = dict(status='FAIL', message='任务不存在!', data='')
        else:
            ret_msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(ret_msg)
