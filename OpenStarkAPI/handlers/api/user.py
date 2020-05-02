from handlers.common import BaseHandler, authenticated_async
from tornado import gen, httpclient
from tornado.web import app_log as log
from handlers.common import AddLogs
from settings import auto_login_url
import time
import datetime
import json
import base64


"""
用户相关接口
"""


# 注册接口
class RegisterHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        params = yield self.get_request_body_to_json()
        email = params.email or ''
        name = params.name or ''
        department = params.department or []
        password = params.password or ''
        confirm = params.confirm or ''
        if not self.common_func.check_string(name.strip(), 'realname'):
            msg = dict(status='FAIL', message='请填写正确的中文姓名!', data='')
        elif not department:
            msg = dict(status='FAIL', message='请选择部门!', data='')
        elif not self.common_func.check_string(email, 'email'):
            msg = dict(status='FAIL', message='邮箱格式不对, 请检查!', data='')
        elif not self.common_func.check_string(password, 'password'):
            msg = dict(status='FAIL', message='密码格式不对, 请检查!', data='')
        elif password != confirm:
            msg = dict(status='FAIL', message='密码跟确认密码不一致, 请检查!', data='')
        else:
            user, msg = yield self.user.register_user(email=email, password=password, real_name=name,
                                                      profile=dict(department=department, avatar='https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png', position=''))
            if user:
                self.set_secure_cookie('OSTSESSION', email, expires=time.time()+1800)
                if user.role == 0:
                    authority = 'admin'
                elif user.role == 1 and user.status == 2:
                    authority = 'user'
                elif user.role == 1 and user.status == 1:
                    authority = 'noActive'
                else:
                    authority = 'guest'
                msg = dict(status='SUCCESS', message=msg, data=dict(authority=authority))
                log.info('{} 注册成功'.format(email))
                if authority == 'noActive':
                    end_time = datetime.datetime.now() + datetime.timedelta(days=3)
                    content = dict(title='激活账户', description='请在 {} 前激活您的账户, 否则将自动注销。'.format(
                        end_time.strftime('%Y-%m-%d')))
                    self.msg.add_message(user_id=user.id, m_type='todo', content=content)
                    config = yield self.option_func.get_option_by_type(o_type='common')
                    data = base64.b64encode(email.encode('utf8', errors='ignore')).decode('utf8', errors='ignore')
                    url = '{}/{}?data={}'.format(self.request.headers.get('Origin'), 'api/py/activeUser', data)
                    html = '''
                    <p>Dear {}:</p>
                    <p>&nbsp;&nbsp;欢迎使用{}, 请点击下面链接激活你的账户, 谢谢!</p>
                    <p><a href="{}">{}</a></p>
                    '''.format(name, config.get('sysName'), url, url)
                    yield self.common_func.send_email(
                        subject='[{}]请尽快激活你的账户'.format(config.get('sysName')), content=html, to=[email])
                content = dict(group=dict(name='', link=''), project=dict(name='', link=''),
                               template='同学, 欢迎加入组织!')
                self.msg.add_message(user_id=user.id, m_type='active', content=content)
            else:
                msg = dict(status='FAIL', message=msg, data='')
                log.warn('{} 注册失败#{}'.format(email, msg))
        self.write_json(msg)


# 登录接口
class LoginHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        params = yield self.get_request_body_to_json()
        username = params.userName or ''
        password = params.password or ''
        user = yield self.user.get_user_info(username)
        if not user:
            msg = dict(status='FAIL', message='用户不存在!', data='')
            log.warn('{} 用户不存在'.format(username))
        elif user.password == self.common_func.encode_password(password) and user.status != 0:
            self.user.edit_user(username, last_login_time=time.strftime('%Y-%m-%d %H:%M:%S'))
            self.set_secure_cookie('OSTSESSION', user.email, expires=time.time()+1800)
            if user.role == 0:
                authority = 'admin'
            elif user.role == 1 and user.status == 2:
                authority = 'user'
            elif user.role == 1 and user.status == 1:
                authority = 'noActive'
            else:
                authority = 'guest'
            msg = dict(status='SUCCESS', message='', data=dict(authority=authority))
            log.info('{} 登录成功'.format(username))
            content = dict(group=dict(name='', link=''), project=dict(name='', link=''),
                           template='同学, 欢迎回来!')
            self.msg.add_message(user_id=user.id, m_type='active', content=content)
        elif user.status == 0:
            msg = dict(status='FAIL', message='用户被禁用, 请联系管理员!', data='')
            log.warn('{} 用户被禁用, 请联系管理员'.format(username))
        else:
            msg = dict(status='FAIL', message='密码不正确!', data='')
            log.warn('{} 密码不正确'.format(username))
        self.write_json(msg)


