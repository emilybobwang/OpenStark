from tornado import gen
from handlers.common import BaseHandler


class IndexHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.redirect('/admin/login')
        """
        argv = dict(title='首页')
        argv = dict(self.argv, **argv)
        self.render('index.html', **argv)
        """


class HelpHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.redirect('/static/readme.html')

    @gen.coroutine
    def post(self):
        data = {"status": "SUCCESS", "message": "接口请求完成的提示", "data": {"foo": "data"}}
        self.write(data)
