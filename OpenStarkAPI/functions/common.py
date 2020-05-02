from Crypto.Hash import MD5
from tornado.log import app_log as log
from urllib.parse import urlsplit, unquote_plus
from munch import munchify
from QTLibrary import QTLibrary
from tornado.concurrent import run_on_executor
from tornado import gen
from concurrent.futures import ThreadPoolExecutor
from functions.mail import Mail
from functions.options import OptionsFunction
import paramiko
import re
import os
import json
import ast
import time
import random
import subprocess
import socket
import base64


class CommonFunction(object):
    def __init__(self):
        self.option_func = OptionsFunction()

    # 对用户密码进行加密
    def encode_password(self, password):
        obj = MD5.new()
        obj.update(password.encode('utf8', errors='ignore') * 3)
        data = obj.hexdigest()
        data = self.__encode_md5(data.encode('utf8', errors='ignore'))
        obj.update(data)
        return obj.hexdigest()

    def __encode_md5(self, md5_string):
        md5_string = bytearray(md5_string)
        buf = bytearray()
        for i in range(len(md5_string)):
            buf.append(((md5_string[i] >> 4) & 0xF) + ord('a'))
            buf.append((md5_string[i] & 0xF) + ord('a'))
        return bytes(buf)

    # 字符串类型及合法性检查
    def check_string(self, string, str_type='email'):
        if str_type == 'email':
            if re.match(r'^[a-zA-Z\d][\w-]+@[\w-]+(\.[a-zA-Z]+)*$', string) is not None:
                return True
            else:
                log.warning('email {} 格式校验不通过'.format(string))
                return False
        elif str_type == 'username':
            if re.match(b'\w*[\x80-\xff]+\w*', string.encode('utf8', errors='ignore')) is not None:
                return False
            elif re.match(r'^[a-zA-Z]\w{1,19}$', string) is not None:
                return True
            else:
                log.warning('username {} 格式校验不通过'.format(string))
                return False
        elif str_type == 'realname':
            if re.match(b'^[\x80-\xff]{6,60}$', string.encode('utf8', errors='ignore')) is not None:
                return True
            else:
                log.warning('realname {} 格式校验不通过'.format(string))
                return False
        elif str_type == 'password':
            if re.match(r'^\S.{5,20}$', string) is not None:
                return True
            else:
                log.warning('password格式校验不通过')
                return False
        elif str_type == 'url':
            if re.match(r'^https?://[\w-]+\.[\w.:/#-]+([?\w=&#-]+)[^-_.]$', string) is not None:
                return True
            else:
                log.warning('url {} 格式校验不通过'.format(string))
                return False
        elif str_type == 'dubbo':
            if re.match(r'^dubbo://[\w-]+\.[\w.:/#-]+([?\w=&#-]+)[^-_.]$', string) is not None:
                return True
            else:
                log.warning('dubbo {} 格式校验不通过'.format(string))
                return False
        elif str_type == 'ip':
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', string) is not None:
                return True
            else:
                log.warning('ip {} 格式校验不通过'.format(string))
                return False
        elif str_type == 'host':
            if re.match(r'^([^http://]|[^https://])[\w-]*\.[\w.-]+[^-_.]$', string) is not None:
                return True
            else:
                log.warning('host {} 格式校验不通过'.format(string))
                return False
        elif str_type == 'json':
            if re.match(r'^\{.*\}$', string) is not None:
                try:
                    json.loads(string)
                    return True
                except Exception as e:
                    log.error(e)
                    log.warning('json {} 格式校验不通过'.format(string))
                return False
            else:
                return False
        elif str_type == 'datetime':
            if re.match(r'^\d{4}/\d{2}/\d{2} \d{2}:\d{2}$', string) is not None:
                return True
            else:
                log.warning('datetime {} 格式校验不通过'.format(string))
                return False
        elif str_type == 'check_key':
            if re.match(r'^\w+=\d\|(int|float|num|str|/.*/|date|time|datetime|list|dict)$',
                        string.strip()) is None and re.match(
                        r'^(\w+|\[\d+\])(\.\w+|\.\[\d+\])*\.\[\w+=\d\|('
                        r'int|float|num|str|/.*/|date|time|datetime|list|dict)('
                        r',\w+=\d\|(int|float|num|str|/.*/|date|time|datetime|list|dict))*\]$', string.strip()
            ) is None:
                log.warning('check_key {} 格式校验不通过'.format(string))
                return False
            else:
                return True
        else:
            return False

    # 切割URL
    def url_split(self, url):
        urls = urlsplit(url)
        url = urls.netloc.split(sep=':', maxsplit=1)
        if len(url) == 2:
            port = url[1]
        else:
            if urls.scheme == 'https':
                port = 443
            else:
                port = 80
        host = url[0]
        urls = {'scheme': urls.scheme, 'netloc': urls.netloc, 'host': host, 'port': port, 'path': urls.path,
                'query': urls.query, 'fragment': urls.fragment}
        return munchify(urls)

    # 解析URL
    def url_query_decode(self, query=''):
        query_dict = dict()
        for line in unquote_plus(query).split('&'):
            line = line.split(sep='=', maxsplit=1)
            if len(line) == 2:
                query_dict[line[0]] = line[1]
        if len(query_dict) == len(query.split('&')):
            return query_dict
        else:
            return query

    # 判断是否是list或dict并尝试转换
    def convert_to_list_or_dict(self, string, s_type='list'):
        flag = True
        if s_type == 'list' and not isinstance(string, list):
            try:
                if isinstance(string, bytes):
                    string = ast.literal_eval(string.decode('utf8', errors='ignore'))
                else:
                    string = ast.literal_eval(string)
            except Exception as e:
                log.warning(e)
            if not isinstance(string, list):
                flag = False
        elif s_type == 'dict' and not isinstance(string, dict):
            if isinstance(string, bytes):
                string = string.decode('utf8', errors='ignore')
            try:
                string = ast.literal_eval(string)
            except Exception as e:
                log.warning(e)
                try:
                    string = json.loads(string)
                except Exception as e:
                    log.warning(e)
            if not isinstance(string, dict):
                flag = False
        return flag, string

    # 预定义参数
    def default_param(self):
        data_gen = QTLibrary()
        banks = [dict(name="招商银行股份有限公司北京分行  ", start=6214830, end=6214832, n=9),
                 dict(name="中国工商银行总行营业部", start=6222020, end=6222022, n=12),
                 dict(name="中国建设银行北京新华支行", start=6227000, end=6227002, n=12)]
        bank = random.choice(banks)
        default_param = dict()
        default_param['{random_mobile}'] = '{}{}'.format(random.choice(['13', '14', '15', '17', '18']),
                                                         random.randint(100000000, 999999999))
        default_param['{random_email}'] = '{}@automation.test'.format(''.join(random.sample(
            'abcdefghijklmnopqrstuvwxyz', 6)))
        default_param['{timestamp}'] = int(time.time())
        default_param['{datetime}'] = time.strftime('%Y-%m-%d %H:%M:%S')
        default_param['{datetime_int}'] = time.strftime('%Y%m%d%H%M%S')
        default_param['{date}'] = time.strftime('%Y-%m-%d')
        default_param['{date_int}'] = time.strftime('%Y%m%d')
        id_card_no = data_gen.gen_idcard()
        default_param['{id_card_no}'] = id_card_no
        default_param['{id_card_birthday}'] = time.strftime('%Y-%m-%d', time.strptime(id_card_no[6:-4], '%Y%m%d'))
        default_param['{bank_card_no}'] = str(random.randint(bank['start'], bank['end'])) + data_gen.gen_nums(bank['n'])
        default_param['{chinese_name}'] = data_gen.gen_name()
        return default_param

    # 发送系统邮件
    @gen.coroutine
    def send_email(self, subject, content, to, cc=list()):
        config = yield self.option_func.get_option_by_type(o_type='common')
        password = config.get('emailPasswd')
        password = password and base64.b16decode(password.encode('utf8', errors='ignore')).decode('utf8', errors='ignore')
        mail = Mail(smtp_server=config.get('emailHost'), smtp_port=config.get('emailPort'),
                    smtp_user=config.get('emailUser'), smtp_password=password, mail_type=config.get('emailType'),
                    use_ssl=config.get('emailSSL'), mail_from=config.get('emailFrom'))
        res, msg = yield mail.send_mail(subject=subject, message=content, to=to, cc=cc)
        return res, msg