# 自动登录接口
class AutoLoginHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        common_info = yield self.option.get_option(o_type='common', name='autoLogin', status=1)
        if auto_login_url and (common_info and common_info.value == 'yes'):
            try:
                api_client = httpclient.AsyncHTTPClient()
                resp = yield api_client.fetch(
                    '{}?ip={}'.format(
                        auto_login_url, self.request.remote_ip), method='GET')
                data = resp.body
                if isinstance(data, bytes):
                    data = data.decode('utf8', errors='ignore')
                data = json.loads(data)
                if data:
                    email = data[0]['email'].strip()
                    name = data[0]['userName'].strip()
                    department = []
                    dep = yield self.option.get_options_list(o_type='teams', status=1)
                    for d in dep:
                        dv = json.loads(d.value)
                        if d.name == 'department' and dv['name'] == data[0]['department'].strip():
                            department.append(dv['up'])
                            department.append(d.id)
                            break
                    user, msg = yield self._login_or_register(email=email, name=name, department=department,
                                                              password=email.split('@')[0]+'123456')
                else:
                    user = None
                    msg = '[自动登录]通过IP {} 获取用户信息失败, 获取到的信息为 {}'.format(self.request.remote_ip, data)
            except Exception as e:
                log.error(e)
                user = None
                msg = str(e)
            if user:
                if user.role == 0:
                    authority = 'admin'
                elif user.role == 1 and user.status == 2:
                    authority = 'user'
                elif user.role == 1 and user.status == 1:
                    authority = 'noActive'
                else:
                    authority = 'guest'
                data = dict(status='SUCCESS', message=msg, data=dict(authority=authority))
            else:
                data = dict(status='FAIL', message=msg, data='')
        else:
            data = dict(status='FAIL', message='', data='')
        self.write_json(data)


# 退出接口
class LogoutHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.clear_cookie('OSTSESSION')
        msg = dict(status='SUCCESS', message='', data=dict(authority='guest'))
        self.write_json(msg)


# 激活用户接口
class ActiveUserHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        data = self.get_argument('data', None)
        if data:
            email = base64.b64decode(data.encode('utf8')).decode('utf8')
            user = yield self.user.get_user_info(email_or_username=email, status=1)
            if user:
                yield self.user.edit_user(email=email, status=2)
        self.clear_cookie('OSTSESSION')
        self.redirect('/')

    @authenticated_async
    @gen.coroutine
    def post(self):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        user = self.current_user
        config = yield self.option_func.get_option_by_type(o_type='common')
        if user.status == 1:
            data = base64.b64encode(user.email.encode('utf8', errors='ignore')).decode('utf8', errors='ignore')
            url = '{}/{}?data={}'.format(self.request.headers.get('Origin'), 'api/py/activeUser', data)
            html = '''
            <p>Dear {}:</p>
            <p>&nbsp;&nbsp;欢迎使用{}, 请点击下面链接激活你的账户, 谢谢!</p>
            <p><a href="{}">{}</a></p>
            '''.format(user.username, config.get('sysName'), url, url)
            res, msg = yield self.common_func.send_email(
                subject='[{}]请尽快激活你的账户'.format(config.get('sysName')), content=html, to=[user.email])
            if res:
                msg = dict(status='SUCCESS', message='激活邮件发送成功!', data=dict(type='active'))
            else:
                log.info(msg)
                msg = dict(status='FAIL', message=str(msg), data=dict(type='active'))
        else:
            msg = dict(status='FAIL', message='用户已是激活状态!', data=dict(type='active'))
        self.write_json(msg)


