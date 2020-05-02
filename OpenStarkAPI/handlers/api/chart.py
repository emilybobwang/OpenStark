from handlers.common import BaseHandler, authenticated_async
from tornado import gen
from tornado.web import app_log as log
from munch import munchify
from handlers.common import AddLogs
from settings import static_path
import time
import json
import base64
import os


"""
统计相关接口
"""


# 测试工具数据统计报表
class ChartDataHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self):
        AddLogs().add_logs(ip=self.request.remote_ip)
        chart_type = self.get_arguments('type')
        start_time = self.get_argument('startTime', time.strftime('%Y-%m-%d'))
        end_time = self.get_argument('endTime', time.strftime('%Y-%m-%d'))
        pid = self.get_argument('pid', '')
        data_pv = []
        data_active = []
        data_pv_rank = []
        data_active_rank = []
        data_range = []
        tools_list = []
        ret_data = dict()
        if 'pv' in chart_type:
            data = yield self.statistics.statistics(s_type='pv', start_time=start_time, order_by=['p.id DESC'],
                                                    end_time=end_time, group_by=['p.id'], status=1)
            for d in data:
                data_pv.append(dict(x=d.projectName, y=d.count))
                data_pv_rank.append(dict(id=str(d.pid), title=d.projectName, total=d.count))
            ret_data['toolsPVRange'] = data_pv
            ret_data['toolsPVRanking'] = sorted(data_pv_rank, key=lambda k: k['total'], reverse=True)
        if 'active' in chart_type:
            data = yield self.statistics.statistics(s_type='active', start_time=start_time, order_by=['p.id DESC'],
                                                    end_time=end_time, group_by=['p.id'], status=1)
            for d in data:
                data_active.append(dict(x=d.projectName, y=d.count))
                data_active_rank.append(dict(id=str(d.pid), title=d.projectName, total=d.count))
            ret_data['toolsActiveRange'] = data_active
            ret_data['toolsActiveRanking'] = sorted(data_active_rank, key=lambda k: k['total'], reverse=True)
        if 'data' in chart_type:
            if not pid:
                tools, total = yield self.project.get_projects_list(p_type='tool', status=1)
                for tool in tools:
                    tools_list.append(dict(id=str(tool.id), name=tool.name))
                ret_data['toolsList'] = tools_list
                pid = len(tools_list) and tools_list[0]['id']
            data_p = yield self.statistics.statistics(project_id=pid, status=1, order_by=['s.createTime'],
                                                      s_type='pv', group_by=["DATE(s.createTime)"],
                                                      start_time=start_time, end_time=end_time)
            if data_p:
                data_a = yield self.statistics.statistics(
                    project_id=pid, status=1, order_by=['s.createTime'], start_time=start_time,
                    s_type='active', group_by=["DATE(s.createTime)"], end_time=end_time)
                for d in data_p:
                    y1 = d.count
                    y2 = 0
                    for a in data_a:
                        if d.createTime.strftime('%Y-%m-%d') == a.createTime.strftime('%Y-%m-%d'):
                            y2 = a.count
                            break
                    data_range.append(dict(x=time.mktime(d.createTime.timetuple())*1000, y1=y1, y2=y2))
            else:
                data_range.append(dict(x=time.time()*1000, y1=0, y2=0))
            ret_data['toolsRangeData'] = sorted(data_range, key=lambda x:x['y1'], reverse=True)
        msg = dict(status='SUCCESS', message='', data=ret_data)
        self.write_json(msg)

    @gen.coroutine
    def post(self):
        data = yield self.get_request_body_to_json()
        if data is None:
            tool_id = self.get_argument('toolId', 0)
            t_type = self.get_argument('type', 'pv')
            ip = self.get_argument('ip', '0.0.0.0')
            data = munchify(dict(toolId=tool_id, type=t_type, ip=ip))
        tool = yield self.project.get_project(pid=data.toolId)
        if tool and data.type in ['pv', 'active']:
            data['name'] = tool.name
            self.statistics.add_statistics(s_type=data.type, project_id=data.toolId,
                                                               name=data.ip, value=data)
            if data.type == 'active':
                self.statistics.add_statistics(s_type='pv', project_id=data.toolId, name=data.ip, value=data)
            result, msg = True, ''
        else:
            result = False
            msg = '请求IP: {} # toolId不正确或type类型错误'.format(self.request.remote_ip)
            log.warn(msg)
        self.write_json(dict(status='SUCCESS' if result else 'FAIL', message=msg, data=''))


