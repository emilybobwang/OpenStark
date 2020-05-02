from handlers.common import BaseHandler, authenticated_async
from tornado import gen
from handlers.common import AddLogs
from settings import net_mail_to, net_mail_cc
from tornado.web import app_log as log
from functions.mail import Mail
import base64
import json
import uuid


"""
控制台相关接口
"""


# 系统配置
class SystemConfigHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self):
        AddLogs().add_logs(ip=self.request.remote_ip)
        configs = yield self.option.get_options_list(o_type='common')
        config = dict()
        for c in configs:
            if c.name == 'emailPasswd':
                c.value = base64.b16decode(c.value.encode('utf8', errors='ignore')).decode('utf8', errors='ignore')
            config[c.name] = c.value
        nav_links = yield self.option.get_options_list(o_type='navLink')
        link = []
        no = 0
        for nav in nav_links:
            no += 1
            link.append(dict(key=no, id=nav.id, title=nav.name, href=nav.value))
        config['navLink'] = link
        self.write_json(dict(status="SUCCESS", message="", data=config))

    @authenticated_async
    @gen.coroutine
    def post(self):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        configs = yield self.get_request_body_to_json()
        op_type = configs.get('type')
        op = configs.get('op')
        if op_type == 'navLink':
            params = configs.data
            if not self.common_func.check_string(params.href, 'url'):
                return self.write_json(dict(status='FAIL', message='链接格式不对, 请检查!', data=dict(type=op_type)))
            if op == 'edit':
                if params.id == '':
                    res, msg = yield self.option.add_option(o_type='navLink', name=params.title, value=params.href)
                    if res:
                        res_msg = dict(status='SUCCESS', message='保存成功!', data=dict(id=res, type=op_type))
                    else:
                        res_msg = dict(status='FAIL', message=msg, data=dict(type=op_type))
                else:
                    res, msg = yield self.option.edit_option(oid=params.id, name=params.title, value=params.href)
                    if res:
                        res_msg = dict(status='SUCCESS', message='保存成功!', data=dict(type=op_type))
                    else:
                        res_msg = dict(status='FAIL', message=msg, data=dict(type=op_type))
            elif op == 'delete':
                res, msg = yield self.option.delete_option(oid=params.id)
                if res:
                    res_msg = dict(status='SUCCESS', message='删除成功!', data=dict(type=op_type))
                else:
                    res_msg = dict(status='FAIL', message=msg, data=dict(type=op_type))
            else:
                res_msg = dict(status='FAIL', message='操作类型错误!', data=dict(type=op_type))
        else:
            if op_type == 'email' and op == 'test':
                current = self.current_user
                res_msg = dict(status='SUCCESS', message='发送成功!', data=dict(type=op_type))
                params = configs.data
                if len(params) >= 5:
                    mail = Mail(smtp_server=params.emailHost, smtp_port=params.emailPort,
                                smtp_user=params.emailUser, smtp_password=params.emailPasswd,
                                use_ssl=params.get('emailSSL') or 'no', mail_from=params.emailFrom,
                                mail_type=params.get('emailType') or 'normal')
                    message = '''
                    <p>Dear {}:</p>
                    <p>&nbsp;&nbsp;你好, 收到此邮件表示系统邮箱配置正确, 现在开始可以愉快地使用邮件报告功能啦。</p>
                    '''.format(current.username)
                    log.info(message)
                    res, msg = yield mail.send_mail(subject='系统邮件配置成功', message=message, to=[current.email])
                    if not res:
                        log.info(msg)
                        res_msg = dict(status='FAIL', message=str(msg), data=dict(type=op_type))
                else:
                    res_msg = dict(status='FAIL', message='系统邮箱配置不正确!', data=dict(type=op_type))
            else:
                res_msg = dict(status='SUCCESS', message='保存成功!', data=dict(type=op_type))
                for key in configs.data:
                    if key == 'emailPasswd':
                        configs.data[key] = base64.b16encode(configs.data[key].encode('utf8', errors='ignore')).decode('utf8', errors='ignore')
                    res, msg = yield self.option.edit_option(o_type='common', name=key, value=configs.data[key])
                    if not res and configs.data[key]:
                        res, msg = yield self.option.add_option(o_type='common', name=key, value=configs.data[key])
                        if not res:
                            res_msg = dict(status='FAIL', message=msg, data=dict(type=op_type))
        self.write_json(res_msg)


