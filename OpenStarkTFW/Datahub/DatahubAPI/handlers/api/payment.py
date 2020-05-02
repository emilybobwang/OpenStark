from handlers.common import BaseHandler
from tornado import gen
from tornado.web import app_log as log
from handlers.common import AddLogs
from xml.etree import cElementTree as ET
import time
import random
import json


"""
支付系统接口
"""


# 快钱、宝付协议支付接口
class PaymentHandler(BaseHandler):
    def prepare(self):
        super(PaymentHandler, self).prepare()
        self.namespace = '{http://www.99bill.com/mas_cnp_merchant_interface}'

    @gen.coroutine
    def post(self, channel=None, service=None):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        if channel == 'bill99':
            yield self.__bill99(service)
        elif channel == 'baofoo':
            yield self.__baofoo(service)
        else:
            self.write_json(dict(status='FAIL', message='参数不正确!'))

    @gen.coroutine
    def __bill99(self, service):
        data = yield self.get_request_body_to_xml()
        msg = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <MasMessage xmlns="{}">  
            <version>1.0</version>  
            <ErrorMsgContent>   
                <errorCode>B5</errorCode>
                <errorMessage>系统维护中，请稍后再试 </errorMessage> 
            </ErrorMsgContent> 
        </MasMessage> 
        '''.format(self.namespace[1:-1])
        log.info('{}# 请求收到: {}'.format(service, ET.tostring(data).decode('utf8')))
        if data:
            if service == 'ind_auth':
                msg = yield self.__ind_auth(data)
            elif service == 'ind_auth_verify':
                msg = yield self.__ind_auth_verify(data)
            elif service == 'purchase':
                msg = yield self.__purchase(data)
            elif service == 'query_txn':
                msg = yield self.__query_txn(data)
            elif service == 'query_cardinfo':
                msg = yield self.__query_cardinfo(data)
            elif service == 'pci_query':
                msg = yield self.__pci_query(data)
            elif service == 'pci_del':
                msg = yield self.__pci_del(data)
            log.info('{}# 响应返回: {}'.format(service, msg))
        self.write_xml(msg)

    @gen.coroutine
    def __pci_query(self, data):
        content = data.find(self.namespace + 'PciQueryContent')
        merchant_id = content.find(self.namespace + 'merchantId').text
        customer_id = content.find(self.namespace + 'customerId').text
        card_type = content.find(self.namespace + 'cardType').text
        auth, total = yield self.logs.get_logs_list(s_type='auth', name=customer_id,
                                                    search=merchant_id or customer_id, order_by=['s.createTime DESC'])
        desc = dict()
        if auth: desc = json.loads(auth[0].value)
        msg = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<MasMessage xmlns="{}">  
    <PciQueryContent>
        <merchantId>{}</merchantId>
        <customerId>{}</customerId>
        <storablePan>{}</storablePan>
        <cardType>{}</cardType>
        <pciInfos>
            <pciInfo>
                <bankId>CMB</bankId>
                <storablePan>{}</storablePan>
                <shortPhoneNo>{}</shortPhoneNo>
                <phoneNO>{}</phoneNO>
                <payToken>{}</payToken>
            </pciInfo>
        </pciInfos>
        <responseCode>00</responseCode>
    </PciQueryContent>
</MasMessage>
        '''.format(self.namespace[1:-1], merchant_id, customer_id, desc.get('storablePan'), card_type,
                   desc.get('storablePan'), (desc.get('phoneNO') or '')[:8], desc.get('phoneNO'), desc.get('payToken'))
        return msg

    @gen.coroutine
    def __pci_del(self, data):
        content = data.find(self.namespace + 'PciDeleteContent')
        merchant_id = content.find(self.namespace + 'merchantId').text
        customer_id = content.find(self.namespace + 'customerId').text
        pay_token = content.find(self.namespace + 'payToken').text
        bank_id = content.find(self.namespace + 'bankId').text
        msg = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?> 
