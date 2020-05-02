from tornado import httpclient, gen
from tornado.netutil import Resolver
from tornado.web import escape
from urllib.parse import urlencode, quote
from tornado.httputil import parse_body_arguments
from functions.common import CommonFunction
from modules.logs import LogsModule
from tornado.log import app_log as log
from functions.options import OptionsFunction
import ast
import json
import re


# 测试执行类
class TestRunner(object):
    Resolver.configure('tornado.netutil.ThreadedResolver')

    def __init__(self, pid=0, jid=0):
        self.default_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                                'Cookie': ''}
        self.headers = dict()
        self.setting = LogsModule()
        self.common_func = CommonFunction()
        self.option_func = OptionsFunction()
        self.pid = pid
        self.jid = jid

    # 获取请求头
    def get_headers(self, headers=''):
        flag, headers = self.common_func.convert_to_list_or_dict(string=headers, s_type='dict')
        self.headers = dict()
        for key in self.default_headers:
            self.headers[key] = self.default_headers[key]
        if flag:
            for key in headers.keys():
                self.headers[key] = headers[key]
        else:
            headers = headers.splitlines()
            for header in headers:
                header = header.strip().split(sep=':', maxsplit=1)
                if len(header) == 2:
                    name = header[0].strip()
                    value = header[1].strip()
                    self.headers[name] = value
        return self.headers

    # 加解密操作
    @gen.coroutine
    def __do_crypt(self, do='encrypt', body=None, crypt_key=''):
        crypt_info = yield self.option_func.get_crypt_info(pid=self.pid, do=do)
        if not crypt_info:
            return body
        func = crypt_info.function
        try:
            if func:
                if crypt_key:
                    flag, body = self.common_func.convert_to_list_or_dict(string=body, s_type='dict')
                    if not flag and isinstance(body, str) and re.match(r'^.*=.*(&.*=.*)*$', body) is not None:
                        body = self.common_func.url_query_decode(body)
                        if isinstance(body, dict):
                            flag = True
                    if flag:
                        source = body[crypt_key]
                        if not isinstance(source, str):
                            try:
                                source = json.dumps(source, ensure_ascii=False)
                            except Exception as e:
                                log.warning(e)
                                if isinstance(source, bytes):
                                    source = source.decode('utf8', errors='ignore')
                                else:
                                    source = str(source)
                        body[crypt_key] = func(source, crypt_info['key'], crypt_info['iv'], crypt_info['mode'])
                else:
                    if not isinstance(body, str):
                        try:
                            body = json.dumps(body, ensure_ascii=False)
                        except Exception as e:
                            log.warning(e)
                            if isinstance(body, bytes):
                                body = body.decode('utf8', errors='ignore')
                            else:
                                body = str(body)
                    body = func(body, crypt_info['key'], crypt_info['iv'], crypt_info['mode'])
        except Exception as e:
            log.warning(e)
        return body

    # 尝试将请求数据转换成字典
    def __parse_body_arguments(self, body):
        flag, body = self.common_func.convert_to_list_or_dict(string=body, s_type='dict')
        if not flag and isinstance(body, str) and re.match(r'^.*=.*(&.*=.*)*$', body) is not None:
            body = self.common_func.url_query_decode(body)
            if isinstance(body, dict):
                flag = True
        if not flag:
            self.headers = self.headers if len(self.headers) != 0 else self.default_headers
            try:
                request_body = dict()
                if re.match(r'^.*=.*(&.*=.*)*$', body) is not None:
                    parse_body_arguments(content_type=self.headers['Content-Type'], body=body,
                                         arguments=request_body, files=request_body, headers=self.headers)
                if len(request_body) > 0:
                    body = request_body
                for key in body:
                    if isinstance(body[key], list):
                        body[key] = body[key][0]
                        body[key] = body[key].decode('utf8', errors='ignore')
                flag = True
            except Exception as e:
                log.warning(e)
                flag = False
        return flag, body

    # 获取请求响应数据
    @gen.coroutine
    def __get_body(self, body='', do='encrypt', name='', crypt_key=''):
        try:
            body = ast.literal_eval(body)
        except Exception as e:
            log.warning(e)
            if do == 'encrypt' and crypt_key != '':
                flag, body = self.__parse_body_arguments(body)
        if isinstance(body, dict):
            if name != 'none':
                if do == 'encrypt' and crypt_key == '':
                    body = urlencode(body, encoding='utf8', quote_via=quote)
                body = yield self.__do_crypt(do=do, body=body, crypt_key=crypt_key)
            if isinstance(body, dict):
                if do == 'encrypt' and self.headers['Content-Type'].find('x-www-form-urlencoded') != -1:
                    body = urlencode(body, encoding='utf8', quote_via=quote)
                else:
                    body = json.dumps(body, ensure_ascii=False)
        else:
            if name != 'none':
                body = yield self.__do_crypt(do=do, body=body, crypt_key='')
            if isinstance(body, dict):
                body = json.dumps(body, ensure_ascii=False)
        return body

    # 解析Host配置
    @gen.coroutine
    def __parse_host(self, url='', env='none'):
        urls = self.common_func.url_split(url=url)
        host = urls.host
        ips, total = yield self.setting.get_logs_list(pid=self.pid, s_type='host',
                                                          name=host, pj_status=1, limit=None)
        for row in ips:
            if env != 'none':
                url = '{}://{}:{}{}'.format(urls.scheme, env, urls.port, urls.path)
                break
            elif row.status == 1:
                url = '{}://{}:{}{}'.format(urls.scheme, row.value, urls.port, urls.path)
                break
        self.headers['Host'] = urls.netloc
        return url

    # 解析接口返回值全字段检查配置
    def __parse_check_key(self, check_key):
        keys = []
        top = []
        rex = re.compile(r'^\[\w+=\d\|(int|float|num|str|/.*/|date|time|datetime|list|dict)('
                         r',\w+=\d\|(int|float|num|str|/.*/|date|time|datetime|list|dict))*\]$')
        for row in check_key.splitlines():
            row = row.strip().split(sep='.', maxsplit=1)
            if len(row) == 2:
                if re.match(rex, row[1]) is not None:
                    deeps = [row[1]]
                else:
                    deeps = row[1].split(sep='.', maxsplit=1)
                if re.match(r'^\[\d+\]$', deeps[0]) is None:
                    top.append('{}=1|dict'.format(row[0]))
                else:
                    top.append('{}=1|list'.format(row[0]))
                deep = '{}.'.format(row[0])
                tmp_key = []
                for i in range(len(row[1].split('.'))):
                    if len(deeps) == 2 and re.match(rex, deeps[1]) is not None:
                        deep += '{}.'.format(deeps[0])
                        for j in deeps[1][1:-1].split(','):
                            tmp_key.append(j)
                        break
                    elif re.match(rex, deeps[0]) is not None:
                        for j in deeps[0][1:-1].split(','):
                            tmp_key.append(j)
                        break
                    deep += '{}.'.format(deeps[0])
                    if len(deeps) == 2:
                        if re.match(rex, deeps[1]) is not None:
                            deeps = deeps[1]
                        else:
                            deeps = deeps[1].split(sep='.', maxsplit=1)
                keys.append(dict(deep=deep[:-1], keys=tmp_key, result=dict()))
            else:
                top.append(row[0])
        keys.append(dict(deep='top', keys=list(set(top)), result=dict()))
        return keys

    # 返回值全字段检查结果判断
    def __check_key_result(self, body, check_key, key, k):
        check_key[k]['result'][key[0]] = True
        key[1] = key[1].split(sep='|', maxsplit=1)
        require = key[1][0]
        key_type = key[1][1]
        if isinstance(body[key[0]], str):
            body[key[0]] = body[key[0]].strip()
        if require == '1' and (body[key[0]] == '' or body[key[0]] is None):
            check_key[k]['result'][key[0]] = False
        elif body[key[0]] != '' and body[key[0]] is not None:
            if re.match(r'^/.*/$', key_type):
                rex = re.compile(key_type[1:-1])
                if re.match(rex, body[key[0]]) is None:
                    check_key[k]['result'][key[0]] = False
            elif key_type == 'int' and not isinstance(body[key[0]], int):
                check_key[k]['result'][key[0]] = False
            elif key_type == 'float' and not isinstance(body[key[0]], float):
                check_key[k]['result'][key[0]] = False
            elif key_type == 'num' and not isinstance(body[key[0]], int) and not isinstance(body[key[0]], float):
                check_key[k]['result'][key[0]] = False
            elif key_type == 'str' and not isinstance(body[key[0]], str):
                check_key[k]['result'][key[0]] = False
            elif key_type == 'list' and not isinstance(body[key[0]], list):
                check_key[k]['result'][key[0]] = False
            elif key_type == 'dict' and not isinstance(body[key[0]], dict):
                check_key[k]['result'][key[0]] = False
            elif key_type == 'date' and re.match(r'^\d{4}-\d{2}-\d{2}$', body[key[0]]) is None:
                check_key[k]['result'][key[0]] = False
            elif key_type == 'time' and re.match(r'^\d{2}:\d{2}:\d{2}$', body[key[0]]) is None:
                check_key[k]['result'][key[0]] = False
            elif key_type == 'datetime' and re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$', body[key[0]]) is None:
                check_key[k]['result'][key[0]] = False
        if not check_key[k]['result'][key[0]]:
            check_key[k]['result']['key_result'] = False
        return body, check_key

    # 解析响应内容
    @gen.coroutine
    def __parse_response(self, response, name='', crypt_key='', checkpoint='', check_key='',
                         correlation='', method='GET', url=''):
        body = response.body if response else ''
        request_body = response.request.body if response else ''
        if isinstance(body, bytes):
            body = body.decode('utf8', errors='ignore')
        if isinstance(request_body, bytes):
            request_body = request_body.decode('utf8', errors='ignore')
        headers_dict = dict(response.headers if response else '')
        headers = ''
        for key in headers_dict:
            headers += '{}: {}\r\n'.format(key, headers_dict[key])
        request_headers_dict = dict(response.request.headers if response else '')
        request_headers = ''
        for key in request_headers_dict:
            request_headers += '{}: {}\r\n'.format(key, request_headers_dict[key])
        if response:
            error = response.error if not response.error else str(response.error)
        else:
            error = str(httpclient.HTTPError(599, 'Timeout while connecting'))
        resp = dict(body=body, code=response.code if response else 599,
                    effective_url=response.effective_url if response else '',
                    error=error, headers=headers, request_headers=request_headers, request_body=request_body,
                    reason=response.reason if response else 'Timeout while connecting',
                    request_time=response.request_time if response else '',
                    time_info=response.time_info if response else '', method=method, url=url)
        resp['body_decrypt'] = yield self.__get_body(body, do='decrypt', name=name, crypt_key=crypt_key)
        resp['checkpoint'] = []
        if checkpoint != '':
            if re.match(r'^/.*/$', checkpoint) is not None:
                rex = re.compile(checkpoint[1:-1])
                if re.findall(rex, resp['body_decrypt']):
                    resp['checkpoint'].append(dict(result=True, checkpoint=checkpoint))
                else:
                    log.warning('检查点 {} 检查不通过'.format(checkpoint))
                    resp['checkpoint'].append(dict(result=False, checkpoint=checkpoint))
            else:
                for check in checkpoint.split('|'):
                    check = check.strip()
                    if resp['body_decrypt'].find(check) != -1:
                        resp['checkpoint'].append(dict(result=True, checkpoint=check))
                    else:
                        log.warning('检查点 {} 检查不通过'.format(check))
                        resp['checkpoint'].append(dict(result=False, checkpoint=check))
        resp['check_key'] = []
        if check_key != '':
            check_key = self.__parse_check_key(check_key)
            for k in range(len(check_key)):
                body = resp['body_decrypt']
                check_key[k]['result']['key_result'] = True
                if check_key[k]['deep'] == 'top':
                    for key in check_key[k]['keys']:
                        if re.match(r'^\[\d+\]$', key) is not None:
                            key = int(key[1:-1])
                            flag, body = self.common_func.convert_to_list_or_dict(body, 'list')
                            if not flag:
                                log.warning('返回值全字段检查 被检查数据格式不是List, 无法继续')
                                if body in ['', '[]', '{}', [], {}]:
                                    check_key[k]['result']['ERROR'] = '被检查数据为空'
                                else:
                                    check_key[k]['result']['ERROR'] = '被检查数据类型不是List'
                                check_key[k]['result']['key_result'] = False
                                continue
                            try:
                                body[key]
                            except Exception as e:
                                log.warning(e)
                                check_key[k]['result']['ERROR'] = '被检查数据格式不包含List类型'
                                check_key[k]['result']['key_result'] = False
                                continue
                        else:
                            flag, body = self.common_func.convert_to_list_or_dict(body, 'dict')
                            if not flag and isinstance(body, str) and re.match(r'^.*=.*(&.*=.*)*$', body) is not None:
                                body = self.common_func.url_query_decode(body)
                                if isinstance(body, dict):
                                    flag = True
                            if not flag:
                                log.warning('返回值全字段检查 被检查数据格式不是Dict, 无法继续')
                                if body in ['', '[]', '{}', [], {}]:
                                    check_key[k]['result']['ERROR'] = '被检查数据为空'
                                else:
                                    check_key[k]['result']['ERROR'] = '被检查数据类型不是Dict'
                                check_key[k]['result']['key_result'] = False
                                continue
                            key = key.split(sep='=', maxsplit=1)
                            if key[0] not in body.keys():
                                log.warning('返回值全字段检查 {} 检查不通过'.format(check_key[k]['keys']))
                                check_key[k]['result'][key[0]] = '字段不存在'
                                check_key[k]['result']['key_result'] = False
                                continue
                            else:
                                body, check_key = self.__check_key_result(body=body, check_key=check_key,
                                                                          key=key, k=k)
                else:
                    keys = check_key[k]['keys']
                    flag, keys = self.common_func.convert_to_list_or_dict(keys, 'list')
                    for key in check_key[k]['deep'].split('.'):
                        if re.match(r'^\[\d+\]$', key) is not None:
                            key = int(key[1:-1])
                            flag, body = self.common_func.convert_to_list_or_dict(body, 'list')
                            if not flag:
                                log.warning('返回值全字段检查 被检查数据格式不是List, 无法继续')
                                if body in ['', '[]', '{}', [], {}]:
                                    check_key[k]['result']['ERROR'] = '被检查数据为空'
                                else:
                                    check_key[k]['result']['ERROR'] = '被检查数据类型不是List'
                                check_key[k]['result']['key_result'] = False
                                continue
                        elif not isinstance(body, dict):
                            flag, body = self.common_func.convert_to_list_or_dict(body, 'dict')
                            if not flag and isinstance(body, str) and re.match(r'^.*=.*(&.*=.*)*$', body) is not None:
                                body = self.common_func.url_query_decode(body)
                                if isinstance(body, dict):
                                    flag = True
                            if not flag:
                                log.warning('返回值全字段检查 被检查数据格式不是Dict, 无法继续')
                                if body in ['', '[]', '{}', [], {}]:
                                    check_key[k]['result']['ERROR'] = '被检查数据为空'
                                else:
                                    check_key[k]['result']['ERROR'] = '被检查数据类型不是Dict'
                                check_key[k]['result']['key_result'] = False
                                continue
                        try:
                            body = body[key]
                        except Exception as e:
                            log.warning(e)
                            check_key[k]['result']['ERROR'] = '被检查数据格式不包含List类型'
                            check_key[k]['result']['key_result'] = False
                            continue
                    flag, body = self.common_func.convert_to_list_or_dict(body, 'dict')
                    if not flag and isinstance(body, str) and re.match(r'^.*=.*(&.*=.*)*$', body) is not None:
                        body = self.common_func.url_query_decode(body)
                        if isinstance(body, dict):
                            flag = True
                    if not flag:
                        log.warning('返回值全字段检查 被检查数据格式不是Dict, 无法继续')
                        if body in ['', '[]', '{}', [], {}]:
                            check_key[k]['result']['ERROR'] = '被检查数据为空'
                        else:
                            check_key[k]['result']['ERROR'] = '被检查数据类型不是Dict'
                        check_key[k]['result']['key_result'] = False
                        continue
                    for key in keys:
                        key = key.split(sep='=', maxsplit=1)
                        if key[0] not in body.keys():
                            log.warning('返回值全字段检查 {} 检查不通过'.format(check_key[k]['keys']))
                            check_key[k]['result'][key[0]] = '字段不存在'
                            check_key[k]['result']['key_result'] = False
                            continue
                        else:
                            body, check_key = self.__check_key_result(
                                body=body, check_key=check_key, key=key, k=k)
            resp['check_key'] = check_key
        resp['correlation'] = dict()
        if response and correlation != '':
            correlations = correlation.split('|')
            correlation = dict()
            for corr in correlations:
                body = resp['body_decrypt']
                cor = corr.split(sep='=', maxsplit=1)
                key = cor[0].strip()
                c_type = 'string'
                words = cor[1].strip()
                if re.match(r'^int\(.+\)$', words) is not None:
                    c_type = 1
                    words = words[4:-1]
                elif re.match(r'^float\(.+\)$', words) is not None:
                    c_type = 1.00
                    words = words[6:-1]
                word = words.split('.')
                correlation[key] = word
                for k in word:
                    if k == 'response_headers' and len(word) != 1:
                        header = words.split(sep='.', maxsplit=1)
                        if len(header) == 2:
                            header_key = header[1]
                            if re.match(r'^/.*/$', header_key) is not None:
                                rex = re.compile(header_key[1:-1])
                                if isinstance(resp['headers'], bytes):
                                    resp['headers'] = resp['headers'].decode('utf8', errors='ignore')
                                result = re.findall(rex, resp['headers'])
                                if result:
                                    if isinstance(result[0], tuple):
                                        body = result[0][0]
                                    else:
                                        body = ''
                                        for row in result:
                                            row = row if row != '' else '\n'
                                            body += row
                                else:
                                    body = ''
                            else:
                                body = response.headers.get(header_key)
                            break
                    if k == 'response_body' and len(word) == 1:
                        if isinstance(resp['body'], bytes):
                            resp['body'] = resp['body'].decode('utf8', errors='ignore')
                        body = escape.xhtml_escape(resp['body'])
                        break
                    if re.match(r'^/.*/$', words) is not None:
                        rex = re.compile(words[1:-1])
                        if isinstance(resp['body'], bytes):
                            resp['body'] = resp['body'].decode('utf8', errors='ignore')
                        result = re.findall(rex, resp['body'])
                        if result:
                            if isinstance(result[0], tuple):
                                body = escape.xhtml_escape(result[0][0])
                            else:
                                body = escape.xhtml_escape(result[0])
                        else:
                            body = ''
                        break
                    if re.match(r'^\[\d+\]$', k) is not None:
                        k = int(k[1:-1])
                        flag, body = self.common_func.convert_to_list_or_dict(body, 'list')
                        if not flag:
                            log.warning('响应数据格式不是List, 无法继续')
                            body = ''
                            break
                    elif not isinstance(body, dict):
                        flag, body = self.common_func.convert_to_list_or_dict(body, 'dict')
                        if not flag and isinstance(body, str) and re.match(r'^.*=.*(&.*=.*)*$', body) is not None:
                            body = self.common_func.url_query_decode(body)
                            if isinstance(body, dict):
                                flag = True
                        if not flag:
                            log.warning('响应数据格式不是Dict, 无法继续')
                            body = ''
                            break
                    try:
                        body = body[k]
                    except Exception as e:
                        log.warning(e)
                        body = ''
                        break
                correlation[key] = body
                try:
                    if isinstance(c_type, int):
                        correlation[key] = int(float(re.sub(r'[^\d+\.]', '', body)))
                    elif isinstance(c_type, float):
                        correlation[key] = float(re.sub(r'[^\d+\.]', '', body))
                except Exception as e:
                    log.warning(e)
            resp['correlation'] = correlation
        flag = True
        if resp['error'] is not None and resp['code'] != 302 and resp['code'] != 301:
            flag = False
        if resp['check_key']:
            for line in resp['check_key']:
                if not line['result']['key_result']:
                    flag = False
                    break
        if resp['checkpoint']:
            for line in resp['checkpoint']:
                if not line['result']:
                    flag = False
                    break
        resp['test_result'] = flag
        return resp

    # 解析自定义参数配置
    @gen.coroutine
    def __parse_custom_param(self, headers, body, correlation_result={}):
        correlation_result = dict(self.common_func.default_param(), **correlation_result)
        params = yield self.option_func.get_custom_param(pid=self.pid, correlation=correlation_result)
        if isinstance(headers, bytes):
            headers = headers.decode('utf8', errors='ignore')
        if isinstance(body, bytes):
            body = body.decode('utf8', errors='ignore')
        for key in correlation_result:
            if not isinstance(correlation_result[key], str):
                correlation_result[key] = str(correlation_result[key])
            if headers.find(key) != -1:
                headers = headers.replace(key, correlation_result[key])
            if body.find(key) != -1:
                body = body.replace(key, correlation_result[key])
        for param in params:
            if headers.find('{%s}' % param['name']) != -1:
                if param['type'] == 'Function':
                    func = param['function']
                    flag, body_dict = self.__parse_body_arguments(body)
                    encrypt = yield self.option_func.get_crypt_info(self.pid)
                    headers = headers.replace('{%s}' % param['name'], func(body_dict, params, encrypt))
                else:
                    headers = headers.replace('{%s}' % param['name'], param['value'])
            if body.find('{%s}' % param['name']) != -1:
                if param['type'] == 'Function':
                    func = param['function']
                    flag, body_dict = self.__parse_body_arguments(body)
                    encrypt = yield self.option_func.get_crypt_info(self.pid)
                    body = body.replace('{%s}' % param['name'], func(body_dict, params, encrypt))
                else:
                    body = body.replace('{%s}' % param['name'], param['value'])
        return headers, body

    # 请求操作
    @gen.coroutine
    def __request_url(self, url='', env='none', method='GET', body='', follow_redirects=True):
        test_client = httpclient.AsyncHTTPClient(max_clients=100)
        argv = dict(method=method, headers=self.headers, follow_redirects=False, request_timeout=600,
                    validate_cert=False, raise_error=False)
        url = yield self.__parse_host(url=url, env=env)
        if method == 'GET':
            url = '{}?{}'.format(url, body)
        elif method == 'POST':
            argv['body'] = body
        try:
            log.info('开始请求接口 {}'.format(url))
            response = yield test_client.fetch(url, **argv)
        except httpclient.HTTPError as e:
            response = e.response
            log.warning('请求接口 {} 异常# {}'.format(url, str(response.error if response else e)))
        # test_client.close()
        if response and response.code in [301, 302]:
            for cookie in response.headers.get_list('Set-Cookie'):
                self.headers['Cookie'] += '{};'.format(cookie)
            url = response.headers.get('Location')
            log.info('{} {} {}'.format(response.code, response.reason, url))
            if response.reason.find('Moved') >= 0:
                response = yield self.__request_url(url=url, env=env, method=method, body=body, follow_redirects=follow_redirects)
            elif follow_redirects:
                response = yield self.__request_url(url=url, env=env, method='GET', follow_redirects=follow_redirects)
        log.info('结束请求接口 {}'.format(url))
        return response

    # 执行单接口测试
    @gen.coroutine
    def run_test(self, url='', label='', comment='', method='GET', headers='', body='', crypt='none',
                 encrypt_content='', no_test=False, check_key='', decrypt_content='', checkpoint='',
                 env='none', correlation='', correlation_result={}, follow_redirects=True):
        headers, body = yield self.__parse_custom_param(headers=headers, body=body,
                                                        correlation_result=correlation_result)
        self.get_headers(headers)
        request_body = yield self.__get_body(body=body, do='encrypt', name=crypt, crypt_key=encrypt_content)
        if no_test:
            return request_body
        resp = yield self.__request_url(url=url, env=env, method=method, body=request_body, follow_redirects=follow_redirects)
        response = yield self.__parse_response(response=resp, name=crypt, crypt_key=decrypt_content, checkpoint=checkpoint,
                                               check_key=check_key, correlation=correlation, method=method, url=url)
        response['label'] = label
        response['comment'] = comment
        if not resp:
            response['request_body'] = request_body
            for key in self.headers:
                response['request_headers'] += '{}: {}\r\n'.format(key, self.headers[key])
        elif method == 'GET':
            response['request_body'] = request_body
        log.info('响应返回 {}'.format(json.dumps(response, ensure_ascii=False)))
        return response