# 性能测试统计
class PerformanceHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op=None):
        AddLogs().add_logs(ip=self.request.remote_ip)
        chart_type = self.get_argument('type', 'load')
        start_time = self.get_argument('startTime', time.strftime('%Y-%m-%d'))
        end_time = self.get_argument('endTime', time.strftime('%Y-%m-%d'))
        env = self.get_argument('env', None)
        load_env = list()
        load_names = dict()
        load_data = list()
        ret_data = dict()
        if env is None:
            env_list = yield self.statistics.statistics(s_type=chart_type, start_time=start_time, join='INNER',
                                                        end_time=end_time, group_by=['s.name'])
            for e in env_list:
                test_env = yield self.project.get_project(p_type='env', name=e.name)
                test_env = test_env and json.loads(test_env.config).get('title')
                load_env.append(dict(name=test_env or e.name, id=e.name))
            ret_data['loadEvn'] = load_env
            env = len(load_env) and load_env[0]['id']
        if op == 'api':
            page = int(self.get_argument('page', 1))
            size = int(self.get_argument('size', 10))
            kw = self.get_argument('kw', '').strip()
            data = list()
            api_list, total = yield self.statistics.get_statistics_list(
                s_type=chart_type, start_time=start_time, end_time=end_time, group_by=['s.name', 'p.name'],
                order_by=['s.name', 'p.name'], limit=size, page=page, name=env or None, search=kw or None)
            no = 0
            for api in api_list:
                no += 1
                desc = api.config and json.loads(api.config)
                test_env = yield self.project.get_project(p_type='env', name=env)
                test_env = test_env and json.loads(test_env.config).get('title')
                data.append(dict(key=no+page*size-size, id=api.projectId, env=test_env or api.name, name=api.projectName,
                                 showName=desc and desc['showName'], api=desc and desc['url'],
                                 description=desc and desc['desc'], userNum=desc and desc['userNum'],
                                 threshold=desc and desc['threshold']))
            return self.write_json(dict(status='SUCCESS', message='', data=dict(
                total=total, page=page, size=size, data=data)))
        if env:
            names = yield self.statistics.statistics(
                s_type=chart_type, start_time=start_time, join='INNER',
                end_time=end_time, group_by=['p.name'], name=env,
                fields=['p.name', 'p.config'])
            for i in range(len(names)):
                load_names['y{}'.format(i+1)] = names[i].name
            data = yield self.statistics.statistics(
                s_type=chart_type, start_time=start_time, end_time=end_time, name=env,
                group_by=['DATE(s.createTime)', 'p.name'], order_by=['s.createTime'],
                fields=['p.name', 's.createTime', 'SUM(s.value)/COUNT(s.id) count'])
            temp_time = ''
            for i in range(len(data)):
                x = data[i].createTime.strftime('%Y-%m-%d')
                if x > temp_time:
                    if temp_time:
                        load_data.append(chart)
                    temp_time = x
                    chart = dict(x=time.mktime(data[i].createTime.timetuple()) * 1000)
                if x == temp_time:
                    for key in load_names:
                        if load_names[key] == data[i].name:
                            chart[key] = round(data[i].count, 3)
                            break
                if i+1 == len(data):
                    load_data.append(chart)
            for n in names:
                for ln in load_names:
                    if load_names[ln] == n.name:
                        if n.config and json.loads(n.config)['showName']:
                            load_names[ln] = json.loads(n.config)['showName']
                            break
        if not load_data:
            load_data.append(dict(x=time.time() * 1000, y1=0, y2=0))
        ret_data['loadData'] = load_data
        ret_data['loadNames'] = load_names
        msg = dict(status='SUCCESS', message='', data=ret_data)
        self.write_json(msg)

    @gen.coroutine
    def post(self, op=None):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        data = yield self.get_request_body_to_json()
        if op == 'edit':
            config = dict(showName=data.showName, url=data.api, desc=data.description,
                          threshold=data.threshold, userNum=data.userNum)
            res, msg = yield self.project.edit_project(pid=data.id, config=config)
            if res:
                msg = dict(status='SUCCESS', message='编辑成功!', data='')
            else:
                msg = dict(status='FAIL', message=msg, data='')
            return self.write_json(msg)
        elif op == 'delete':
            res, msg = yield self.project.delete_project(pid=data.id)
            if res:
                self.statistics.delete_statistics(project_id=data.id)
                msg = dict(status='SUCCESS', message='删除成功!', data='')
            else:
                msg = dict(status='FAIL', message=msg, data='')
            return self.write_json(msg)
        if data is None:
            key = self.get_argument('key', '').strip()
            name = self.get_argument('name', '').strip()
            duration = self.get_argument('time', '').strip()
            ip = self.get_argument('ip', '').strip()
            url = self.get_argument('url', '').strip()
            description = self.get_argument('description', '').strip()
            user_num = self.get_argument('userNum', '150').strip()
            threshold = self.get_argument('threshold', '50').strip()
            token = self.get_argument('token', '').strip()
            data = munchify(dict(key=key, name=name, time=duration, ip=ip, url=url, token=token,
                                 description=description, userNum=user_num, threshold=threshold))
        msg = dict(status='FAIL', message='参数key、time、url、ip, token必填, 并且time字段需大于0!', data='')
        if data and data.key and data.time and float(data.time) > 0 and data.ip and data.url and data.token:
            user = dict()
            if data.token.strip():
                try:
                    email = base64.b64decode(base64.b16decode(data.token.strip().encode('utf8'))).decode('utf8')
                    user = yield self.user.get_user_info(email, status=2)
                except Exception as e:
                    log.error(e)
            if not user:
                return self.write_json(dict(status='FAIL', message='Token不正确!', data=''))
            tran = yield self.project.get_project(p_type='sLoad', name=data.key)
            if tran:
                tran_id = tran.id
            else:
                tran_id, msg = yield self.project.add_project(
                    p_type='sLoad', name=data.key, config=dict(userId=user.get('id'),
                        showName=data.name, url=data.url, desc=data.description, author=user.get('realname'),
                        threshold=data.threshold, userNum=data.userNum))
            if tran_id:
                env, total = yield self.setting.get_settings_list(s_type='env', search=data.ip)
                name = data.ip
                for e in env:
                    value = json.loads(e.value)
                    if value.get('ip').strip() == data.ip.strip():
                        name = value.name
                        break
                res, msg = yield self.statistics.add_statistics(
                    project_id=tran_id, name=name, value=float(data.time), s_type='load')
                if res:
                    msg = dict(status='SUCCESS', message=msg, data='')
                else:
                    msg = dict(status='FAIL', message=msg, data='')
            else:
                msg = dict(status='FAIL', message=msg, data='')
        self.write_json(msg)