# 项目管理
class ProjectsHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self):
        AddLogs().add_logs(ip=self.request.remote_ip)
        op = self.get_argument('type', '')
        if op == 'projects':
            projects, total = yield self.project.get_projects_list(p_type='project', status=1)
            projects_list = list()
            for p in projects:
                projects_list.append(dict(pid=p.id, name=p.name))
            return self.write_json(dict(status='SUCCESS', message='', data=dict(data=projects_list, type=op)))
        name = self.get_argument('name', '').strip()
        page = int(self.get_argument('page', 1))
        size = int(self.get_argument('size', 10))
        tid = self.get_argument('tid', '').strip()
        projects, total = yield self.project.get_projects_list(p_type='project', page=page, limit=size,
                                                               name=name or None, team_id=tid or None)
        data = []
        no = 0
        for project in projects:
            info = json.loads(project.config) if project.config else dict(description='', params=[])
            no += 1
            data.append(dict(no=no+page*size-size, key=project.id, name=project.name, tid=project.teamId, status=project.status,
                             team=json.loads(project.team)['name'], description=info.get('description'),
                             params=[], pid=project.id, userId=info.get('userId')))
        msg = dict(status='SUCCESS', message='', data=dict(data=data, page=page, size=size, total=total, type=op))
        self.write_json(msg)

    @authenticated_async
    @gen.coroutine
    def post(self, op='edit'):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        data = yield self.get_request_body_to_json()
        if op == 'edit':
            if data.name.strip() == '':
                return self.write_json(msg=dict(status='FAIL', message='项目名称不能为空!', data=''))
            if str(data.key).find('NEW_TEMP_ID') != -1 and data.pid == '':
                pid, msg = yield self.project.add_project(
                    name=data.name.strip(), p_type='project', status=data.status, team_id=data.tid,
                    config=dict(description=data.description, userId=self.current_user.id))
                if pid:
                    content = dict(group=dict(name=data.team), project=dict(name=data.name.strip()),
                                   template='在 @{group} 新建了项目 @{project}')
                    self.msg.add_message(user_id=self.current_user.id, m_type='active', content=content)
                    msg = dict(status='SUCCESS', message='新增成功', data=dict(pid=pid))
                else:
                    msg = dict(status='FAIL', message=msg, data='')
            else:
                res, msg = yield self.project.edit_project(
                    pid=data.pid, name=data.name.strip(), status=data.status, team_id=data.tid,
                    config=dict(description=data.description, userId=data.userId))
                if res:
                    msg = dict(status='SUCCESS', message='编辑成功', data=dict(pid=data.pid))
                else:
                    msg = dict(status='FAIL', message=msg, data='')
        elif op == 'delete':
            res, msg = yield self.project.delete_project(pid=data.pid)
            if res:
                if not isinstance(data.pid, list):
                    content = dict(group=dict(name=data.team), project=dict(name=data.name.strip()),
                               template='删除了 @{group} 的项目 @{project}')
                else:
                    content = dict(group=dict(), project=dict(),
                               template='批量删除了项目')
                self.msg.add_message(user_id=self.current_user.id, m_type='active', content=content)
                yield self.statistics.delete_statistics(project_id=data.pid)
                msg = dict(status='SUCCESS', message='删除成功', data='')
            else:
                msg = dict(status='FAIL', message=msg, data='')
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)