<MasMessage xmlns="{}">  
    <version>1.0</version> 
    <PciDeleteContent>
        <merchantId>{}</merchantId>
        <customerId>{}</customerId>
        <bankId>{}</bankId>
        <responseCode>00</responseCode>
        <payToken>{}</payToken>
    </PciDeleteContent> 
</MasMessage>
        '''.format(self.namespace[1:-1], merchant_id, customer_id, bank_id, pay_token)
        auth, total = yield self.logs.get_logs_list(s_type='auth', name=customer_id, search=pay_token or customer_id or merchant_id)
        if auth: yield self.logs.delete_logs(sid=auth[0].id)
        return msg

    @gen.coroutine
    def __query_cardinfo(self, data):
        content = data.find(self.namespace + 'QryCardContent')
        txn_type = content.find(self.namespace + 'txnType').text
        card_no = content.find(self.namespace + 'cardNo').text
        msg = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?> 
<MasMessage xmlns="{}">  
    <version>1.0</version> 
    <CardInfoContent>   
        <validFlag>{}</validFlag>
    </CardInfoContent> 
    <QryCardContent>
        <cardType>{}</cardType>
        <cardNo>{}</cardNo>
    </QryCardContent> 
</MasMessage>
        '''.format(self.namespace[1:-1], random.choice(['1', '2']), txn_type, card_no)
        return msg

    @gen.coroutine
    def __query_txn(self, data):
        content = data.find(self.namespace + 'QryTxnMsgContent')
        merchant_id = content.find(self.namespace + 'merchantId').text
        external_ref_number = content.find(self.namespace + 'externalRefNumber')
        external_ref_number = external_ref_number.text if external_ref_number is not None else ''
        ref_number = content.find(self.namespace + 'refNumber')
        ref_number = ref_number.text if ref_number is not None else ''
        txn, total = yield self.logs.get_logs_list(s_type='txn', name=external_ref_number or ref_number, search=external_ref_number or ref_number or merchant_id)
        if txn:
            desc = json.loads(txn[0].value)
            msg_data = '''    <QryTxnMsgContent>
        <externalRefNumber>{}</externalRefNumber>
        <txnType>{}</txnType>
        <merchantId>{}</merchantId>
        <terminalId>{}</terminalId>
    </QryTxnMsgContent>
    <TxnMsgContent>
        <txnType>{}</txnType>
        <amount>{}</amount>
        <merchantId>{}</merchantId>
        <terminalId>{}</terminalId>
        <entryTime>{}</entryTime>
        <externalRefNumber>{}</externalRefNumber>
        <customerId>{}</customerId>
        <transTime>{}</transTime>
        <voidFlag>{}</voidFlag>
        <refNumber>{}</refNumber>
        <responseCode>00</responseCode>
        <responseTextMessage>查询成功</responseTextMessage>
        <cardOrg>CMB</cardOrg>
        <issuer>招商银行</issuer>
        <storableCardNo>62258878</storableCardNo>
        <authorizationCode>{}</authorizationCode>
        <txnStatus>{}</txnStatus>
    </TxnMsgContent>'''.format(desc.get('externalRefNumber'), desc.get('txnType'), desc.get('merchantId'), desc.get('terminalId'),
                       desc.get('txnType'), desc.get('amount'), desc.get('merchantId'), desc.get('terminalId'),
                       desc.get('entryTime'), desc.get('externalRefNumber'), desc.get('customerId'), desc.get('transTime'),
                       desc.get('voidFlag'), desc.get('refNumber'), desc.get('authorizationCode'), desc.get('txnStatus'))
        else:
            msg_data = '''    <ErrorMsgContent>   
        <errorCode>2000</errorCode>
        <errorMessage>交易不存在</errorMessage>
    </ErrorMsgContent> 
            '''
        msg = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?> 
<MasMessage xmlns="{}">  
    <version>1.0</version>  
    {}
