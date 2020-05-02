from handlers.common import BaseHandler, authenticated_async
from tornado import gen
from tornado.web import app_log as log
from handlers.common import AddLogs
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from munch import munchify
from datetime import datetime
import json
import os
import time
import base64
import uuid
import shutil


"""
API测试相关接口
"""


# API自动化测试相关
class APITestHandler(BaseHandler):
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
                cases, total = yield self.setting.get_settings_list(
                    s_type='caseA', page=page, limit=size, pj_status=1, pid=pid or None,
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
                             executor=desc.get('executor'), function=desc.get('function'), urlCount=desc.get('urlCount'),
                             userId=desc.get('userId'), module=desc.get('module')))
                msg = dict(status='SUCCESS', message='', data=dict(data=data, page=page, size=size, total=total))
            elif do == 'detail':
                key_word = self.get_argument('keyWord', '').strip()
                pid = self.get_argument('pid', '').strip()
                cid = self.get_argument('cid', '').strip()
                case = yield self.setting.get_setting(s_type='caseA', pid=pid, name=cid)
                data = []
                if case:
                    urls = json.loads(case.value).get('urls')
                    details = yield self.setting.get_settings_by_id(sid=urls or '')
                    no = 0
                    for detail in details:
                        desc = json.loads(detail.value) if detail.value else dict(
                            url=detail.name, title='', method='', request_headers='',
                            request_body='', description='', userId=self.current_user.id)
                        if key_word and (case.get('name') or '').find(key_word) == -1 and (desc.get('title') or '').find(key_word) == -1 and (desc.get('description') or '').find(key_word) == -1:
                            continue
                        no += 1
                        data.append(
                            dict(no=no, key=detail.id, title=desc.get('title'), description=desc.get('description'),
                                 cid=case.name, url=desc.get('url'), method=desc.get('method'), userId=desc.get('userId'),
                                 request_headers=desc.get('request_headers'), request_body=desc.get('request_body')))
                msg = dict(status='SUCCESS', message='', data=dict(data=data))
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
                jobs, total = yield self.setting.get_settings_list(
                    s_type='jobA', page=page, limit=size, pj_status=1, pid=pid or None,
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
                yield self.option_func.get_job_logs(job_type='api')
                reports, total = yield self.setting.get_settings_list(
                    s_type='reportA', page=page, limit=size, pj_status=1, pid=pid or None,
                    team_id=tid or None, status=status or None,
                    order_by=['s.createTime DESC', 's.sort DESC'], search=key_word or None)
                data = []
                no = 0
                for report in reports:
                    desc = json.loads(report.value) if report.value else dict(
                        description='', runCases=0, passCases=0, title='', startTime='', endTime='', runTime='',
                        errorCases=0, failCases=0, passRate=0, urlCases=0, userId=self.current_user.id)
                    no += 1
                    data.append(
                        dict(no=no + page * size - size, key=report.id, title=desc.get('title'), tid=report.team_id,
                             team=json.loads(report.team).get('name'), description=desc.get('description'),
                             pid=report.project_id, project=report.project_name, jid=report.name, status=report.status,
                             runCases=desc.get('runCases'), passCases=desc.get('passCases'),
                             runTime=round(float(desc.get('runTime') or 0)/60, 3), passRate=desc.get('passRate'),
                             failCases=desc.get('failCases'), userId=desc.get('userId'), endTime=desc.get('endTime'),
                             errorCases=desc.get('errorCases'), startTime=desc.get('startTime'),
                             urlCases=desc.get('urlCases'), date=report.createTime.strftime('%Y-%m-%d')))
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
                path = os.path.join(self.settings.get('static_path'), 'files', 'apiTest', 'logs')
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
                            base64.b64decode(base64.b16decode(desc.get('token').encode('utf8'))).decode('utf8'))
                        user_id = user.id
                    data.append(
                        dict(title=desc.get('case_title'), runTime=desc.get('test_time'), cid=desc.get('case_id'),
                             description=desc.get('test_description'), lastResult=(desc.get('test_result') or '').upper(),
                             actual=desc.get('actual'), userId=user_id, executor=desc.get('executor'),
                             startTime=desc.get('test_start_time'), endTime=desc.get('test_end_time'),
                             timestamp=desc.get('timestamp'), date=date, avgRunTime=desc.get('avgTestTime'),
                             maxRunTime=desc.get('maxTestTime'), minRunTime=desc.get('minTestTime'),
                             runTimes=desc.get('runTimes'), passTimes=desc.get('passTimes'), key=desc.get('key'),
                             runPassRate=desc.get('runPassRate'), runCases=desc.get('runCases'),
                             result=(desc.get('test_result') or '').upper()))
                total = len(data)
                data = sorted(data, key=lambda k: k['cid'])[page*size-size:size*page]
                no = 0
                for d in data:
                    no += 1
                    d['no'] = no + page * size - size
                msg = dict(status='SUCCESS', message='', data=dict(data=data, page=page, size=size, total=total))
            elif do == 'case':
                page = int(self.get_argument('page', 1))
                size = int(self.get_argument('size', 10))
                key_word = self.get_argument('keyWord', '').strip()
                jid = self.get_argument('jid', '').strip()
                cid = self.get_argument('cid', '').strip()
                date = self.get_argument('date', '').strip()
                result = self.get_argument('result', '').strip()
                path = os.path.join(self.settings.get('static_path'), 'files', 'apiTest', 'logs')
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
                case_desc = dict()
                for report in reports:
                    desc = json.loads(report.decode('utf8'))
                    if (desc.get('case_id') or '').strip() == cid.strip():
                        case_desc = desc
                        break
                if case_desc and isinstance(case_desc.get('test_details'), list):
                    detail = case_desc.get('test_details')
                    for desc in detail:
                        if (result and result.upper().find((desc.get('test_result') or '').upper()) == -1) or (
                                (desc.get('description') or '').find(key_word) == -1 and
                                (case_desc.get('case_id') or '').find(key_word) == -1 and
                                (desc.get('title') or '').find(key_word) == -1
                        ):
                            continue
                        if user_id is None:
                            user = yield self.user.get_user_info(
                                base64.b64decode(base64.b16decode((case_desc.get('token') or '').encode('utf8'))).decode('utf8'))
                            user_id = user and user.id
                        start_time = desc.get('start_time') or '1980-01-01 00:00:00.000'
                        end_time = desc.get('end_time') or '1980-01-01 00:00:00.000'
                        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
                        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
                        data.append(
                            dict(title=desc.get('title'), runTime=round((end_time - start_time).total_seconds() * 1000, 3), cid=case_desc.get('case_id'),
                                 description=desc.get('description'), userId=user_id, url=desc.get('url'), status=desc.get('status'),
                                 startTime=desc.get('start_time'), endTime=desc.get('end_time'), method=desc.get('method'),
                                 timestamp=case_desc.get('timestamp'), date=date, request_headers=desc.get('request_headers'),
                                 request_body=desc.get('request_body'), response_headers=desc.get('response_headers'),
                                 response_body=desc.get('response_body'), key=desc.get('key')))
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
                            function=data.get('function'), title=data.get('title'), urls=list(), urlCount=0,
                            executor=data.get('executor'), author=data.get('author') or self.current_user.realname,
                            module=data.get('module'), userId=data.get('userId') or self.current_user.id)
                if str(data.key).find('NEW_TEMP_KEY') != -1:
                    key, msg = yield self.setting.add_setting(s_type='caseA', name=data.cid, value=desc,
                                                              status=data.status or 1, pid=data.pid)
                    if key:
                        ret_msg = dict(status='SUCCESS', message='新增成功!', data=dict(type=do, key=key))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
                else:
                    cases = yield self.setting.get_settings_by_id(sid=data.key)
                    for case in cases:
                        case_desc = json.loads(case.value)
                        desc['urls'] = case_desc.get('urls') or list()
                        desc['urlCount'] = case_desc.get('urlCount') or 0
                    res, msg = yield self.setting.edit_setting(sid=data.key, pid=data.pid, name=data.cid,
                                                               value=desc, status=data.status or None)
                    if res:
                        ret_msg = dict(status='SUCCESS', message='编辑成功!', data=dict(type=do, key=data.key))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
            elif do == 'editDetail':
                if not self.common_func.check_string(data.url, 'url') and not self.common_func.check_string(data.url, 'dubbo'):
                    return self.write_json(dict(status='FAIL', message='接口格式不对!', data=dict(type=do)))
                desc = dict(url=data.url, title=data.title, method=data.method, request_headers=data.request_headers,
                            request_body=data.request_body, description=data.description, userId=data.userId)
                if str(data.key).find('NEW_TEMP_KEY') != -1:
                    key, msg = yield self.setting.add_setting(s_type='suiteA', name=data.url.strip(), value=desc, pid=data.pid)
                    url = data.url.strip().split('?', 1)
                    if not (yield self.setting.get_setting(s_type='url', name=url[0])) and url[0]:
                        desc['url'] = url[0]
                        if len(url) > 1: desc['request_body'] += url[1]
                        yield self.setting.add_setting(s_type='url', name=url[0], value=desc, pid=data.pid)
                    if key:
                        case = yield self.setting.get_setting(s_type='caseA', pid=data.pid, name=data.cid)
                        if case:
                            desc = json.loads(case.value)
                            if isinstance(desc.get('urls'), list):
                                desc['urls'].append(key)
                            else:
                                desc['urls'] = [key]
                            urls, total = yield self.setting.get_settings_list(s_type='suiteA', name=data.url.strip(), pid=case.project_id)
                            exist_url = list()
                            for url in urls:
                                if url.name.split('?', 1)[0] not in exist_url:
                                    exist_url.append(url.name.split('?', 1)[0])
                            desc['urlCount'] = len(exist_url)
                            res, msg = yield self.setting.edit_setting(sid=case.id, value=desc)
                            if res:
                                ret_msg = dict(status='SUCCESS', message='新增接口成功!', data=dict(type=do, key=key))
                            else:
                                ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
                        else:
                            ret_msg = dict(status='FAIL', message='所编辑的用例不存在!', data=dict(type=do, key=key))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
                else:
                    res, msg = yield self.setting.edit_setting(sid=data.key, pid=data.pid, name=data.url, value=desc)
                    if res:
                        ret_msg = dict(status='SUCCESS', message='编辑接口成功!', data=dict(type=do, key=data.key))
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
            elif do == 'deleteDetail':
                case = yield self.setting.get_setting(s_type='caseA', pid=data.pid, name=data.cid)
                if case:
                    desc = json.loads(case.value)
                    if isinstance(desc.get('urls'), list):
                        if data.get('key') in desc.get('urls'):
                            desc['urls'].remove(data.get('key'))
                    yield self.setting.delete_setting(sid=data.key)
                    urls, total = yield self.setting.get_settings_list(s_type='suiteA', name=data.url.strip(), pid=case.project_id)
                    exist_url = list()
                    for url in urls:
                        if url.name.split('?', 1)[0] not in exist_url:
                            exist_url.append(url.name.split('?', 1)[0])
                    desc['urlCount'] = len(exist_url)
                    res, msg = yield self.setting.edit_setting(sid=case.id, value=desc)
                    if res:
                        ret_msg = dict(status='SUCCESS', message='删除接口成功!', data=dict(type=do))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data=dict(type=do))
                else:
                    ret_msg = dict(status='FAIL', message='所编辑的用例不存在!', data=dict(type=do))
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
                        s_type='jobA', name=jid, value=desc, status=status,
                        pid=data.pid, create_time=data.planTime)
                    if key:
                        content = dict(group=dict(name=data.title), project=dict(name=data.project),
                                       comment=dict(name='API自动化测试'),
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
                                       comment=dict(name='API自动化测试'),
                                       template='删除了 @{comment} 任务 @{group}, 所属项目 @{project}')
                    else:
                        content = dict(group=dict(), project=dict(),
                                       comment=dict(name='API自动化测试'),
                                       template='批量删除了 @{comment} 任务')
                    self.msg.add_message(user_id=self.current_user.id, m_type='active', content=content)
                    ret_msg = dict(status='SUCCESS', message='删除成功!', data=dict(type=do))
                    path = os.path.join(self.settings.get('static_path'), 'files', 'apiTest', 'logs')
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    file_list = os.listdir(path)
                    for job in jobs:
                        yield self.setting.delete_settings_by_type(s_type='reportA', name=job.name)
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
                    path = os.path.join(self.settings.get('static_path'), 'files', 'apiTest', 'logs')
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
                path = os.path.join(self.settings.get('static_path'), 'files', 'apiTest', 'logs')
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
            elif do == 'editDetail':
                path = os.path.join(self.settings.get('static_path'), 'files', 'apiTest', 'logs')
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
                            test_details = desc.get('test_details')
                            if not isinstance(test_details, list):
                                continue
                            for detail in test_details:
                                detail['description'] = data.description
                            desc['test_details'] = test_details
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


