from handlers.common import BaseHandler
from functions.common import CommonFunction
from tornado import gen
from tornado.web import app_log as log
from settings import static_path
import json
import time
import os


#应急处理中心挡板接口
class Ifcert(BaseHandler):
    @gen.coroutine
    def get(self, op=None):
        data_type = self.get_argument('dataType', None)
        batch_num = self.get_argument('batchNum', None)
        inf_type = self.get_argument('infType', '')
        sent_date = self.get_argument('sentDate', time.strftime('%Y-%m-%d'))
        page_num = int(self.get_argument('pageNum', 1))
        ret_status = self.get_argument('retStatus', None)
        if ret_status:
            with open('STATUS', 'w') as fp:
                fp.write(ret_status)
            return self.write_json(dict(status='SUCCESS', message='已切换返回数据状态为 {}'.format(ret_status)))
        elif os.path.isfile('STATUS'):
            with open('STATUS', 'r') as fp:
                ret_status = fp.read().strip()
        else:
            ret_status = 'success'
        ret_msg = dict(message='[调试]未知错误，请联系中心', code='1506')
        if op == 'batchMessage':
            p2p_data, total = yield self.logs.get_logs_list(
                s_type=inf_type, name=batch_num, status=data_type)
            results = list()
            # if p2p_data and total:
            for d in p2p_data:
                results.append(dict(dataType='正式数据' if d.type == '1' else '测试数据',
                                    batchNum=d.name, errorMsg=ret_status))
            ret_msg = dict(code='0000', message='查询成功!', result=results)
        elif op == 'batchNum':
            p2p_data, total = yield self.logs.get_logs_list(
                s_type=inf_type, status=data_type, create_time=sent_date)
            # if p2p_data and total:
            #     total = 0
            #     for d in p2p_data:
            #         desc = json.loads(d.value)
            #         total += int(desc.get('totalNum', 0))
            ret_msg = dict(code='0000', message='查询成功!', sentDate=sent_date, result=dict(
                dataType='正式数据' if data_type == '1' else '测试数据',
                totalNum=total, successNum=total if ret_status == 'success' else 0, faildlNum=0 if ret_status == 'success' else total))
        elif op == 'batchList':
            p2p_data, total = yield self.logs.get_logs_list(
                s_type=inf_type, status=data_type, create_time=sent_date, page=page_num, limit=3000)
            results = list()
            # if p2p_data and total:
            #     total = 0
            for d in p2p_data:
                # desc = json.loads(d.value)
                # total += int(desc.get('totalNum', 0))
                results.append(d.name)
            ret_msg = dict(code='0000', message='查询成功!', sentDate=sent_date, totalNum=total, result=results)
        else:
            ret_msg = dict(message='[调试]infType和实际调用接口不匹配', code='1502')
        log.info(ret_msg)
        self.write_json(ret_msg)

    @gen.coroutine
    def post(self, op=None):
        data = yield self.get_request_body_to_json()
        if isinstance(data, str):
            data_split = CommonFunction().url_query_decode(data)
            data = json.loads(data_split.get('msg'))
        if (not data) or (not isinstance(data, dict)):
            ret_msg = dict(message='[调试]JSON文件错误或接口异常', code='1200')
        else:
            ret_msg = dict(message='[调试]数据已成功上报，正在等待处理，请使用对账接口查看数据状态。', code='0000')
            pro = yield self.project.get_project(name='互联网应急中心', p_type='project')
            if not pro:
                pid, msg = yield self.project.add_project(name='互联网应急中心', p_type='project')
            else:
                pid = pro.id
            ext_data = yield self.logs.get_log(pid=pid, s_type=data.get('infType'), name=data.get('batchNum'))
            if ext_data:
                ret_msg = dict(message='[调试]该批次已经上传成功，请勿重复上报。', code='1512')
            else:
                json_path = os.path.join(static_path, 'ifcert')
                if not os.path.isdir(json_path):
                    os.makedirs(json_path)
                with open(os.path.join(json_path, '{}.json'.format(data.get('batchNum'))), 'w', encoding='utf8') as fp:
                    fp.write(json.dumps(data, ensure_ascii=False))
                if 'dataList' in data: data.pop('dataList')
                res, msg = yield self.logs.add_log(pid=pid, s_type=data.get('infType'), name=data.get('batchNum'),
                                        value=data, create_time=data.get('sentTime'), status=data.get('dataType'))
                if not res:
                    ret_msg = dict(message='[调试]未知错误，请联系中心', code='1506')
        log.info(ret_msg)
        self.write_json(ret_msg)
