from handlers.common import BaseHandler
from tornado import gen
from tornado.web import app_log as log
from handlers.common import AddLogs
from Crypto.Hash import SHA1, MD5
from functions.custom.des_crypt import DESCrypt
from functions.common import CommonFunction
import time
import uuid
import json


"""
消息系统接口
"""


# 玄武、云信、梦网短信发送接口
class MessagesHandler(BaseHandler):
    @gen.coroutine
    def get(self, channel=None, service=None):
        if channel == 'xuanwu' and service == 'getreport':
            yield self.__xuanwu_mass_report()
        elif channel == 'chuanl' and service == 'query':
            yield self.__chuanl_query()
        else:
            yield self.post(channel=channel, service=service)

    @gen.coroutine
    def post(self, channel=None, service=None):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        if channel == 'yunxin' and service == 'sendMsgByEncrypt':
            yield self.__yunxin()
        elif channel == 'yunxin' and service == 'SendVoiceCode':
            yield self.__yunxin_voice()
        elif channel == 'yunxin' and service == 'IndividualSm':
            yield self.__yunxin_individualSm()
        elif channel == 'xuanwu' and service == 'massSend':
            yield self.__xuanwu()
        elif channel == 'xuanwu' and service in ('mass', 'group'):
            yield self.__xuanwu_mass_group()
        elif channel == 'yuntongxin' and service == 'voice':
            yield self.__yun_tong_xin()
        elif channel == 'mengw' and service == 'singleSend':
            yield self.__single_send()
        elif channel == 'chuanl' and service == 'smsSend':
            yield self.__chuanl()
        else:
            self.write_json(dict(status='FAIL', message='参数不正确!'))

    @gen.coroutine
    def __yun_tong_xin(self):
        data = yield self.get_request_body_to_json()
        log.info('收到请求: {}'.format(data))
        log.info('请求头: {}'.format(self.request.headers))
        if data and 'subject' in data.keys():
            mobile = data.subject.get('called') or ''
            if mobile.endswith('0001'):
                code = '9001'
                msg = '其他错误'
            elif mobile.endswith('0002'):
                code = '2001'
                msg = '无效的用户账号'
            elif mobile.endswith('0003'):
                code = '3005'
                msg = '不存在有效的应用'
            else:
                code = '0'
                msg = 'success'
        else:
            code = '1000'
            msg = '服务方法的参数非法'
        if 'Authorization' not in self.request.headers or not self.request.headers['Authorization']:
            code = '1008'
            msg = '请求包头Authorization参数为空'
        if code == '0':
            res_msg = dict(result=dict(code=code, description=msg), info=dict(
                appID=data and (data.get('info') or {}).get('appID'), callID=str(uuid.uuid1()), sessionID=str(uuid.uuid1())),
                           subject=data and data.get('subject'), data=data and data.get('data'), timestamp=int(time.time()*1000))
        else:
            res_msg = dict(result=dict(code=code, description=msg), info=data and data.get('info'),
                           subject=data and data.get('subject'), timestamp=int(time.time()*1000))
        log.info('返回: {}'.format(res_msg))
        self.write_json(res_msg)

    @gen.coroutine
    def __xuanwu(self):
        data = yield self.get_request_body_to_json()
        log.info('收到请求: {}'.format(data))
        if data and len(data.get('items') or []) > 0:
            mobile = data.get('items')[0].get('to') or ''
            if mobile.endswith('0001'):
                code = '1'
                msg = '消息过期'
            elif mobile.endswith('0002'):
                code = '2'
                msg = '下发失败'
            elif mobile.endswith('0003'):
                code = '3'
                msg = '拒绝接收'
            elif mobile.endswith('0004'):
                code = '4'
                msg = '未知错误'
            elif mobile.endswith('0005'):
                code = '5'
                msg = '消息被删除'
            else:
                code = '0'
                msg = '成功'
        else:
            code = '1000'
            msg = '无效请求参数: to不能为空'
        if code == '0':
            res_msg = dict(code=code, msg=msg, uuid=str(uuid.uuid1()))
        else:
            res_msg = dict(code=code, msg=msg)
        log.info('返回: {}'.format(res_msg))
        self.write_json(res_msg)

    @gen.coroutine
    def __xuanwu_mass_report(self):
        pagesize = int(self.get_argument('pagesize', 500))
        sms, total = yield self.logs.get_logs_list(s_type='xuanwu', limit=pagesize>500 and 500 or pagesize)
        data = list()
        for m in sms:
            desc = json.loads(m.value)
            data.append({
                "id": m.id,
                "batchID": desc.get('batchName'),
                "phone": m.name,
                "msgID": m.id,
                "customMsgID": desc.get('customMsgID'),
                "state": 0,
                "total": total,
                "number": 1,
                "submitTime": desc.get('submitTime'),
                "doneTime": time.strftime('%Y-%m-%dT%H:%M:%S'),
                "originResult": "ok",
                "reserve": ""
            })
        self.write_json(data)

    @gen.coroutine
    def __xuanwu_mass_group(self):
        data = yield self.get_request_body_to_json()
        log.info('收到请求: {}'.format(data))
        if data and len(data.get('items') or []) > 0:
            mobile = data.get('items')[0].get('to') or '0002'
            if mobile.endswith('0001'):
                code = '-1'
                msg = '账号无效'
            elif mobile.endswith('0002'):
                code = '-2'
                msg = '参数：无效'
            elif mobile.endswith('0003'):
                code = '-3'
                msg = '连接不上服务器'
            elif mobile.endswith('0006'):
                code = '-6'
                msg = '用户名密码错误'
            elif mobile.endswith('0007'):
                code = '-7'
                msg = '旧密码不正确'
            elif mobile.endswith('0009'):
                code = '-9'
                msg = '资金账户不存在'
            elif mobile.endswith('0011'):
                code = '-11'
                msg = '包号码数量超过最大限制'
            elif mobile.endswith('0012'):
                code = '-12'
                msg = '余额不足'
            elif mobile.endswith('0013'):
                code = '-13'
                msg = '账号没有发送权限'
            elif mobile.endswith('0099'):
                code = '-99'
                msg = '系统内部错误'
            elif mobile.endswith('0100'):
                code = '-100'
                msg = '其它错误'
            elif mobile.endswith('0200'):
                code = '-200'
                msg = '网络问题'
            else:
                code = '0'
                msg = '成功'
                xw = yield self.project.get_project(p_type='project', name='玄武短信')
                if not xw:
                    pid, ret_msg = yield self.project.add_project(p_type='project', name='玄武短信')
                else:
                    pid = xw.id
                for item in data.get('items'):
                    value = dict(batchName=data.get('batchName'), customMsgID=item.get('customMsgID'), submitTime=time.strftime('%Y-%m-%dT%H:%M:%S'))
                    yield self.logs.add_log(s_type='xuanwu', pid=pid, name=item.get('to'), value=value)
        else:
            code = '1000'
            msg = '无效请求参数: to不能为空'
        if code == '0':
            res_msg = dict(code=code, msg=msg, uuid=str(uuid.uuid1()))
        else:
            res_msg = dict(code=code, msg=msg)
        log.info('返回: {}'.format(res_msg))
        self.write_json(res_msg)

    @gen.coroutine
    def __yunxin(self):
        user_code = self.get_argument('userCode', '')
        submit_info = self.get_argument('submitInfo', '')
        log.info(dict(userCode=user_code, submitInfo=submit_info))
        user_code_list = dict(xnzxyz='XNZbyz123', xnzxcf='Gaocc123')
        if user_code:
            user_pass = user_code_list[user_code]
            key = SHA1.new(user_pass.encode('utf8')).hexdigest().upper().encode('utf8')[:8]
            obj = DESCrypt(key=key, iv=key, mode='CBC')
            query = obj.des_decode(submit_info, decode='gb2312')
            func = CommonFunction()
            query = func.url_query_decode(query)
            log.info('解密后数据: {}'.format(query))
            mobile = (query.get('DesNo') or '').split(',')[0]
        else:
            mobile = '0001'
        if mobile.endswith('0001'):
            msg = '-1'
        elif mobile.endswith('0003'):
            msg = '-3'
        elif mobile.endswith('0004'):
            msg = '-4'
        elif mobile.endswith('0005'):
            msg = '-5'
        elif mobile.endswith('0007'):
            msg = '-7'
        elif mobile.endswith('0008'):
            msg = '-8'
        elif mobile.endswith('0009'):
            msg = '-9'
        elif mobile.endswith('0010'):
            msg = '-10'
        elif mobile.endswith('0011'):
            msg = '-11'
        elif mobile.endswith('0012'):
            msg = '-12'
        elif mobile.endswith('0013'):
            msg = '-13'
        elif mobile.endswith('0014'):
            msg = '-14'
        elif mobile.endswith('0015'):
            msg = '-15'
        elif mobile.endswith('0016'):
            msg = '-16'
        elif mobile.endswith('0017'):
            msg = '-17'
        elif mobile.endswith('0023'):
            msg = '-23'
        else:
            msg = int(time.time() * 1000000)
        res_msg = '''<?xml version="1.0" encoding="utf-8"?>
        <string xmlns="http://tempuri.org/">{}</string>
                    '''.format(msg)
        self.set_header("Content-Type", "text/xml; charset=UTF-8")
        log.info('返回: {}'.format(res_msg))
        self.finish(res_msg)

    @gen.coroutine
    def __yunxin_voice(self):
        user_code = self.get_argument('userCode', '')
        mobile = self.get_argument('DesNo', '13500000009')
        log.info(dict(userCode=user_code, DesNo=mobile))
        user_code_list = dict(xnzxyz='XNZbyz123', xnzxcf='Gaocc123')
        if mobile.endswith('0001'):
            msg = '-1'
        elif mobile.endswith('0003'):
            msg = '-3'
        elif mobile.endswith('0004'):
            msg = '-4'
        elif mobile.endswith('0005'):
            msg = '-5'
        elif mobile.endswith('0007'):
            msg = '-7'
        elif mobile.endswith('0008'):
            msg = '-8'
        elif mobile.endswith('0009'):
            msg = '-9'
        elif mobile.endswith('0010'):
            msg = '-10'
        elif mobile.endswith('0011'):
            msg = '-11'
        elif mobile.endswith('0012'):
            msg = '-12'
        elif mobile.endswith('0013'):
            msg = '-13'
        elif mobile.endswith('0014'):
            msg = '-14'
        elif mobile.endswith('0015'):
            msg = '-15'
        elif mobile.endswith('0016'):
            msg = '-16'
        elif mobile.endswith('0017'):
            msg = '-17'
        elif mobile.endswith('0023'):
            msg = '-23'
        else:
            msg = int(time.time() * 1000000)
        res_msg = '''<?xml version="1.0" encoding="utf-8"?>
        <string xmlns="http://tempuri.org/">{}</string>
                    '''.format(msg)
        self.set_header("Content-Type", "text/xml; charset=UTF-8")
        log.info('返回: {}'.format(res_msg))
        self.finish(res_msg)

    @gen.coroutine
    def __yunxin_individualSm(self):
        msgs = self.get_argument('msg', '')
        msg = msgs.split('|^|')
        mobile = msg and msg[0].split('|!|')
        mobile = mobile and mobile[0] or ''
        log.info(dict(msgs=msgs, mobile=mobile))
        if mobile.endswith('0001'):
            msg = '-1'
        elif mobile.endswith('0003'):
            msg = '-3'
        elif mobile.endswith('0005'):
            msg = '-5'
        elif mobile.endswith('0006'):
            msg = '-6:促销'
        elif mobile.endswith('0007'):
            msg = '-7'
        elif mobile.endswith('0008'):
            msg = '-8'
        elif mobile.endswith('0009'):
            msg = '-9'
        elif mobile.endswith('0010'):
            msg = '-10'
        elif mobile.endswith('0011'):
            msg = '-11'
        else:
            msg = int(time.time() * 1000000)
        res_msg = '''<?xml version="1.0" encoding="utf-8"?>
        <string xmlns="http://tempuri.org/">{}</string>
                    '''.format(msg)
        self.set_header("Content-Type", "text/xml; charset=UTF-8")
        log.info('返回: {}'.format(res_msg))
        self.finish(res_msg)

    @gen.coroutine
    def __single_send(self):
        data = yield self.get_request_body_to_json()
        if not data:
            mobile = self.get_argument('mobile', '13500000012')
            custid = self.get_argument('custid', MD5.new(str(time.time()).encode('utf8')).hexdigest())
        else:
            mobile = data.get('mobile')
            custid = data.get('custid')
        log.info('梦网短信#收到请求参数: {}'.format(dict(mobile=mobile, custid=custid)))
        if mobile.endswith('0001'):
            result = -100001
        elif mobile.endswith('0002'):
            result = -100002
        elif mobile.endswith('0003'):
            result = -100003
        elif mobile.endswith('0004'):
            result = -100004
        elif mobile.endswith('0011'):
            result = -100011
        elif mobile.endswith('0012'):
            result = -100012
        elif mobile.endswith('0014'):
            result = -100014
        elif mobile.endswith('0029'):
            result = -100029
        elif mobile.endswith('0056'):
            result = -100056
        elif mobile.endswith('0057'):
            result = -100057
        elif mobile.endswith('0126'):
            result = -100126
        elif mobile.endswith('0252'):
            result = -100252
        elif mobile.endswith('0253'):
            result = -100253
        elif mobile.endswith('0999'):
            result = -100999
        else:
            result = 0
        res_msg = dict(result=result, msgid=0 if result else int(time.time() * 1000000) , custid='' if result else custid)
        self.write_json(res_msg)

    @gen.coroutine
    def __chuanl(self):
        msgs = self.get_argument('mobile', '')
        if not msgs: 
            body = self.request.body.decode('utf8')
            for m in body.split('&'):
                m = m.split('=')
                if m[0] == 'mobile':
                    msgs = len(m) > 1 and m[1] or ''
                    break
        msgs = msgs.split(',')
        mobile = msgs and msgs[0] or '0004'
        status = 'Faild'
        task_id = int(time.time() * 1000000)
        if mobile.endswith('0001'):
            msg = '用户名或密码不能为空'
        elif mobile.endswith('0002'):
            msg = '发送内容包含sql注入字符'
        elif mobile.endswith('0003'):
            msg = '用户名或密码错误'
        elif mobile.endswith('0004'):
            msg = '短信号码不能为空'
        elif mobile.endswith('0005'):
            msg = '短信内容不能为空'
        elif mobile.endswith('0006'):
            msg = '包含非法字符'
        elif mobile.endswith('0007'):
            msg = '对不起，您当前要发送的量大于您当前余额'
        elif mobile.endswith('0008'):
            msg = '其他错误'
        else:
            msg = 'ok'
            status = 'Success'
            cl = yield self.project.get_project(p_type='project', name='川凌短信')
            if not cl:
                pid, ret_msg = yield self.project.add_project(p_type='project', name='川凌短信')
            else:
                pid = cl.id
            for item in msgs:
                value = dict(status=10, mobile=item, receivetime=time.strftime('%Y-%m-%dT%H:%M:%S'))
                yield self.logs.add_log(s_type='chuanl', pid=pid, name=task_id, value=value)
        res_msg = '''<?xml version="1.0" encoding="utf-8" ?>
<returnsms>
    <returnstatus>{}</returnstatus>
    <message>{}</message>
    <remainpoint>1000.00</remainpoint>
    <taskID>{}</taskID>
    <successCounts>{}</successCounts>
</returnsms>
'''.format(status, msg, task_id, status == 'Success' and len(msgs) or 0)
        self.write_xml(res_msg)
        
    @gen.coroutine
    def __chuanl_query(self):
        statusNum = int(self.get_argument('statusNum', 4000))
        sms, total = yield self.logs.get_logs_list(s_type='chuanl', limit=statusNum>4000 and 4000 or statusNum)
        msg = ''
        for m in sms:
            desc = json.loads(m.value)
            msg += '''
    <statusbox>
        <mobile>{}</mobile>
        <taskid>{}</taskid>
        <status>{}</status>
        <receivetime>{}</receivetime>
        <errorcode>0</errorcode>
        <extno></extno>
    </statusbox>
            '''.format(desc.get('mobile'), m.name, desc.get('status'), desc.get('receivetime'))
        res_msg = '''<?xml version="1.0" encoding="utf-8" ?> 
<returnsms>
    {}
</returnsms>
'''.format(msg or ('''<errorstatus>
<error>5</error>
<remark>没有记录</remark>
</errorstatus>
'''))
        self.write_xml(res_msg)