</MasMessage> 
        '''.format(self.namespace[1:-1], msg_data)
        return msg

    @gen.coroutine
    def __purchase(self, data):
        content = data.find(self.namespace + 'TxnMsgContent')
        txn_type = content.find(self.namespace + 'txnType').text
        interactive_status = content.find(self.namespace + 'interactiveStatus').text
        interactive_status = 'TR2' if interactive_status == 'TR1' else 'TR4'
        amount = content.find(self.namespace + 'amount').text
        merchant_id = content.find(self.namespace + 'merchantId').text
        terminal_id = content.find(self.namespace + 'terminalId').text
        entry_time = content.find(self.namespace + 'entryTime').text
        external_ref_number = content.find(self.namespace + 'externalRefNumber').text
        customer_id = content.find(self.namespace + 'customerId').text
        pay_token = content.find(self.namespace + 'payToken').text
        tr3_url = content.find(self.namespace + 'tr3Url')
        tr3_url = tr3_url.text if tr3_url is not None else ''
        storable_card_no = content.find(self.namespace + 'storableCardNo')
        storable_card_no = storable_card_no and storable_card_no.text or ''
        ref_number = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
        authorizationCode = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 6))
        trans_time = time.strftime('%Y%m%d%H%M%S')
        if int(float(amount)) == 123 or int(float(amount)) == 120:
            txn_status = 'F'
            response_code = '12'
            response_text_message = '充值失败'
        elif int(float(amount)) == 223 or int(float(amount)) == 220:
            txn_status = 'P'
            response_code = 'C0'
            response_text_message = '交易请求处理中，稍后通知处理结果'
        elif int(float(amount)) == 323 or int(float(amount)) == 320:
            txn_status = 'P'
            response_code = '68'
            response_text_message = '无法在正常时间内获得交易应答，请稍后重试'
        elif int(float(amount)) == 423 or int(float(amount)) == 420:
            txn_status = 'F'
            response_code = '96'
            response_text_message = '系统异常、失效，请联系快钱'
        else:
            txn_status = 'S'
            response_code = '00'
            response_text_message = '充值成功'
        msg = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?> 
<MasMessage xmlns="{}">  
    <version>1.0</version>  
    <TxnMsgContent>   
        <txnType>{}</txnType>
        <interactiveStatus>{}</interactiveStatus> 
        <amount>{}</amount>
        <merchantId>{}</merchantId>
        <terminalId>{}</terminalId>
        <entryTime>{}</entryTime>
        <externalRefNumber>{}</externalRefNumber>
        <customerId>{}</customerId>
        <transTime>{}</transTime>
        <refNumber>{}</refNumber>
        <responseCode>{}</responseCode>
        <responseTextMessage>{}</responseTextMessage>
        <storableCardNo>{}</storableCardNo>
        <payToken>{}</payToken>   
        <authorizationCode>{}</authorizationCode>
    </TxnMsgContent> 
</MasMessage>
        '''.format(self.namespace[1:-1], txn_type, interactive_status, amount, merchant_id, terminal_id, entry_time,
                   external_ref_number, customer_id, trans_time, ref_number, response_code, response_text_message,
                   storable_card_no, pay_token, authorizationCode)
        bill99 = yield self.project.get_project(p_type='project', name='快钱协议支付')
        if not bill99:
            pid, ret_msg = yield self.project.add_project(p_type='project', name='快钱协议支付')
        else:
            pid = bill99.id
        if int(float(amount)) in [120, 220, 320, 420]: txn_status = 'S'
        value = dict(txnType=txn_type, txnStatus=txn_status, interactiveStatus=interactive_status, amount=amount, merchantId=merchant_id,
                    terminalId=terminal_id, entryTime=entry_time, externalRefNumber=external_ref_number, customerId=customer_id,
                    transTime=trans_time, refNumber=ref_number, responseCode='V2', responseTextMessage='扣款成功待充值', voidFlag='0',
                    storableCardNo=storable_card_no, payToken=pay_token, authorizationCode=authorizationCode, tr3Url=tr3_url)
        yield self.logs.add_log(s_type='txn', pid=pid, name=external_ref_number, value=value)
        return msg

    @gen.coroutine
    def __ind_auth_verify(self, data):
        content = data.find(self.namespace + 'indAuthDynVerifyContent')
        merchant_id = content.find(self.namespace + 'merchantId').text
        customer_id = content.find(self.namespace + 'customerId').text
        external_ref_number = content.find(self.namespace + 'externalRefNumber').text
        storable_pan = content.find(self.namespace + 'pan').text
        auth, total = yield self.logs.get_logs_list(s_type='auth', name=customer_id, search=external_ref_number or merchant_id or customer_id)
        desc = dict()
        if auth: desc = json.loads(auth[0].value)
        msg = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?> 
