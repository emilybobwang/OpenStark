from tornado.websocket import WebSocketHandler
from tornado.log import app_log as log
from tornado.options import options
from tornado.web import escape
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import os


class WeblogsHandler(WebSocketHandler):
    executor = ThreadPoolExecutor()

    def prepare(self):
        self.file = options.log_file_prefix
        self.flag = False
        self.fp = None
        self.offset = 0

    def check_origin(self, origin):
        return True

    # 实时获取log日志并输出
    def open(self):
        log.info('建立WebSocket连接, 开始处理日志文件')
        if self.file is not None and os.path.isfile(self.file):
            self.fp = open(self.file, 'r')
            self.flag = True

    @gen.coroutine
    def on_message(self, message):
        log.info('收到消息: {}'.format(message))
        if message == 'get_logs':
            try:
                while self.flag:
                    if self.file is None:
                        message = '无法读取日志文件或日志文件不存在, 请联系管理员处理, 可能在启动命令中没有加--log_file_prefix参数指定日志路径'
                        self.write_message(message)
                        self.flag = False
                    else:
                        lines = yield self.__send_logs()
                        for msg in lines:
                            self.write_message(msg)
                        yield gen.sleep(1)
            except Exception as e:
                self.flag = False
                self.close()
                log.error(e)

    def on_close(self):
        log.info('WebSocket连接已关闭, 关闭日志文件')
        self.flag = False
        if self.fp is not None:
            self.fp.close()

    @run_on_executor
    def __send_logs(self):
        self.fp.seek(self.offset, 0)
        lines = self.fp.readlines()
        if lines:
            if self.offset == 0:
                lines = lines if len(lines) < 20 else lines[-20:]
            for i in range(len(lines)):
                lines[i] = escape.xhtml_escape(lines[i])
            self.offset = self.fp.tell()
        return lines or list()
