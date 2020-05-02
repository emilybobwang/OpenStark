from tornado.web import RequestHandler, app_log as log
from tornado import gen, httpclient, httputil
from modules.logs import LogsModule
from modules.project import ProjectModule
from functions.common import CommonFunction
from functions.common import ThreadFunction
from munch import munchify
from settings import log_url
import json
import functools
from xml.etree import cElementTree as ET


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
        self.project = ProjectModule()
        self.logs = LogsModule()
        self.common_func = CommonFunction()
        self.thread_func = ThreadFunction()

    # 获取当前用户信息
    @gen.coroutine
    def get_current_user_async(self):
        user = self.get_secure_cookie('OSTSESSION', None)
        return user

    # 返回json格式字符串
    @gen.coroutine
    def write_json(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg, ensure_ascii=False)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(isinstance(msg, str) and msg or str(msg))

    # 返回xml格式字符串
    @gen.coroutine
    def write_xml(self, msg):
        self.set_header("Content-Type", "text/xml; charset=UTF-8")
        self.finish(isinstance(msg, str) and msg or str(msg))

    # 获取json格式请求参数
    @gen.coroutine
    def get_request_body_to_json(self, decode='utf8'):
        params = self.request.body
        if isinstance(params, bytes):
            params = params.decode(decode)
        try:
            params = munchify(json.loads(params, encoding=decode))
        except Exception as e:
            log.error(e)
        return params

    # 获取json格式请求参数
    @gen.coroutine
    def get_request_body_to_xml(self, decode='utf8'):
        params = self.request.body
        if isinstance(params, bytes):
            params = params.decode(decode)
        try:
            params = ET.fromstring(params)
        except Exception as e:
            log.error(e)
        return params

class AddLogs(object):
    def __init__(self):
        self.url = log_url

    @gen.coroutine
    def add_logs(self, tool_id='374', ip='127.0.0.1', op_type='pv'):
        if log_url:
            try:
                api_client = httpclient.AsyncHTTPClient()
                data = dict(toolId=tool_id, ip=ip, type=op_type)
                yield api_client.fetch(self.url, method='POST', body=httputil.urlencode(data))
            except Exception as e:
                log.error(e)