<MasMessage xmlns="{}">  
    <version>1.0</version> 
    <indAuthDynVerifyContent>   
        <merchantId>{}</merchantId>   
        <customerId>{}</customerId>   
        <externalRefNumber>{}</externalRefNumber>   
        <storablePan>{}</storablePan> 
        <payToken>{}</payToken>   
        <responseCode>00</responseCode>   
        <responseTextMessage>成功</responseTextMessage>  
    </indAuthDynVerifyContent> 
</MasMessage>
        '''.format(self.namespace[1:-1], merchant_id, customer_id, external_ref_number,
                   desc.get('storablePan') or '{}{}'.format(storable_pan[:6], storable_pan[-4:]), desc.get('payToken') or int(time.time() * 1000))
        return msg

    @gen.coroutine
    def __ind_auth(self, data):
        content = data.find(self.namespace + 'indAuthContent')
        merchant_id = content.find(self.namespace + 'merchantId').text
        terminal_id = content.find(self.namespace + 'terminalId').text
        customer_id = content.find(self.namespace + 'customerId').text
        external_ref_number = content.find(self.namespace + 'externalRefNumber').text
        storable_pan = content.find(self.namespace + 'pan').text
        card_holder_name = content.find(self.namespace + 'cardHolderName').text
        card_holder_id = content.find(self.namespace + 'cardHolderId').text
        phone_no = content.find(self.namespace + 'phoneNO').text
        bind_type = content.find(self.namespace + 'bindType').text
        id_type = content.find(self.namespace + 'idType').text
        msg = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?> 
<MasMessage xmlns="{}">  
    <version>1.0</version>  
    <indAuthContent>   
        <merchantId>{}</merchantId>   
        <terminalId>{}</terminalId>   
        <customerId>{}</customerId>   
        <externalRefNumber>{}</externalRefNumber>   
        <storablePan>{}</storablePan>   
        <token>{}</token>   
        <responseCode>00</responseCode>   
        <responseTextMessage>交易成功</responseTextMessage>  
    </indAuthContent> 
</MasMessage> 
        '''.format(self.namespace[1:-1], merchant_id, terminal_id, customer_id, external_ref_number, storable_pan[:10], int(time.time() * 1000))
        bill99 = yield self.project.get_project(p_type='project', name='快钱协议支付')
        if not bill99:
            pid, ret_msg = yield self.project.add_project(p_type='project', name='快钱协议支付')
        else:
            pid = bill99.id
        value = dict(merchantId=merchant_id, terminalId=terminal_id, customerId=customer_id, externalRefNumber=external_ref_number,
                     storablePan='{}{}'.format(storable_pan[:6], storable_pan[-4:]), cardHolderName=card_holder_name, cardHolderId=card_holder_id,
                     phoneNO=phone_no, payToken=int(time.time() * 1000), idType=id_type, bindType=bind_type)
        yield self.logs.add_log(s_type='auth', pid=pid, name=customer_id or external_ref_number, value=value)
        return msg

    @gen.coroutine
    def __baofoo(self, service):
        res_msg = '''<?xml version="1.0" encoding="utf-8"?>
        <string xmlns="http://tempuri.org/">{}</string>
                    '''
        log.info('返回: {}'.format(res_msg))
        self.write_xml(msg=res_msg)