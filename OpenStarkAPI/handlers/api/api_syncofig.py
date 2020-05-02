#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json,re
from handlers.common import BaseHandler, authenticated_async
from tornado import gen
from tornado.web import app_log as log
from handlers.common import AddLogs
from functions.synConfig import SynConfig
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import urlencode

"""
配置同步相关接口
"""
class SynConfigHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def post(self):
        log.info('进入配置同步post方法')
        flag = 'FAIL'
        msg = '未知错误'
        filename = 'configParams.properties'
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        params = yield self.get_request_body_to_json()
        sourceIp = params.sourceIp or ''
        targetIp = params.targetIp or ''
        sc = SynConfig()
        if sourceIp is '':
            flag = 'FAIL'
            msg = '导出配置文件服务器ip地址不能为空'
        elif targetIp is '':
            flag = 'FAIL'
            msg = '导入配置文件服务器ip地址不能为空'
        elif targetIp == '172.20.77.15':
            flag = 'FAIL'
            msg = '导入配置文件服务器不能为准生产服务器'
        else:
            try:
                slflag,scookie = sc.login(sourceIp)
                # slflag,scookie = yield sc.login(sourceIp)
                if slflag != 1:
                    flag = 'FAIL'
                    msg = scookie
                else:
                    dflag,downLoadContent = sc.downLoadFiles(sourceIp,scookie)
                    if dflag == 'false':
                        flag = 'FAIL'
                        msg = "源配置文件下载失败"
                    else:
                        uflag = 'false'
                        i = 0
                        while (i<=3):
                            i = i + 1
                            uflag,updateContent = sc.updateContent(sourceIp,targetIp,downLoadContent)
                            if uflag == 'true':
                                break
                        if uflag == 'false':
                            flag = 'FAIL'
                            msg = "更改配置内容失败"
                        else:
                            tlflag,tcookie = sc.login(targetIp)
                            # tlflag,tcookie = yield sc.login(sourceIp)
                            if tlflag != 1:
                                flag = 'FAIL'
                                msg = tcookie
                            else:
                                bflag,bakContent = sc.backupTargetConfig(targetIp,tcookie)
                                # deleteFlag,deleteResContent = sc.deleteConfig(targetIp,tcookie)
                                deleteFlag = 'false'
                                tflag,upLoadContent = sc.upLoadContent(targetIp,tcookie,filename,updateContent)
                                if tflag == 'false':
                                    flag = 'FAIL'
                                    msg = "配置文件上传目标服务器失败"
                                elif deleteFlag == 'false':
                                    flag = 'SUCCESS'
                                    msg = '覆盖导入成功 (没有删除原配置)'
                                else:
                                    flag = 'SUCCESS'
                                    msg = '导入成功'
            except:
                flag = 'FAIL'
                msg = '文件同步异常'
                pass
        msgs = dict(status=flag, message=msg)
        self.write_json(msgs)

    @gen.coroutine
    def login(self,ip):
        # url = "http://172.20.20.114:9040/config/login"
        url = "http://"+ip+":9040/config/login"
        loginName,loginPwd = self.defaultUserInfo(ip)
        logindata = {
            'loginName': loginName,
            'loginPwd': loginPwd,
            'RedImg.x':44,
            'RedImg.y':18
        }
        client = AsyncHTTPClient()
        response = yield client.fetch(url, method='POST', body=urlencode(logindata))
        login_cookies = response.headers.get_list('Set-Cookie')
        cookie = login_cookies[0].split(';')
        # print(response)
        # print(response.code)
        print(login_cookies)
        print(cookie[0])
        lflag = 'true'
        return lflag,cookie[0]

    def defaultUserInfo(self,ip):
        '''获取服务器账号密码'''
        if (ip == '172.20.77.15') or ('172.20.77' in ip):
            loginName = 'admin88'
            loginPwd = 'root@xiaoniu88.COM'
        else:
            loginName = 'admin66'
            loginPwd = '66admin'
        return loginName,loginPwd


"""
查询备份配置相关接口
"""
class SynConfigQueryHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self):
        log.info('进入查询备份文件名列表get方法')
        flag = 'FAIL'
        msg = '未知错误'
        fileNameList = []
        queryIp = self.get_argument('queryIp', None)
        sc = SynConfig()
        if queryIp is None:
            flag = 'FAIL'
            msg = '查询配备份服务器ip不能为空'
        else:
            try:
                fileNameList = sc.readFileNameList(queryIp)
                flag = 'SUCCESS'
                msg = ''
            except:
                flag = 'FAIL'
                msg = '文件同步异常'
                pass
        msgs = dict(status=flag, message=msg ,data=fileNameList)
        self.write_json(msgs)

"""
还原备份配置相关接口
"""
class SynConfigRecoveryHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def post(self):
        log.info('进入还原备份配置文件post方法')
        flag = 'FAIL'
        msg = '未知错误'
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        params = yield self.get_request_body_to_json()
        ip = params.ip or ''
        fileName = params.filename or ''
        sc = SynConfig()
        if ip is '':
            flag = 'FAIL'
            msg = '恢复配备文件份服务器ip不能为空'
        elif ip == '172.20.77.15':
            flag = 'FAIL'
            msg = '恢复配置文件服务器不能为准生产服务器'
        elif fileName is '':
            flag = 'FAIL'
            msg = '恢复配置文件服名称不能为空'
        else:
            try:
                rflag,msg = sc.recoveryBackupFile(ip,fileName)
                if rflag == 4:
                    flag = 'SUCCESS'
                    msg = msg
                else:
                    flag = 'FAIL'
                    msg = msg
            except:
                flag = 'FAIL'
                msg = '恢复服务器%s的配置文件%s过程中出现异常' % (ip,fileName)
                pass
        msgs = dict(status=flag, message=msg)
        self.write_json(msgs)
