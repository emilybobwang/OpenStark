from modules.logs import LogsModule
from tornado import gen
from tornado.web import app_log
from functions.test_runner import TestRunner
from Crypto.Hash import SHA1
import base64
import json


class JobsMonitor(object):
    def __init__(self):
        self.logs = LogsModule()
        self.test = TestRunner()

    # 异步通知
    @gen.coroutine
    def sync_notice(self):
        logs, total = yield self.logs.get_logs_list(s_type='txn')
        for log in logs:
            desc = json.loads(log.value)
            if desc.get('responseCode') == 'V2' and desc.get('tr3Url'):
                desc['responseCode'] = '00'
                yield self.logs.edit_log(sid=log.id, value=desc)
                body = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<MasMessage xmlns="http://www.99bill.com/mas_cnp_merchant_interface">
	<version>1.0</version>
	<TxnMsgContent>
		<txnType>{}</txnType>
		<interactiveStatus>TR3</interactiveStatus>
		<amount>{}</amount>
		<merchantId>{}</merchantId>
		<terminalId>{}</terminalId>
		<entryTime>{}</entryTime>
		<externalRefNumber>{}</externalRefNumber>
		<transTime>{}</transTime>
		<refNumber>{}</refNumber>
		<responseCode>00</responseCode>
		<cardOrg>CU</cardOrg>
		<storableCardNo>{}</storableCardNo>
		<authorizationCode>{}</authorizationCode>
	</TxnMsgContent>
</MasMessage>'''.format(desc.get('txnType'), desc.get('amount'), desc.get('merchantId'), desc.get('terminalId'), desc.get('entryTime'), desc.get('externalRefNumber'),
                        desc.get('transTime'), desc.get('refNumber'), desc.get('storableCardNo'), desc.get('authorizationCode'))
                signature = base64.b64encode(SHA1.new(body.encode('utf8')).hexdigest().encode('utf8'))
                body = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<MasMessage xmlns="http://www.99bill.com/mas_cnp_merchant_interface">
    <version>1.0</version>
    <TxnMsgContent>
        <txnType>{}</txnType>
        <interactiveStatus>TR3</interactiveStatus>
        <amount>{}</amount>
        <merchantId>{}</merchantId>
        <terminalId>{}</terminalId>
        <entryTime>{}</entryTime>
        <externalRefNumber>{}</externalRefNumber>
        <transTime>{}</transTime>
        <refNumber>{}</refNumber>
        <responseCode>00</responseCode>
        <cardOrg>CU</cardOrg>
        <storableCardNo>{}</storableCardNo>
        <authorizationCode>{}</authorizationCode>
        <signature>{}</signature>
    </TxnMsgContent>
</MasMessage>'''.format(desc.get('txnType'), desc.get('amount'), desc.get('merchantId'),
                        desc.get('terminalId'), desc.get('entryTime'), desc.get('externalRefNumber'),
                        desc.get('transTime'), desc.get('refNumber'), desc.get('storableCardNo'),
                        desc.get('authorizationCode'), signature.decode('utf8'))
                resp = yield self.test.run_test(url=desc.get('tr3Url'), method='POST', headers='Content-Type: text/xml; charset=UTF-8', body=body)
                app_log.info(resp)

def job_monitor():
    job = JobsMonitor()
    job.sync_notice()