class ThreadFunction(object):
    executor = ThreadPoolExecutor(50)

    def __init__(self):
        self.func = CommonFunction()

    # 远程执行shell
    @run_on_executor
    def exec_remote_shell(self, host='localhost', port=22, username='root', password='', shell=''):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect(hostname=host, port=port, username=username, password=password)
            log.info('RUN SHELL: {}'.format(shell))
            stdin, stdout, stderr = ssh_client.exec_command(shell)
            msg = stdout.read()
            err_msg = stderr.read()
            if isinstance(msg, bytes):
                msg = msg.decode('utf8', errors='ignore').strip()
            if len(msg) > 0 or not err_msg:
                log.info(msg)
                ssh_client.close()
                return True, msg
            else:
                if isinstance(err_msg, bytes):
                    err_msg = err_msg.decode('utf8', errors='ignore').strip()
                log.error(err_msg)
                ssh_client.close()
                return False, err_msg
        except Exception as e:
            log.info(e)
            return False, e

    # 通过sftp传输文件
    @run_on_executor
    def exec_sftp(self, host='localhost', port=22, username='root', password='', do='get', local_path='.', remote_path='/home'):
        try:
            trans = paramiko.Transport((host, int(port)))
            trans.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(trans)
            if do == 'get':
                log.info('从远程路径 {} 获取文件到 {}'.format(remote_path, local_path))
                sftp.get(remotepath=remote_path, localpath=local_path)
                return True, '操作成功!'
            elif do == 'put':
                log.info('从本地路径 {} 上传文件到 {}'.format(local_path, remote_path))
                sftp.put(localpath=local_path, remotepath=remote_path)
                return True, '操作成功!'
            else:
                return False, '操作类型错误!'
        except Exception as e:
            log.info(e)
            return False, e

    # 本地执行shell
    @run_on_executor
    def exec_shell(self, shell=''):
        try:
            log.info('RUN SHELL: {}'.format(shell))
            p = subprocess.Popen(shell, env=os.environ, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, encoding='utf8', errors='ignore')
            msg, err_msg = p.communicate()
            if isinstance(msg, bytes):
                msg = msg.decode('utf8', errors='ignore').strip()
            else:
                msg = str(msg).strip()
            if len(msg) > 0 or not err_msg:
                log.info(msg)
                return True, msg
            if isinstance(err_msg, bytes):
                err_msg = err_msg.decode('utf8', errors='ignore').strip()
            else:
                err_msg = str(err_msg).strip()
            log.error(err_msg)
            return False, err_msg
        except Exception as e:
            log.error(e)
            return False, e

    # 检查指定端口是否存在
    @run_on_executor
    def check_port(self, host, port):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect((host.strip(), int(port)))
            soc.close()
            return True
        except socket.error as e:
            log.error(e)
            return False