# 自动化测试开放接口
class TestAPIHandler(BaseHandler):
    @gen.coroutine
    def post(self, op=None, do=None):
        data = yield self.get_request_body_to_json()
        token = self.get_argument('token', '') or data.get('token') or ''
        test_type = self.get_argument('test_type', None) or data.get('test_type')
        if token.strip():
            user = dict()
            try:
                email = base64.b64decode(base64.b16decode(token.strip().encode('utf8'))).decode('utf8')
                user = yield self.user.get_user_info(email, status=2)
            except Exception as e:
                log.error(e)
            if not user:
                return self.write_json(dict(status='FAIL', message='Token不正确!', data=''))
        else:
            return self.write_json(dict(status='FAIL', message='Token不能为空!', data=''))
        if test_type not in ('gui', 'api'):
            return self.write_json(dict(status='FAIL', message='测试类型test_type参数不对, 请填写gui或api!', data=''))
        if op == 'testCase':
            project_id = self.get_argument('project_id', '') or data.get('project_id') or ''
            case_id = self.get_argument('case_id', '').strip() or data.get('case_id') or ''
            title = self.get_argument('title', '').strip() or data.get('title') or ''
            description = self.get_argument('description', '').strip() or data.get('description') or ''
            expected = self.get_argument('expected', '').strip() or data.get('expected') or ''
            author = self.get_argument('author', '').strip() or data.get('author') or ''
            executor = self.get_argument('executor', '').strip() or data.get('executor') or ''
            status = self.get_argument('status', '').strip() or data.get('status') or ''
            func = self.get_argument('function', '').strip() or data.get('function') or ''
            module = self.get_argument('module', '').strip() or data.get('module') or ''
            details = self.get_argument('details', list()) or data.get('details') or list()
            if do == 'list' and project_id.strip():
                if not project_id:
                    return self.write_json(dict(
                        status='FAIL', message='以下字段不能为空:project_id, 请检查后重试!', data=''))
                cases_list = list()
                cases, total = yield self.setting.get_settings_list(
                    s_type='caseA' if test_type == 'api' else 'caseG', pid=project_id.strip(),
                    limit=None, order_by=['s.projectId', 's.sort DESC', 's.name', 's.id'])
                for case in cases:
                    desc = json.loads(case.value) if case.value else dict(
                        description='', expected='', title='', author='', executor='', function='', module='')
                    status = '已实现' if case.status == 2 else '开发中' if case.status == 1 else '已废弃'
                    urls = desc.get('urls') or list()
                    details = list()
                    if isinstance(urls, list) and urls:
                        urls = yield self.setting.get_settings_by_id(sid=urls)
                        for url in urls:
                            details.append(json.loads(url.value))
                    cases_list.append(
                        dict(case_id=case.name, team=json.loads(case.team)['name'], project=case.project_name,
                             title=desc.get('title'), description=desc.get('description'),
                             status=status, author=desc.get('author'), details=details, expected=desc.get('expected'),
                             executor=desc.get('executor'), function=desc.get('function'), module=desc.get('module')))
                ret_msg = dict(status='SUCCESS', message='获取用例成功!', data=cases_list)
            elif do == 'update' and project_id:
                data = dict(project_id=project_id, case_id=case_id, title=title, description=description, expected=expected,
                            author=author, executor=executor, status=status, func=func, module=module, details=details, test_type=test_type)
                ret_msg = yield self.__edit_cases(data, user)
            else:
                ret_msg = dict(status='FAIL', message='请求参数不全!', data='')
        elif op == 'test':
            if not data:
                data = munchify(dict(job_id=self.get_argument('job_id', '').strip(),
                                     executor=self.get_argument('executor', '').strip(),
                                     case_title=self.get_argument('case_title', '').strip(),
                                     test_description=self.get_argument('test_description', '').strip(),
                                     case_id=self.get_argument('case_id', '').strip(),
                                     test_details=self.get_argument('test_details', list()),
                                     test_start_time=self.get_argument('test_start_time', ''),
                                     test_end_time=self.get_argument('test_end_time', ''),
                                     test_result=self.get_argument('test_result', ''),
                                     actual=self.get_argument('actual', ''),
                                     token=self.get_argument('token', '')))
            data['timestamp'] = time.time()
            if not data.get('job_id') or not data.get('case_id') or not data.get('case_title') or not data.get('test_start_time') or not data.get('test_end_time') or not data.get('test_result') or not data.get('actual'):
                return self.write_json(dict(
                    status='FAIL', message='以下字段不能为空:job_id、case_id、case_title、test_start_time、test_end_time、test_result、actual, 请检查后重试!', data=''))
            flag, data['test_details'] = self.common_func.convert_to_list_or_dict(data.get('test_details'))
            if test_type == 'api' and not flag:
                return self.write_json(dict(status='FAIL', message='test_details字段必须是个json数组!', data=''))
            if do == 'log':
                log_file_path = os.path.join(self.settings.get('static_path'), 'files',
                                             'apiTest' if test_type == 'api' else 'guiTest', 'logs')
                log_file_name = data.get('job_id') or ''
                job = yield self.setting.get_setting(s_type='jobA' if test_type == 'api' else 'jobG', name=log_file_name.strip())
                if log_file_name.strip() and job:
                    cast_data = dict(project_id=job.project_id, case_id=data.get('case_id'), title=data.get('case_title'),
                                description=data.get('test_description'), expected='', author=data.get('executor'),
                                executor=data.get('executor'), status='已实现', func='', module='',
                                details=data.get('test_details'), test_type=test_type)
                    log_file_name = '{}_{}.jsons'.format(log_file_name.strip(), time.strftime('%Y-%m-%d'))
                    data = '{}\n'.format(json.dumps(data, ensure_ascii=False))
                    log_file = yield self.__save_file(log_file_path, log_file_name, data)
                    if log_file:
                        log_file = self.static_url('files/{}/logs/{}'.format(
                            'apiTest' if test_type == 'api' else 'guiTest', log_file_name))
                        ret_msg = dict(status='SUCCESS', message='上报测试记录成功!', data=log_file)
                        yield self.__edit_cases(cast_data, user)
                    else:
                        ret_msg = dict(status='FAIL', message='保存测试记录失败!', data='')
                else:
                    ret_msg = dict(status='FAIL', message='job_id配置不正确, 请确认后重试!', data='')
            else:
                ret_msg = dict(status='FAIL', message='请求参数不全!', data='')
        else:
            ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        self.write_json(ret_msg)

    @gen.coroutine
    def __save_file(self, file_path, filename, data):
        try:
            if not os.path.isdir(file_path):
                os.makedirs(file_path)
            file_path = os.path.join(file_path, filename)
            with open(file_path, 'ab') as fp:
                if not isinstance(data, bytes):
                    data = data.encode('utf8')
                fp.write(data)
            return file_path
        except Exception as e:
            log.error(e)
            return None

    @gen.coroutine
    def __edit_cases(self, data, user):
        if not data.get('project_id') or not data.get('case_id') or not data.get('title'):
            return dict(status='FAIL', message='以下字段不能为空:project_id、case_id、title, 请检查后重试!', data='')
        flag, details = self.common_func.convert_to_list_or_dict(data.get('details'))
        if data.get('test_type') == 'api' and not flag:
            return dict(status='FAIL', message='details字段必须是个json数组!', data='')
        desc = dict(description=data.get('description'), expected=data.get('expected'), function=data.get('func'),
                    title=data.get('title'), author=data.get('author') or user.get('realname'), executor=data.get('executor'),
                    module=data.get('module'), userId=user.get('id'), urls=list())
        status = 2 if data.get('status') == '已实现' else 1 if data.get('status') == '开发中' else 0
        cases = list()
        if data.get('case_id'):
            cases, total = yield self.setting.get_settings_list(
                s_type='caseA' if data.get('test_type') == 'api' else 'caseG', name=data.get('case_id'),
                pid=data.get('project_id'), limit=None)
        if data.get('title') and (not data.get('case_id') or not cases):
            exist_url = list()
            for detail in details:
                if isinstance(detail, dict):
                    if detail.get('url'):
                        key, msg = yield self.setting.add_setting(s_type='suiteA', name=detail.get('url'), value=detail,
                                                                  pid=data.get('project_id'))
                        key and desc['urls'].append(key)
                    url = (detail.get('url') or '').split('?', maxsplit=1)
                    if url[0] not in exist_url:
                        exist_url.append(url[0])
                        if not (yield self.setting.get_setting(s_type='url', name=url[0])) and url[0]:
                            detail['url'] = url[0]
                            if len(url) > 1: detail['request_body'] += url[1]
                            yield self.setting.add_setting(s_type='url', name=url[0], value=detail,
                                                           pid=data.get('project_id'))
            desc['urlCount'] = len(exist_url)
            key, msg = yield self.setting.add_setting(s_type='caseA' if data.get('test_type') == 'api' else 'caseG',
                                                      name=data.get('case_id'), value=desc, status=status, pid=data.get('project_id'))
            if key:
                ret_msg = dict(status='SUCCESS', message='新增用例成功!', data='')
            else:
                ret_msg = dict(status='FAIL', message=msg, data='')
        elif data.get('title'):
            flag = False
            msg = '编辑用例成功!'
            for case in cases:
                case_desc = json.loads(case.value)
                desc['executor'] = data.get('executor') or case_desc.get('executor')
                desc['function'] = data.get('func') or case_desc.get('function')
                desc['module'] = data.get('module') or case_desc.get('module')
                yield self.setting.delete_setting(sid=case_desc.get('urls'))
                exist_url = list()
                for detail in details:
                    if isinstance(detail, dict):
                        if detail.get('url'):
                            key, msg = yield self.setting.add_setting(s_type='suiteA', name=detail.get('url'),
                                                                      value=detail, pid=data.get('project_id'))
                            key and desc['urls'].append(key)
                        url = (detail.get('url') or '').split('?', maxsplit=1)
                        if url[0] not in exist_url:
                            exist_url.append(url[0])
                            if not (yield self.setting.get_setting(s_type='url', name=url[0])) and url[0]:
                                detail['url'] = url[0]
                                if len(url) > 1: detail['request_body'] += url[1]
                                yield self.setting.add_setting(s_type='url', name=url[0],
                                                               value=detail, pid=data.get('project_id'))
                desc['urlCount'] = len(exist_url)
                flag, msg = yield self.setting.edit_setting(sid=case.id, pid=data.get('project_id'), name=data.get('case_id'),
                                                            value=desc, status=status)
            if flag:
                ret_msg = dict(status='SUCCESS', message='编辑用例成功!', data='')
            else:
                ret_msg = dict(status='FAIL', message=msg, data='')
        else:
            ret_msg = dict(status='FAIL', message='请求参数不全!', data='')
        return ret_msg