# 自动化测试统计
class AutoTestHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op='gui', do='case'):
        AddLogs().add_logs(ip=self.request.remote_ip)
        start_time = self.get_argument('startTime', '1970-01-01')
        end_time = self.get_argument('endTime', '1970-01-01')
        key = self.get_argument('key', '')
        status = self.get_argument('status', None)
        if op == 'gui':
            if do == 'case':
                if status is not None:
                    sql = '''
                    SELECT p.teamId, IF(s.`status`=0, '已废弃', IF(s.`status`=1, '开发中', '已实现')) project, COUNT(s.id) num 
                    FROM t_settings s JOIN t_projects p ON p.id = s.projectId 
                    WHERE s.type = 'caseG' AND s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59' GROUP BY p.teamId, s.`status`;
                    '''.format(start_time, end_time)
                else:
                    sql = '''
                    SELECT p.`name` project, p.teamId, COUNT(s.id) num 
                    FROM t_settings s JOIN t_projects p ON p.id = s.projectId 
                    WHERE s.type = 'caseG' AND s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59' GROUP BY s.projectId, p.teamId;
                    '''.format(start_time, end_time)
                data = dict()
                count_list = yield self.statistics.custom_statistics(sql=sql)
                for count in count_list:
                    if count.teamId not in data.keys():
                        data[count.teamId] = [dict(x=count.project, y=count.num)]
                    else:
                        data[count.teamId].append(dict(x=count.project, y=count.num))
                if status is not None:
                    ret_data = dict(caseStatus=data)
                else:
                    ret_data = dict(guiCaseData=data)
                ret_msg = dict(status='SUCCESS', message='', data=ret_data)
            elif do == 'reports':
                ret_data = dict()
                if not key:
                    jobs, total = yield self.setting.get_settings_list(s_type='jobG')
                    jobs_dict = dict()
                    for job in jobs:
                        desc = json.loads(job.value)
                        jobs_dict[job.name] = desc.get('title')
                    sql = '''
                    SELECT s.`name`, s.`value`, s.`createTime`
                    FROM t_settings s 
                    WHERE s.type = 'reportG' AND s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59';
                    '''.format(start_time, end_time)
                    reports = yield self.statistics.custom_statistics(sql=sql)
                    report_list = list()
                    for report in reports:
                        if report.name in jobs_dict.keys() and report.name not in [k['id'] for k in report_list]:
                            report_list.append(dict(id=report.name, name=jobs_dict[report.name]))
                            key = key or report_list[0]['id']
                    ret_data['guiJobs'] = report_list
                else:
                    sql = '''
                    SELECT s.`name`, s.`value`, s.`createTime`
                    FROM t_settings s 
                    WHERE s.type = 'reportG' AND s.`name`='{}' AND s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59';
                    '''.format(key, start_time, end_time)
                    reports = yield self.statistics.custom_statistics(sql=sql)
                report_data = list()
                sql = '''
                SELECT s.projectId, p.`name` project, COUNT(s.id) num 
                FROM t_settings s JOIN t_projects p ON p.id = s.projectId 
                WHERE s.projectId = (SELECT t.projectId FROM t_settings t WHERE t.type = 'jobG' AND t.`name` = '{}') 
                AND s.type = 'caseG' AND s.`status` > 1 GROUP BY p.teamId, s.`status`;
                '''.format(key)
                project = yield self.statistics.custom_statistics(sql=sql)
                pid = project[0].get('num') if project else 1
                for report in reports:
                    desc = json.loads(report.value)
                    if report.name == key:
                        run_rate = round((desc.get('runCases') or 0) / (pid or 1) * 100, 2)
                        y1 = desc.get('runCases', 0)
                        y2 = desc.get('passCases', 0)
                        y3 = round(desc.get('passCases', 0)/desc.get('runCases', 1) * 100, 2)
                        y4 = 100 if run_rate > 100 else run_rate
                        if not y1 and not y2 and not y3 and not y4:
                            continue
                        report_data.append(dict(x=time.mktime(report.createTime.timetuple()) * 1000,
                                                y1=y1, y2=y2, y3=y3, y4=y4))
                if not report_data:
                    report_data.append(dict(x=time.time() * 1000, y1=0, y2=0, y3=0, y4=0))
                ret_data['guiReports'] = report_data
                report_data = list()
                for report in reports:
                    desc = json.loads(report.value)
                    if report.name == key:
                        y1 = round(desc.get('line', 0) * 100, 2)
                        y2 = round(desc.get('branch', 0) * 100, 2)
                        y3 = round(desc.get('method', 0) * 100, 2)
                        y4 = round(desc.get('classes', 0) * 100, 2)
                        if not y1 and not y2 and not y3 and not y4:
                            continue
                        report_data.append(dict(x=time.mktime(report.createTime.timetuple()) * 1000,
                                                y1=y1, y2=y2, y3=y3, y4=y4))
                if not report_data:
                    report_data.append(dict(x=time.time() * 1000, y1=0, y2=0, y3=0, y4=0))
                ret_data['guiJacoco'] = report_data
                ret_msg = dict(status='SUCCESS', message='', data=ret_data)
            else:
                ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        elif op == 'api':
            if do == 'case':
                if status is not None:
                    sql = '''
                    SELECT p.teamId, IF(s.`status`=0, '已废弃', IF(s.`status`=1, '开发中', '已实现')) project, COUNT(s.id) num 
                    FROM t_settings s JOIN t_projects p ON p.id = s.projectId 
                    WHERE s.type = 'caseA' AND s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59' GROUP BY p.teamId, s.`status`;
                    '''.format(start_time, end_time)
                else:
                    sql = '''
                    SELECT p.`id` pid, p.`name` project, p.teamId tid, count(tmp.url) apinum, ctmp.num casenum 
FROM (SELECT * FROM (SELECT s.projectId pid, SUBSTRING_INDEX(s.`name`, '?', 1) url FROM t_settings s WHERE s.type = 'suiteA' AND s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59') as utmp GROUP BY utmp.pid, utmp.url) as tmp 
RIGHT JOIN t_projects p ON p.id = tmp.pid JOIN (SELECT p.`id` pid, p.`name` project, p.teamId tid, count(s.name) num FROM t_settings s 
JOIN t_projects p ON p.id = s.projectId WHERE s.type = 'caseA' AND s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59'
GROUP BY p.teamId, p.id) ctmp ON ctmp.tid = p.teamId AND ctmp.pid = p.id GROUP BY p.teamId, p.id;
                    '''.format(start_time, end_time, start_time, end_time)
                data = dict()
                case_list = yield self.statistics.custom_statistics(sql=sql)
                if status is not None:
                    for count in case_list:
                        if count.teamId not in data.keys():
                            data[count.teamId] = [dict(x=count.project, y=count.num)]
                        else:
                            data[count.teamId].append(dict(x=count.project, y=count.num))
                    ret_data = dict(caseStatus=data)
                else:
                    data_list = dict()
                    for case in case_list:
                        if case.tid not in data_list.keys():
                            data_list[case.tid] = {case.pid: dict(
                                name=case.project, y=case.casenum, z=case.apinum)}
                        else:
                            if case.pid not in data_list[case.tid].keys():
                                data_list[case.tid][case.pid] = dict(
                                name=case.project, y=case.casenum, z=case.apinum)
                            else:
                                project = data_list[case.tid][case.pid]
                                data_list[case.tid][case.pid] = dict(
                                    name=case.project, y=project['y'] + case.casenum,
                                    z=project['z'] + case.apinum)
                    for tid in data_list:
                        t_data = list()
                        for pid in data_list[tid]:
                            t_data.append(dict(x=data_list[tid][pid]['name'],
                                               y=data_list[tid][pid]['y'],
                                               z=data_list[tid][pid]['z']))
                        data[tid] = t_data
                    ret_data = dict(apiCaseData=data)
                ret_msg = dict(status='SUCCESS', message='', data=ret_data)
            elif do == 'reports':
                ret_data = dict()
                if not key:
                    jobs, total = yield self.setting.get_settings_list(s_type='jobA')
                    jobs_dict = dict()
                    for job in jobs:
                        desc = json.loads(job.value)
                        jobs_dict[job.name] = desc.get('title')
                    sql = '''
                    SELECT s.`name`, s.`value`, s.`createTime`
                    FROM t_settings s 
                    WHERE s.type = 'reportA' AND s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59';
                    '''.format(start_time, end_time)
                    reports = yield self.statistics.custom_statistics(sql=sql)
                    report_list = list()
                    for report in reports:
                        if report.name in jobs_dict.keys() and report.name not in [k['id'] for k in report_list]:
                            report_list.append(dict(id=report.name, name=jobs_dict[report.name]))
                            key = key or report_list[0]['id']
                    ret_data['apiJobs'] = report_list
                else:
                    sql = '''
                    SELECT s.`name`, s.`value`, s.`createTime`
                    FROM t_settings s 
                    WHERE s.type = 'reportA' AND s.`name`='{}' AND s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59';
                    '''.format(key, start_time, end_time)
                    reports = yield self.statistics.custom_statistics(sql=sql)
                sql = '''
                    SELECT s.projectId, p.`name` project, COUNT(s.id) num 
                    FROM t_settings s JOIN t_projects p ON p.id = s.projectId 
                    WHERE s.projectId = (SELECT t.projectId FROM t_settings t WHERE t.type = 'jobA' AND t.`name` = '{}') 
                    AND s.type = 'caseA' AND s.`status` > 1 GROUP BY p.teamId, s.`status`;
                    '''.format(key)
                project = yield self.statistics.custom_statistics(sql=sql)
                pid = project[0].get('num') if project else 1
                report_data = list()
                for report in reports:
                    desc = json.loads(report.value)
                    if report.name == key:
                        run_rate = round((desc.get('runCases') or 0) / (pid or 1) * 100, 2)
                        y1 = desc.get('runCases', 0)
                        y2 = desc.get('passCases', 0)
                        y3 = round(desc.get('passCases', 0)/desc.get('runCases', 1) * 100, 2)
                        y4 = 100 if run_rate > 100 else run_rate
                        if not y1 and not y2 and not y3 and not y4:
                            continue
                        report_data.append(dict(x=time.mktime(report.createTime.timetuple()) * 1000,
                                                y1=y1, y2=y2, y3=y3, y4=y4))
                if not report_data:
                    report_data.append(dict(x=time.time() * 1000, y1=0, y2=0, y3=0, y4=0))
                ret_data['apiReports'] = report_data
                report_data = list()
                for report in reports:
                    desc = json.loads(report.value)
                    if report.name == key:
                        y1 = round(desc.get('line', 0) * 100, 2)
                        y2 = round(desc.get('branch', 0) * 100, 2)
                        y3 = round(desc.get('method', 0) * 100, 2)
                        y4 = round(desc.get('classes', 0) * 100, 2)
                        if not y1 and not y2 and not y3 and not y4:
                            continue
                        report_data.append(dict(x=time.mktime(report.createTime.timetuple()) * 1000,
                                                y1=y1, y2=y2, y3=y3, y4=y4))
                if not report_data:
                    report_data.append(dict(x=time.time() * 1000, y1=0, y2=0, y3=0, y4=0))
                ret_data['apiJacoco'] = report_data
                ret_msg = dict(status='SUCCESS', message='', data=ret_data)
            else:
                ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        elif op == 'runtime':
            if do == 'list':
                envs, total = yield self.setting.get_settings_list(
                    s_type='env.auto', order_by=['s.createTime DESC'])
                jobs, total = yield self.setting.get_settings_list(
                    s_type=['jobG', 'jobA'], order_by=['s.createTime DESC'], search='docker')
                data = []
                no = 0
                for env in envs:
                    desc = json.loads(env.value) if env.value else dict(title='', docker=dict())
                    for uid in (desc.get('docker') or dict()).keys():
                        for docker in desc.get('docker')[uid]:
                            no += 1
                            data.append(
                                dict(key=no, title=desc.get('title'), jid=env.name, id=docker.get('id'),
                                     name=docker.get('name'), userId=int(uid), url=docker.get('url'), type=docker.get('type')))
                for job in jobs:
                    desc = json.loads(job.value) if job.value else dict(
                        docker=list(), title='', userId=self.current_user.id)
                    for docker in (desc.get('docker') or list()):
                        no += 1
                        data.append(
                            dict(key=no, title=desc.get('title'), jid=job.name, id=docker.get('id'),
                                 name=docker.get('name'), userId=desc.get('userId'), url=docker.get('url'), type=docker.get('type')))
                ret_msg = dict(status='SUCCESS', message='', data=data)
            else:
                ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        else:
            ret_msg = dict(status='FAIL', message='操作类型错误!', data='')
        self.write_json(ret_msg)