# 当前用户信息
class CurrentUserHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self):
        AddLogs().add_logs(ip=self.request.remote_ip)
        user = self.current_user
        profile = json.loads(user.profile)
        department = ''
        work_id = profile['workerId'] if 'workerId' in profile.keys() else ''
        for oid in profile['department']:
            dep = yield self.option.get_option(oid=oid)
            if dep:
                department = '{} / {}'.format(department, json.loads(dep.value)['name'])
        if user.role == 0:
            authority = 'admin'
        elif user.role == 1 and user.status == 2:
            authority = 'user'
        elif user.role == 1 and user.status == 1:
            authority = 'noActive'
        else:
            authority = 'guest'
        data = dict(name='{}{}'.format(user.realname, '[未激活]' if user.status == 1 else work_id and '[{}]'.format(work_id)),
                    avatar=profile['avatar'], userId=user.id, unreadCount=user.unreadCount, authority=authority,
                    email=user.email, department=department[3:], position=profile['position'], workerId=work_id,
                    department_id=profile['department'], username=user.username, status=user.status,
                    realname=user.realname, token=base64.b16encode(base64.b64encode(user.email.encode('utf8'))).decode('utf8'))
        self.write_json(dict(status='SUCCESS', message='', data=data))

    @authenticated_async
    @gen.coroutine
    def post(self):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        user = self.current_user
        data = yield self.get_request_body_to_json()
        save_data = data.data
        flag = False
        if data.type == 'info':
            department = save_data.department_id or []
            if not department:
                msg = '请选择部门!'
            elif not self.common_func.check_string(save_data.username.strip(), 'username'):
                msg = '用户名格式不对, 请检查!'
            elif not self.common_func.check_string(save_data.realname.strip(), 'realname'):
                msg = '请填写正确的中文姓名!'
            elif not self.common_func.check_string(save_data.email.strip(), 'email'):
                msg = '邮箱格式不对, 请检查!'
            else:
                profile = dict(department=save_data.department_id, workerId=save_data.workerId.strip(),
                               avatar=json.loads(user.profile)['avatar'], position=save_data.position.strip())
                flag, msg = yield self.user.edit_user(uid=user.id, username=save_data.username.strip(),
                                                      real_name=save_data.realname.strip(),
                                                      profile=profile, email=save_data.email.strip())
        elif data.type == 'passwd':
            if not self.common_func.check_string(save_data.newPasswd, 'password'):
                msg = '密码格式不对, 请检查!'
            else:
                if self.common_func.encode_password(save_data.password) != user.password:
                    msg = '原密码不正确!'
                elif save_data.newPasswd == save_data.rePasswd:
                    flag, msg = yield self.user.edit_user(uid=user.id, password=save_data.newPasswd)
                else:
                    msg = '新密码与确认密码不一致!'
        else:
            msg = '操作类型错误!'
        self.write_json(dict(status='SUCCESS' if flag else 'FAIL', message='修改成功' if flag else msg, data=dict(type=data.type)))


# 用户动态
class ActivitiesHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self):
        data = dict(active=[], users=[], blogs=[])
        msgs, count = yield self.msg.get_messages_list(m_type='active', status=1, limit=6)
        for msg in msgs:
            content = json.loads(msg.content)
            active = dict(id=msg.id, updatedAt=msg.createTime.strftime('%Y-%m-%d %H:%M:%S'),
                          user=dict(name=msg.realname, avatar=json.loads(msg.profile)['avatar']),
                          group=content.get('group'), project=content.get('project'),
                          comment=content.get('comment'), template=content.get('template'))
            data['active'].append(active)
        users, count = yield self.user.get_users_list(status=2, limit=None)
        for user in users:
            profile = json.loads(user.profile)
            data['users'].append(dict(uid=user.id, name=user.realname, username=user.username, avatar=profile['avatar']))
        blogs, count = yield self.project.get_projects_list(p_type='knowledge.book', status=1, limit=8)
        for blog in blogs:
            desc = json.loads(blog.config)
            book = dict(id=blog.id, updatedAt=blog.createTime.strftime('%Y-%m-%d %H:%M:%S'),
                        project=dict(name=desc.get('title'), link="/knowledge/books/blog/{}/{}".format(blog.teamId, blog.id)),
                        template='分享的《@{project}》', uid=desc.get('uid'))
            data['blogs'].append(book)
        self.write_json(dict(status='SUCCESS', message='', data=data))