# 测试环境管理
class EnvironmentManage(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op=None, do=None):
        AddLogs().add_logs(ip=self.request.remote_ip)
        if op == 'server':
            if do == 'list':
                page = int(self.get_argument('page', 1))
                size = int(self.get_argument('size', 10))
                key_word = self.get_argument('keyWord', '').strip()
                status = self.get_argument('status', None)
                e_type = self.get_argument('type', '')
                env_list, total = yield self.project.get_projects_list(
                    p_type='env', page=page, limit=size, status=status or None, search=key_word or e_type or None)
                data = list()
                no = 0
                for env in env_list:
                    desc = json.loads(env.config)
                    if e_type and e_type.find(desc.get('type')) == -1:
                        total -= 1
                        continue
                    no += 1
                    data.append(dict(no=no+page*size-size, key=env.id, eid=env.name, title=desc.get('title'),
                                     type=desc.get('type'), description=desc.get('description'),
                                     principal=desc.get('principal').get('name'), status=env.status,
                                     uid=desc.get('principal').get('uid'), dep=desc.get('principal').get('dep'),
                                     username=desc.get('principal').get('username')))
                self.write_json(dict(status='SUCCESS', message='',
                                     data=dict(data=data, total=total, page=page, size=size)))
            elif do == 'all':
                env_list, total = yield self.project.get_projects_list(p_type='env', status=1)
                data = list()
                for env in env_list:
                    desc = json.loads(env.config)
                    data.append(dict(key=env.id, id=env.name, title=desc.get('title'),
                                     description=desc.get('description')))
                self.write_json(dict(status='SUCCESS', message='',
                                     data=dict(data=data, total=total, page=1, size=10)))
            else:
                self.write_json(dict(status='FAIL', message='操作类型错误', data=''))
        elif op == 'detail':
            if do == 'list':
                page = int(self.get_argument('page', 1))
                size = int(self.get_argument('size', 10))
                key_word = self.get_argument('keyWord', '').strip()
                status = self.get_argument('status', None)
                e_type = self.get_argument('type', '')
                network = self.get_argument('network', '')
                eid = self.get_argument('eid', '')
                detail_list, total = yield self.setting.get_settings_list(
                    s_type='env', name=eid, page=page, limit=size, status=status or None, search=key_word or None)
                data = list()
                no = 0
                for detail in detail_list:
                    desc = json.loads(detail.value)
                    if (e_type and e_type.find(desc.get('type')) == -1) or (
                            network and network.find(desc.get('network')) == -1):
                        total -= 1
                        continue
                    no += 1
                    data.append(dict(no=no+page*size-size, key=detail.id, title=desc.get('title'),
                                     type=desc.get('type'), description=desc.get('description'),
                                     host=desc.get('host'), ip=desc.get('ip'), status=detail.status,
                                     port=desc.get('port'), user=desc.get('user'), mac=desc.get('mac'),
                                     password=desc.get('password'), network=desc.get('network')))
                self.write_json(dict(status='SUCCESS', message='',
                                     data=dict(data=data, total=total, page=page, size=size)))
            elif do == 'all':
                eid = self.get_argument('eid', '')
                detail_list, total = yield self.setting.get_settings_list(s_type='env', name=eid, status=1)
                data = list()
                keys = list()
                for detail in detail_list:
                    desc = json.loads(detail.value)
                    if desc.get('type') != self.get_argument('type', 'OS') or desc.get('ip').strip() in keys:
                        continue
                    data.append(dict(key=detail.id, title=desc.get('ip').strip(),
                                     description=desc.get('title').strip(), id=desc.get('ip').strip()))
                    keys.append(desc.get('ip').strip())
                self.write_json(dict(status='SUCCESS', message='',
                                     data=dict(data=data, total=total, page=1, size=10)))
            else:
                self.write_json(dict(status='FAIL', message='操作类型错误', data=''))
        else:
            self.write_json(dict(status='FAIL', message='操作类型错误', data=''))

    @authenticated_async
    @gen.coroutine
    def post(self, op=None, do=None):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        data = yield self.get_request_body_to_json()
        if op == 'server':
            if do == 'edit':
                desc = dict(description=data.get('description'), title=data.get('title'), type=data.get('type'),
                            principal=dict(name=data.get('principal'), username=data.get('username'),
                                           uid=data.get('uid'), dep=data.get('dep')))
                if str(data.key).find('NEW_TEMP_KEY') != -1:
                    eid = str(uuid.uuid1())
                    key, msg = yield self.project.add_project(p_type='env', name=eid, config=desc, status=data.status or 1)
                    if key:
                        ret_msg = dict(status='SUCCESS', message='新增成功!', data=dict(eid=eid, key=key))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data='')
                else:
                    res, msg = yield self.project.edit_project(pid=data.key, config=desc, status=data.status or None)
                    if res:
                        ret_msg = dict(status='SUCCESS', message='编辑成功!', data=dict(eid=data.eid, key=data.key))
                    else:
                        ret_msg = dict(status='FAIL', message=msg, data='')
            elif do == 'delete':
                res, msg = yield self.project.delete_project(pid=data.key)
                if res:
                    ret_msg = dict(status='SUCCESS', message='删除成功!', data='')
                else:
                    ret_msg = dict(status='FAIL', message=msg, data='')
            elif do == 'host':
                env_list, total = yield self.setting.get_settings_list(
                    s_type='env', name=data.get('eid'), status=1)
                data = list()
                hosts = list()
                for env in env_list:
                    desc = json.loads(env.value)
                    host = (desc.get('ip').strip(), desc.get('host').strip())
                    if desc.get('host').strip() and desc.get('ip').strip() and host not in hosts:
                        data.append('{}\t\t{}\t\t# {}'.format(
                            desc.get('ip').strip(), desc.get('host').strip(), desc.get('title').strip()))
                        hosts.append(host)
                ret_msg = dict(status='SUCCESS', message='获取HOST成功!', data='\n'.join(data))
            else:
                ret_msg = dict(status='FAIL', message='操作类型错误', data='')
        elif op == 'detail':
            if do == 'edit':
                if self.common_func.check_string(data.get('ip').strip(), 'ip'):
                    desc = dict(description=data.get('description'), title=data.get('title'), type=data.get('type'),
                                host=data.get('host'), ip=data.get('ip'), port=data.get('port'),  user=data.get('user'),
                                mac=data.get('mac'), password=data.get('password'), network=data.get('network') or 'no')
                    if str(data.key).find('NEW_TEMP_KEY') != -1:
                        server = yield self.project.get_project(name=data.eid, p_type='env')
                        if server:
                            key, msg = yield self.setting.add_setting(
                                s_type='env', pid=server.id, name=data.eid, value=desc, status=data.status or 1)
                            if key:
                                ret_msg = dict(status='SUCCESS', message='新增成功!', data=dict(key=key))
                            else:
                                ret_msg = dict(status='FAIL', message=msg, data='')
                        else:
                            ret_msg = dict(status='FAIL', message='所要编辑的环境信息不存在!', data='')
                    else:
                        res, msg = yield self.setting.edit_setting(sid=data.key, value=desc, status=data.status or None)
                        if res:
                            ret_msg = dict(status='SUCCESS', message='编辑成功!', data=dict(key=data.key))
                        else:
                            ret_msg = dict(status='FAIL', message=msg, data='')
                else:
                    ret_msg = dict(status='FAIL', message='IP地址格式不对, 请检查!', data='')
            elif do == 'delete':
                res, msg = yield self.setting.delete_setting(sid=data.key)
                if res:
                    ret_msg = dict(status='SUCCESS', message='删除成功!', data='')
                else:
                    ret_msg = dict(status='FAIL', message=msg, data='')
            elif do == 'status':
                ret_data = list()
                server = yield self.setting.get_settings_by_id(sid=data.key)
                for svr in server:
                    desc = json.loads(svr.value)
                    env_type = desc.get('type')
                    env_ip = desc.get('ip') or ''
                    env_port = desc.get('port') or ''
                    env_user = desc.get('user') or ''
                    env_password = desc.get('password') or ''
                    env_title = desc.get('title') or ''
                    if env_type == 'OS':
                        if env_title.strip().split('_', maxsplit=1)[0].lower().startswith('linux'):
                            linux_shell = '''
                            mac1=`ifconfig -a|grep -C 2 %s|awk 'NR==1{print}'|awk '{print $5}'`&&mac2=`ifconfig -a|grep -C 2 %s|awk 'END{print}'|awk '{print $2}'`&&net=`ping -c 2 www.baidu.com|awk 'END{print}'`&&echo "$mac1 mac1"&&echo "$mac2 mac2"&&echo "$net net"
                            ''' % (env_ip.strip(), env_ip.strip())
                            flag, msg = yield self.thread_func.exec_remote_shell(
                                host=env_ip.strip(), port=env_port.strip(), shell=linux_shell,
                                username=env_user.strip(), password=env_password.strip())
                            if flag:
                                msg = msg.split('\n')
                                if len(msg) == 3:
                                    mac = msg[1] if msg[0].strip() == 'mac1' else msg[0]
                                    net = 'no' if msg[2].strip() == 'net' else 'yes'
                                    desc['mac'] = desc.get('mac') or mac.split()[0].upper()
                                    desc['network'] = net
                                status = 1
                            else:
                                res = yield self.thread_func.check_port(env_ip, env_port)
                                if res:
                                    status = 1
                                else:
                                    status = 0
                            yield self.setting.edit_setting(svr.id, value=desc, status=status)
                            ret_data.append(dict(key=svr.id, status=status, network=desc['network'], mac=desc['mac']))
                    elif env_type == 'APPLICATION':
                        res = yield self.thread_func.check_port(env_ip, env_port)
                        if res:
                            status = 1
                        else:
                            status = 0
                        yield self.setting.edit_setting(svr.id, status=status)
                        ret_data.append(dict(key=svr.id, status=status))
                ret_msg = dict(status='SUCCESS', message='刷新状态成功!', data=ret_data)
            elif do == 'network':
                title = yield self.project.get_project(name=data.eid, p_type='env')
                server = yield self.setting.get_settings_by_id(sid=data.key)
                ips = []
                for svr in server:
                    desc = json.loads(svr.value)
                    if desc.get('ip'):
                        ips.append(desc.get('ip').strip())
                title = '测试环境申请开放外网权限_{}'.format(title and json.loads(title.config).get('title'))
                mail_content = '''
<p>Hi 你好！</p>
<p style="padding-left:30px;">测试人员 ({}) 申请开放本测试环境服务器外网权限，以供功能测试验收。请帮忙处理一下，3ks~</p>
<p style="padding-left:30px;">1、服务器</p>
<p style="padding-left:60px;">{}</p>
<p style="padding-left:30px;">2、使用时间</p>
<p style="padding-left:60px;">开始使用时间：{}</p>
<p style="padding-left:60px;">结束使用时间：{}</p>
<p style="padding-left:30px;">3、备注</p>
<p style="padding-left:60px;">凡是开放了外网权限的服务器必须做到以下准备工作，否则会造成线上问题：</p>
<p style="padding-left:60px;">1、6020-common-service服务必须关闭</p>
<p style="padding-left:60px;">2、短信、邮箱相关配置必须设置为测试配置</p>
<p style="padding-left:60px;">3、使用完毕要及时申请关闭外网权限</p>     
                '''.format(self.current_user.realname, '</br>'.join(set(ips)), data.startTime, data.endTime)
                res, msg = yield self.common_func.send_email(
                    subject=title, content=mail_content, to=net_mail_to, cc=net_mail_cc)
                if res:
                    ret_msg = dict(status='SUCCESS', message='申请邮件发送成功!', data='')
                    for svr in server:
                        desc = json.loads(svr.value)
                        desc['network'] = 'yes'
                        yield self.setting.edit_setting(sid=svr.id, value=desc, create_time=data.endTime)
                else:
                    ret_msg = dict(status='FAIL', message=msg, data='')
            else:
                ret_msg = dict(status='FAIL', message='操作类型错误', data='')
        else:
            ret_msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(ret_msg)