# JaCoCo统计
class JacocoReports(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self):
        p_type = self.get_argument('type', ['package', 'class', 'method'])
        name = self.get_argument('name', None)
        kw = self.get_argument('kw', None)
        job_id = self.get_argument('jid', '')
        job_date = self.get_argument('date', '')
        jacoco_report = os.path.join(static_path, 'files', 'jacoco', job_id, job_date, 'analysis')
        if not os.path.isdir(jacoco_report):
            return self.write_json(dict(status='FAIL', message='统计数据未生成, 请返回刷新报告后再试!', data=''))
        jacoco_report = [file[:-5] for file in os.listdir(jacoco_report)]
        java_list, total = yield self.project.get_projects_list(
            p_type=p_type, name=name, search=kw, limit=10 if not name and kw else None, order_by=['p.type DESC', 'p.id'])
        data = list()
        if kw is not None:
            if name is not None:
                classes = list()
                method = list()
                for java in java_list:
                    if java.name not in jacoco_report:
                        continue
                    desc = json.loads(java.config)
                    if java.type == 'package' and (java.name not in [p['title'] for p in data]):
                        data.append(dict(title=java.name, key='package-{}'.format(java.name),
                                         package=desc.get('package'), classes=desc.get('classes')))
                    elif (java.type == 'class' or java.type == 'method') and (desc.get('package') not in [p['title'] for p in data]):
                        data.append(dict(title=desc.get('package'), key='package-{}'.format(desc.get('package')),
                                         package=desc.get('package'), classes=desc.get('classes')))
                    if java.type == 'class' or java.type == 'method':
                        sub_class = dict(title=desc.get('classes'), package=desc.get('package'), classes=desc.get('classes'))
                        if sub_class not in classes:
                            classes.append(sub_class)
                    if java.type == 'method':
                        sub_method = dict(title=desc.get('method'), package=desc.get('package'), classes=desc.get('classes'))
                        if sub_method not in method:
                            method.append(sub_method)
                for c in classes:
                    children = list()
                    for m in method:
                        if m['classes'] == c['title'] and m['package'] == c['package']:
                            children.append(dict(title=m['title'], key='method-{}.{}.{}'.format(m['package'], m['classes'], m['title']),
                                                 isLeaf=True, package=m['package'], classes=m['classes']))
                    if children: c['children'] = children
                for d in data:
                    children = list()
                    for c in classes:
                        if c['package'] == d['title']:
                            if c.get('children'):
                                children.append(dict(title=c['title'], key='class-{}.{}'.format(c['package'], c['title']),
                                                     children=c['children'], package=c['package'], classes=c['classes']))
                            else:
                                children.append(dict(title=c['title'], key='class-{}.{}'.format(c['package'], c['title']),
                                                     package=c['package'], classes=c['classes']))
                    if children: d['children'] = children
            else:
                for java in java_list:
                    if java.name not in jacoco_report:
                        continue
                    data.append(dict(title=java.name, key='{}-{}'.format(java.type, java.id)))
        else:
            for java in java_list:
                desc = json.loads(java.config)
                if (java.name not in jacoco_report) or (
                        java.type == 'class' and name != desc.get('package')) or (
                        java.type == 'method' and name != desc.get('classes')):
                    continue
                data.append(dict(title=java.name if java.type == 'package' else desc.get('classes') if java.type == 'class' else desc.get('method'),
                                 key='{}-{}'.format(java.type, java.name), isLeaf=(java.type == 'method'),
                                 package=desc.get('package'), classes=desc.get('classes')))
        self.write_json(dict(status='SUCCESS', message='', data=dict(type=p_type, data=sorted(data, key=lambda x: x['title']))))

    @authenticated_async
    @gen.coroutine
    def post(self):
        data = yield self.get_request_body_to_json()
        chart_method = list()
        chart_class = list()
        only_chart_class = list()
        chart_package = list()
        for key in data.checkedKeys:
            key = key.split('-')
            if key[0] == 'method' and (key[1] not in chart_method):
                chart_method.append(key[1])
            elif key[0] == 'class' and (key[1] not in chart_class):
                chart_class.append(key[1])
            elif key[0] == 'package' and (key[1] not in chart_package):
                chart_package.append(key[1])
        for key in data.halfCheckedKeys:
            key = key.split('-')
            if key[0] == 'class' and (key[1] not in only_chart_class):
                only_chart_class.append(key[1])
        for p in chart_package[:]:
            for c in chart_class:
                if c.startswith(p) and p in chart_package:
                    chart_package.remove(p)
                    break
        for c in chart_class[:]:
            for m in chart_method:
                if m.startswith(c) and c in chart_class and c not in only_chart_class:
                    chart_class.remove(c)
                    only_chart_class.append(c)
                    break
        line = list()
        method = list()
        classes = list()
        branch = list()
        jacoco_report = os.path.join(static_path, 'files', 'jacoco', data.jid, data.date, 'analysis')
        for p in chart_package:
            json_file = os.path.join(jacoco_report, '{}.json'.format(p))
            if os.path.isfile(json_file):
                with open(json_file, 'r', encoding='utf8') as fp:
                    content = json.loads(fp.read())
                    line.append(dict(missed=content.get('line', dict()).get('missed', 0), covered=content.get('line', dict()).get('covered', 0)))
                    method.append(dict(missed=content.get('method', dict()).get('missed', 0),
                                     covered=content.get('method', dict()).get('covered', 0)))
                    classes.append(dict(missed=content.get('classes', dict()).get('missed', 0),
                                     covered=content.get('classes', dict()).get('covered', 0)))
                    branch.append(dict(missed=content.get('branch', dict()).get('missed', 0),
                                     covered=content.get('branch', dict()).get('covered', 0)))
        for c in chart_class:
            json_file = os.path.join(jacoco_report, '{}.json'.format(c))
            if os.path.isfile(json_file):
                with open(json_file, 'r', encoding='utf8') as fp:
                    content = json.loads(fp.read())
                    line.append(dict(missed=content.get('line', dict()).get('missed', 0),
                                     covered=content.get('line', dict()).get('covered', 0)))
                    method.append(dict(missed=content.get('method', dict()).get('missed', 0),
                                       covered=content.get('method', dict()).get('covered', 0)))
                    classes.append(dict(missed=content.get('classes', dict()).get('missed', 0),
                                        covered=content.get('classes', dict()).get('covered', 0)))
                    branch.append(dict(missed=content.get('branch', dict()).get('missed', 0),
                                       covered=content.get('branch', dict()).get('covered', 0)))
        for c in only_chart_class:
            json_file = os.path.join(jacoco_report, '{}.json'.format(c))
            if os.path.isfile(json_file):
                with open(json_file, 'r', encoding='utf8') as fp:
                    content = json.loads(fp.read())
                    classes.append(dict(missed=content.get('classes', dict()).get('missed', 0),
                                        covered=content.get('classes', dict()).get('covered', 0)))
        for m in chart_method:
            json_file = os.path.join(jacoco_report, '{}.json'.format(m))
            if os.path.isfile(json_file):
                with open(json_file, 'r', encoding='utf8') as fp:
                    content = json.loads(fp.read())
                    line.append(dict(missed=content.get('line', dict()).get('missed', 0),
                                     covered=content.get('line', dict()).get('covered', 0)))
                    method.append(dict(missed=content.get('method', dict()).get('missed', 0),
                                       covered=content.get('method', dict()).get('covered', 0)))
                    classes.append(dict(missed=content.get('classes', dict()).get('missed', 0),
                                        covered=content.get('classes', dict()).get('covered', 0)))
                    branch.append(dict(missed=content.get('branch', dict()).get('missed', 0),
                                       covered=content.get('branch', dict()).get('covered', 0)))
        data = dict(line=list(), method=list(), branch=list(), classes=list())
        missed = dict(x='missed', y=0)
        covered = dict(x='covered', y=0)
        for l in line:
            missed['y'] += l.get('missed', 0)
            covered['y'] += l.get('covered', 0)
        data['line'].append(missed)
        data['line'].append(covered)

        missed = dict(x='missed', y=0)
        covered = dict(x='covered', y=0)
        for m in method:
            missed['y'] += m.get('missed', 0)
            covered['y'] += m.get('covered', 0)
        data['method'].append(missed)
        data['method'].append(covered)

        missed = dict(x='missed', y=0)
        covered = dict(x='covered', y=0)
        for b in branch:
            missed['y'] += b.get('missed', 0)
            covered['y'] += b.get('covered', 0)
        data['branch'].append(missed)
        data['branch'].append(covered)

        missed = dict(x='missed', y=0)
        covered = dict(x='covered', y=0)
        for c in classes:
            missed['y'] += c.get('missed', 0)
            covered['y'] += c.get('covered', 0)
        data['classes'].append(missed)
        data['classes'].append(covered)
        self.write_json(dict(status='SUCCESS', message='', data=data))