# 用户通知
class NoticesHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self):
        m_type = self.get_argument('type', None)
        offset = int(self.get_argument('offset', 0))
        user = self.current_user
        data = list()
        if m_type is None or m_type == 'event':
            msgs, count = yield self.msg.get_messages_list(m_type='todo', user_id=user.id, offset=offset, status=[1,2,3,4,5])
        else:
            msgs = list()
        for msg in msgs:
            read = False
            if msg.status == 1:
                todo_status = 'todo'
                extra = '未开始'
            elif msg.status == 2:
                todo_status = 'processing'
                extra = '进行中'
            elif msg.status == 3:
                todo_status = 'doing'
                extra = '已耗时 {} 天'.format((datetime.datetime.now() - datetime.datetime.strptime(
                    msg.createTime.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')).days)
            elif msg.status == 4:
                todo_status = 'urgent'
                extra = '马上到期'
            elif msg.status == 5:
                todo_status = 'done'
                extra = '已完成'
                read = True
            else:
                continue
            content = json.loads(msg.content)
            notice = dict(id=msg.id, title=content.get('title'), description=content.get('description'),
                          extra=extra, status=todo_status, type='event', read=read)
            data.append(notice)
        if m_type is None or m_type == 'notification':
            msgs, count = yield self.msg.get_messages_list(m_type='notice', user_id=user.id, offset=offset, status=[1,2])
        else:
            msgs = list()
        for msg in msgs:
            if msg.status == 1:
                read = False
            elif msg.status == 2:
                read = True
            else:
                continue
            content = json.loads(msg.content)
            notice = dict(id=msg.id, title=content.get('title'), avatar=content.get('avatar'), read=read,
                          datetime=msg.createTime.strftime('%Y-%m-%d %H:%M:%S'), type='notification')
            data.append(notice)
        if m_type is None or m_type == 'message':
            msgs, count = yield self.msg.get_messages_list(m_type='message', user_id=user.id, offset=offset, status=[1,2])
        else:
            msgs = list()
        for msg in msgs:
            if msg.status == 1:
                read = False
            elif msg.status == 2:
                read = True
            else:
                continue
            content = json.loads(msg.content)
            notice = dict(id=msg.id, title=content.get('title'), avatar=content.get('avatar'),
                          description=content.get('description'), type='message', read=read,
                          datetime=msg.createTime.strftime('%Y-%m-%d %H:%M:%S'))
            data.append(notice)
        if len(data) == 0:
            data.append(None)
        self.write_json(dict(status='SUCCESS', message='', data=data))

    @authenticated_async
    @gen.coroutine
    def post(self):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        user = self.current_user
        params = yield self.get_request_body_to_json()
        m_type = ''
        if params.type == 'notification':
            m_type = 'notice'
        elif params.type == 'message':
            m_type = 'message'
        elif params.type == 'event':
            m_type = 'todo'
        elif params.type == 'read':
            msg = yield self.msg.get_message(mid=params.mid)
            if msg and msg.type == 'todo':
                status = 5 if msg.status == 3 else msg.status + 1
                status = 0 if status > 5 else status
            else:
                status = 0 if msg.status == 2 else 2
            yield self.msg.edit_message(mid=params.mid, status=status)
            if msg.type == 'notice':
                m_type = '通知'
            elif msg.type == 'message':
                m_type = '消息'
            elif msg.type == 'todo':
                m_type = '待办'
            return self.write_json(dict(status='SUCCESS', message='{} 状态已变更!'.format(m_type), data=''))
        if m_type:
            res, msg = yield self.msg.edit_message(m_type=m_type, user_id=user.id, status=0)
            if res:
                msg = dict(status='SUCCESS', message='清除成功', data='')
            else:
                msg = dict(status='FAIL', message='清除失败', data='')
        else:
            msg = dict(status='FAIL', message='清除失败', data='')
        self.write_json(msg)


# 自定义导航
class CustomNavHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op='all'):
        links = yield self.option.get_options_list(o_type='navLink')
        user = self.current_user
        profile = json.loads(user.profile)
        nav_list = []
        id_num = 0
        if op == 'all':
            for link in links:
                id_num += 1
                nav_list.append(dict(id=id_num, title=link.name, href=link.value))
            if 'nav' in profile.keys():
                for link in profile['nav']:
                    id_num += 1
                    link['id'] = id_num
                    nav_list.append(link)
            msg = dict(status='SUCCESS', message='', data=nav_list)
        elif op == 'own':
            if 'nav' in profile.keys():
                for link in profile['nav']:
                    id_num += 1
                    link['key'] = id_num
                    nav_list.append(link)
            msg = dict(status='SUCCESS', message='', data=nav_list)
        else:
            msg = dict(status='FAIL', message='操作类型错误!', data=[])
        self.write_json(msg)

    @authenticated_async
    @gen.coroutine
    def post(self, op='edit'):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        params = yield self.get_request_body_to_json()
        params = params.data
        user = self.current_user
        profile = json.loads(user.profile)
        if not self.common_func.check_string(params.href, 'url'):
            return self.write_json(dict(status='FAIL', message='链接格式不对, 请检查!', data=''))
        if op == 'edit':
            nid = 1
            if 'nav' not in profile.keys():
                profile['nav'] = [dict(id=nid, title=params.title, href=params.href)]
            elif 'id' not in params.keys() or params.id == '':
                nid = len(profile['nav']) + 1
                profile['nav'].append(dict(id=nid, title=params.title, href=params.href))
            else:
                for link in profile['nav']:
                    if link['id'] == params.id:
                        link['title'] = params.title
                        link['href'] = params.href
            res, msg = yield self.user.edit_user(uid=user.id, profile=profile)
            if res:
                msg = dict(status='SUCCESS', message='便捷导航保存成功!', data=dict(id=nid))
            else:
                msg = dict(status='FAIL', message=msg, data='')
        elif op == 'delete':
            if 'nav' in profile.keys():
                for link in profile['nav']:
                    if link['id'] == params.id:
                        profile['nav'].remove(link)
                res, msg = yield self.user.edit_user(uid=user.id, profile=profile)
                if res:
                    msg = dict(status='SUCCESS', message='删除便捷导航成功!', data='')
                else:
                    msg = dict(status='FAIL', message=msg, data='')
            else:
                msg = dict(status='FAIL', message='便捷导航列表为空!', data='')
        else:
            msg = dict(status='FAIL', message='操作类型错误!', data='')
        self.write_json(msg)
