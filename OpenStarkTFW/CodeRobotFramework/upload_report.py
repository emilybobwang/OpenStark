#!/usr/bin/env python3
# coding=utf8

import requests
import json
import re
import sys
from xml.etree import cElementTree as TE


class UploadReport(object):
    def __init__(self, project_id='', job_id='', author='彭鹏', token='', test_type='gui'):
        self.get_case_url = 'http://172.20.20.160:8090/api/py/test/token/testCase/list'
        self.update_case_url = 'http://172.20.20.160:8090/api/py/test/token/testCase/update'
        self.test_log_url = 'http://172.20.20.160:8090/api/py/test/token/test/log'
        # self.get_case_url = 'http://localhost:8000/api/py/test/token/testCase/list'
        # self.update_case_url = 'http://localhost:8000/api/py/test/token/testCase/update'
        # self.test_log_url = 'http://localhost:8000/api/py/test/token/test/log'
        self.project_id = project_id
        self.job_id = job_id
        self.author = author
        self.token = token
        self.test_type = test_type

    # 获取云平台用例列表
    def get_case_list(self):
        try:
            data = dict(project_id=self.project_id, token=self.token, test_type=self.test_type)
            resp = requests.post(self.get_case_url, json=data,)
            cases = json.loads(resp.text, encoding='utf8')
            if cases['status'] == 'SUCCESS':
                cases = cases['data']
            else:
                print(cases)
                cases = list()
        except Exception as e:
            print('获取测试用例列表出错#{}'.format(e))
            cases = list()
        return cases

    # 生成CRF用例列表
    def create_case(self, case_file):
        cases = self.get_case_list()
        def_cases = ''
        for case in cases:
            def_cases += '''
    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_{case_id}(self):
        """{case_id}_{title}
        用例描述:
        {description}
        ======
        预期结果:
        {expected}
        """
        pass
        '''.format(**dict(case_id=case['case_id'] or 'edit_this_case_id', title=case['title'].replace('\n', ''), description=case['description'].replace('\n', '\n\t\t'), expected=case['expected'].replace('\n', '\n\t\t'))) 
        case_text = '''#!/usr/bin/env python3
# coding=utf8

import unittest


class TestCase(unittest.TestCase):
    """请修改这里的测试套件(用例组合)说明"""
    # 用例执行过滤标签, 只执行已标记该标签的用例
    tag = 'run'
    
    @classmethod
    def setUpClass(cls):
        # 测试套件setUp, 执行所有用例前执行一次
        pass

    @classmethod
    def tearDownClass(cls):
        # 测试套件tearDown, 执行完所有用例后执行一次
        pass

    def setUp(self):
        # 测试用例setUp, 执行每个用例前执行一次
        pass

    def tearDown(self):
        # 测试用例tearDown, 执行完每个用例后执行一次
        pass
    {}
        '''.format(def_cases)
        with open(case_file, 'wb') as fp:
            fp.write(case_text.encode('utf8'))
        print('生成CRF用例列表成功, 保存在文件{}中'.format(case_file))

    # 更新单条测试用例
    def update_case(self, data):
        print('更新单条测试用例: {}'.format(json.dumps(data, ensure_ascii=False)))
        try:
            resp = requests.post(self.update_case_url, json=data)
            print(resp.text)
            if json.loads(resp.text)['status'] == 'FAIL':
                raise Exception('更新失败')
        except Exception as e:
            print('更新单条测试用例出错#{}'.format(e))
 
    # 从测试结果文件中获取测试用例及测试结果
    def get_result_case(self, result_file):
        doc_tree = TE.parse(result_file)
        root = doc_tree.getroot()
        cases = []
        for suite in root.iter('testsuite'):
            suite_name = suite.get('name')
            for test in suite.iter('testcase'):
                suite_path = test.get('classname')
                test_name = test.get('name').strip()
                test_func = test.get('function')
                status = test.get('status')
                if status == 'SKIP':
                    continue
                actual_result = '{}\n'.format(test.find('failure').get('message')) if test.find('failure') is not None else ''
                actual_result += '{}\n'.format(test.find('failure').text) if test.find('failure') is not None else ''
                actual_result += '{}\n'.format(test.find('error').get('message')) if test.find('error') is not None else ''
                actual_result += '{}'.format(test.find('error').text) if test.find('error') is not None else ''
                
                starttime = test.get('starttime')
                endtime = test.get('stoptime')
                log_time = test.get('time')
                detail_step = test.find('step').get('message').replace('用例描述:', '').strip()
                expect_result = test.find('expected').get('message').replace('预期结果:', '').strip()
                if re.match(r'^\w+', test_name) is not None:
                    name = test_name.split('_', 1)
                    test_code = name[0] if len(test_name.split('_')) > 2 else ''
                    test_name = name[1] if test_code else test_name
                else:
                    test_code = ''
                code = test_func.split('.')[-1].split('_', 1)[1] if len(test_func.split('.')[-1].split('_', 1)) > 1 else test_func.split('.')[-1].split('_', 1)[0]
                case = dict(suite=suite_path, suite_name=suite_name, case_id=test_code or code, title=test_name, test_func=test_func,
                    status=status.lower(), log_time=log_time, test_startTime=starttime[:-3], test_endTime=endtime[:-3], 
                    description=detail_step, expected=expect_result, actual=actual_result or '实际与预期一致')
                cases.append(case)
        return cases

    # 上传测试结果
    def upload_result(self, result):
        for case in result:
            data = dict(job_id=self.job_id, executor=self.author, case_title=case['title'],
                test_description='测试套件: {}\n测试类: {}\n测试方法: {}'.format(case['suite_name'], case['suite'], case['test_func']),
                case_id=case['case_id'], token=self.token, test_type=self.test_type, test_start_time=case['test_startTime'], test_end_time=case['test_endTime'],
                test_details=[dict(title='', url='', method='', status='', request_headers='', request_body='', response_headers='', response_body='', description='', 
                start_time=case['test_startTime'], end_time=case['test_endTime'])], test_result=case['status'], actual=case['actual'])
            print('上传测试结果: {}'.format(json.dumps(data, ensure_ascii=False)))
            try:
                resp = requests.post(self.test_log_url, json=data)
                print(resp.text)
                if json.loads(resp.text)['status'] == 'FAIL':
                    raise Exception('上传测试结果失败')
            except Exception as e:
                print('上传测试结果出错#{}'.format(e))

    # 检查是否需要更新用例, 用例标题、编号、状态或实际结果是否变更
    def check_case(self, result):
        cases = self.get_case_list()
        update_case = []
        case_ids = []
        for case in result:
            if len(cases) == 0:
                update_case = result
                break
            for row in cases:
                if case['case_id'] == row['case_id'] and case['title'] != row['title']:
                    update_case.append(case)
                elif case['case_id'] == row['case_id'] and case['title'] == row['title'] and row['status'] != '已实现':
                    update_case.append(case)
                elif case['case_id'] == row['case_id'] and case['title'] == row['title'] and case['test_func'] != row['function']:
                    update_case.append(case)
                case_ids.append(row['case_id'])
        for case in result:
            for row in cases:
                if case['case_id'] not in case_ids and case not in update_case:
                    update_case.append(case)
        for case in update_case:
            data = dict(project_id=self.project_id, case_id=case['case_id'], token=self.token, function=case['test_func'], details=[dict(
                title='', url='', method='', request_headers='', request_body='', description='')],
                title=case['title'], author=self.author, executor=self.author, test_type=self.test_type, module='会员中心',
                description=case['description'].replace('         ', '\n'), expected=case['expected'].replace('         ', '\n'), status='已实现')
            self.update_case(data)


def main():
    project_id = '128'    # 测试用例项目编码
    job_id = '41fd6d98-bca6-11e8-9c6a-f44d3016f44c'    # 测试任务ID 0c44b837-d6f5-11e6-a18d-000c29874a1a 为每日构建测试
    author = '彭鹏'
    token = '634756755A33426C626D644165476C6862323570645459324C6D4E7662513D3D'
    case_file = 'TestCase/CaseList.py'    # 从测试管理平台获取用例生成CRF用例保存文件路径
    result_file = 'Results/output.xml'    # CRF测试结果xml文件路径

    argv = sys.argv
    project_id = argv[1] if len(argv) > 1 else project_id
    job_id = argv[2] if len(argv) > 2 else job_id
    author = argv[3] if len(argv) > 3 else author

    ur = UploadReport(project_id=project_id, job_id=job_id, author=author, token=token, test_type='api')
    # 生成CRF用例列表
    ur.create_case(case_file)
    # 上传测试结果
    cases = ur.get_result_case(result_file)  
    ur.upload_result(cases)
    # 检查是否需要更新用例
    ur.check_case(cases)


if __name__ == '__main__':
    main()
