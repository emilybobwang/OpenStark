from tornado.web import RequestHandler, app_log as log
from tornado import gen, httpclient, httputil
from modules.setting import SettingModule
from modules.user import UserModule
from modules.project import ProjectModule
from modules.option import OptionModule
from modules.messages import MessagesModule
from modules.statistics import StatisticsModule
from functions.common import CommonFunction
from functions.common import ThreadFunction
from functions.options import OptionsFunction
from munch import munchify
from settings import log_url
import json
import time
import functools
import base64


# 异步用户认证
def authenticated_async(f):
    @functools.wraps(f)
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        self._auto_finish = False
        self.current_user = yield self.get_current_user_async()
        if not self.current_user:
            self.set_status(401, '登录超时')
            yield self.write_json(dict(status='FAIL', message='登录超时, 请重新登录!', data=dict(authority='guest')))
        else:
            f(self, *args, **kwargs)
    return wrapper


class BaseHandler(RequestHandler):
    """
    后台管理父类，后台相关handlers继承本类
    """
    current_user = None

    # 初始化方法
    @gen.coroutine
    def prepare(self):
        self.user = UserModule()
        self.project = ProjectModule()
        self.setting = SettingModule()
        self.option = OptionModule()
        self.msg = MessagesModule()
        self.statistics = StatisticsModule()
        self.common_func = CommonFunction()
        self.option_func = OptionsFunction()
        self.thread_func = ThreadFunction()

    # 获取当前用户信息
    @gen.coroutine
    def get_current_user_async(self):
        user = self.get_secure_cookie('OSTSESSION', None)
        try:
            token = self.request.headers.get('Token')
            if token and not user:
                user = base64.b64decode(base64.b16decode(token.strip().encode('utf8'))).decode('utf8')
        except Exception as e:
            log.error(e)
        if user is not None:
            if isinstance(user, bytes):
                user = user.decode('utf8', errors='ignore')
            user = yield self.user.get_user_info(email_or_username=user)
            if not user:
                self.clear_cookie('OSTSESSION')
            else:
                self.set_secure_cookie('OSTSESSION', user.email, expires=time.time() + 1800)
        return user

    # 返回json格式字符串
    @gen.coroutine
    def write_json(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg, ensure_ascii=False)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(msg)

    # 获取json格式请求参数
    @gen.coroutine
    def get_request_body_to_json(self):
        params = self.request.body
        if isinstance(params, bytes):
            params = params.decode('utf8')
        try:
            params = munchify(json.loads(params))
        except Exception as e:
            log.error(e)
            params = None
        return params

    # 登录或注册
    @gen.coroutine
    def _login_or_register(self, username='', email='', name='', department='', password='123456'):
        self.clear_cookie('OSTSESSION')
        if (username == '' and email == '') or password == '' or name == '' or department == '':
            return False, '[自动登录]请求参数不对!'
        username = email if email != '' else username
        user = yield self.user.get_user_info(username)
        if not user:
            if not self.common_func.check_string(username, 'email') and not self.common_func.check_string(password, 'password'):
                return False, '[自动注册]邮箱或密码格式不对!'
            else:
                user, msg = yield self.user.register_user(email=email, password=password, real_name=name, status=2,
                                                          profile=dict(department=department, avatar='https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png', position=''))
                if user:
                    self.set_secure_cookie('OSTSESSION', email, expires=time.time() + 1800)
                    content = dict(group=dict(name='', link=''), project=dict(name='', link=''),
                                   template='同学, 欢迎加入组织!')
                    self.msg.add_message(user_id=user.id, m_type='active', content=content)
                return user, '[自动注册]{}'.format(msg)
        elif user.password == self.common_func.encode_password(password) and user.status != 0:
            self.user.edit_user(username, last_login_time=time.strftime('%Y-%m-%d %H:%M:%S'))
            self.set_secure_cookie('OSTSESSION', email, expires=time.time() + 1800)
            content = dict(group=dict(name='', link=''), project=dict(name='', link=''),
                           template='同学, 欢迎回来!')
            self.msg.add_message(user_id=user.id, m_type='active', content=content)
            return user, '[自动登录]操作成功!'
        else:
            return False, '[自动登录]登录密码不对或账户被禁用!'


class AddLogs(object):
    def __init__(self):
        self.project = ProjectModule()
        self.statistics = StatisticsModule()

    @gen.coroutine
    def add_logs(self, tool_id='34', ip='127.0.0.1', op_type='pv'):
        try:
            data = munchify(dict(toolId=tool_id, type=op_type, ip=ip))
            tool = yield self.project.get_project(pid=data.toolId)
            if tool and data.type in ['pv', 'active']:
                data['name'] = tool.name
                self.statistics.add_statistics(s_type=data.type, project_id=data.toolId,
                                                                   name=data.ip, value=data)
                if data.type == 'active':
                    self.statistics.add_statistics(s_type='pv', project_id=data.toolId, name=data.ip, value=data)
        except Exception as e:
            log.error(e)
