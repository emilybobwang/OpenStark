#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,datetime,time,json
import requests
import re
from urllib3 import encode_multipart_formdata
from tornado.web import app_log as log
from tornado.httpclient import AsyncHTTPClient
from tornado import gen,httpclient
from handlers.common import BaseHandler, authenticated_async
from tornado.httputil import urlencode
import functions
import settings


class SynConfig(BaseHandler):
    '''同步服务器配置'''
    def __init__(self):
        self.path, f = os.path.split(functions.__file__)
        self.path = self.path[:self.path.rfind('functions')]
        # print(self.path)

    def defaultHeader(self):
        '''默认报文头'''
        header = {}
        header['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 SE 2.X MetaSr 1.0)"
        header['Accept'] = "*/*"
        header['Accept-Language'] = "zh-CN,zh;q=0.8"
        header['Accept-Encoding'] = "gzip,deflate,sdch"
        header['Connection'] = "keep-alive"
        header['Upgrade-Insecure-Requestsy'] = "1"
        header['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
        header['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
        return header

    def defaultUserInfo(self,ip):
        '''获取服务器账号密码'''
        if (ip == '172.20.77.15') or ('172.20.77' in ip):
            loginName = 'admin88'
            loginPwd = '88admin'
        else:
            loginName = 'admin66'
            loginPwd = '66admin'
        return loginName,loginPwd

    def login(self,ip):
        '''登录'''
        log.info('开始登陆服务器 %s' %ip)
        flag = 0
        loginUrl="http://"+ip+":9040/config/login"
        headers=self.defaultHeader()
        try:
            login = requests.get(loginUrl,timeout=60)
        except Exception as e:
            log.info(e)
            flag = 2
            cookie = str(e)
        else:
            getcookietoken=re.findall(r"Cookie JSESSIONID=(.*?) for",str(login.cookies))
            cookietoken=getcookietoken[0]
            cookie={
            'JSESSIONID':cookietoken
            }
            loginName,loginPwd = self.defaultUserInfo(ip)
            logindata = {
                'loginName': loginName,
                'loginPwd': loginPwd,
                'RedImg.x':44,
                'RedImg.y':18
            }
            try:
                loginRes = requests.post(login.url,headers=headers,data=logindata,cookies=cookie,timeout=60)
                requests.post('http://'+ip+':9040/config/action/main/initMenu ',headers=headers,cookies=cookie,timeout=60)
            except Exception as e:
                flag = 'false'
                flag = 3
                cookie = str(e)
            else:
                if '欢迎使用' in ((loginRes.content).decode('utf-8')):
                    flag = 1
                    log.info('登陆服务器%s成功' % ip)
                elif  '登录名及密码不能为空' in ((loginRes.content).decode('utf-8')):
                    lflag = 4
                    cookie = '登录服务器%s 登录名及密码不能为空' % ip
                elif '用户名或者密码错误' in ((loginRes.content).decode('utf-8')):
                    lflag = 5
                    cookie = '登录服务器%s 用户名或者密码错误' % ip
                else:
                    flag = 6
                    cookie = '登录服务器%s失败' % ip
            finally:
                return flag,cookie
        finally:
            return flag,cookie


    def downLoadFiles(self,ip,cookie):
        '''下载文件'''
        log.info('开始从服务器%s上下载配置文件' %ip)
        flag = ''
        downLoadContent = ''
        # flag,cookie = self.login(ip)
        downLoadUrl = 'http://'+ip+':9040/config/action/zk/exportParams?nodeId=0'
        headers = self.defaultHeader()
        try:
            downLoadRes = requests.get(downLoadUrl,headers=headers,cookies=cookie)
            downLoadContent = (downLoadRes.content).decode('utf-8')
            if 'config-pro' in downLoadContent:
                flag = 'true'
                log.info('从服务器%s上下载配置文件成功' %ip)
            else:
                flag = 'false'
        except:
            flag = 'false'
            log.info('从服务器%s上下载配置文件出现异常' %ip)
        finally:
            return flag,downLoadContent

    def upLoadFiles(self,ip,cookie,path,filename):
        '''上传文件'''
        log.info('开始上传配置文件到服务器%s上' %ip)
        flag = ''
        upLoadResContent = ''
        upLoadUrl = 'http://'+ip+':9040/config/action/zk/importParams?nodeId=0'
        fileName = filename
        filePath = path
        data = {}
        headers =self.defaultHeader()
        data['importParamFile']= (fileName,open(os.path.join(filePath, fileName),'rb').read().decode('GB2312').encode('utf-8'))
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        headers['Content-Type'] = encode_data[1]
        try:
            upLoadRes = requests.post(upLoadUrl, headers=headers, data=data,cookies=cookie)
            upLoadResContent = (upLoadRes.content).decode('utf-8')
            if 'true' in upLoadResContent:
                flag = 'true'
                log.info('上传配置文件到服务器%s上成功' %ip)
            else:
                flag = 'false'
        except:
            flag = 'false'
            upLoadResContent = '文件上传出现异常'
            log.info('上传配置文件到服务器%s上出现异常' %ip)
        finally:
            return  flag,upLoadResContent

    def upLoadContent(self,ip,cookie,filename,Content):
        '''上传文件'''
        log.info('开始上传配置文件到服务器%s上' %ip)
        flag = ''
        upLoadResContent = ''
        upLoadUrl = 'http://'+ip+':9040/config/action/zk/importParams?nodeId=0'
        fileName = filename
        data = {}
        headers =self.defaultHeader()
        data['importParamFile']= (fileName,Content)
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        headers['Content-Type'] = encode_data[1]
        try:
            upLoadRes = requests.post(upLoadUrl, headers=headers, data=data,cookies=cookie)
            upLoadResContent = (upLoadRes.content).decode('utf-8')
            if 'true' in upLoadResContent:
                flag = 'true'
                log.info('上传配置文件到服务器%s上成功' %ip)
            else:
                flag = 'false'
        except:
            flag = 'false'
            upLoadResContent = '文件上传出现异常'
        finally:
            return  flag,upLoadResContent

    def writeFiles(self,path,fileName,content):
        '''写文件'''
        log.info('开始把配置文件写到文件%s中' %fileName)
        writefilePath = path
        writefileName = fileName
        writeContent = content
        try:
            newF = open(os.path.join(writefilePath, writefileName), 'w')
            newF.write(writeContent)
            log.info('配置内容写到文件%s中成功' %fileName)
        except:
            log.info('配置内容写到文件%s中出现异常' %fileName)
            pass
        finally:
            if newF:
                newF.close()

    def updateContent(self,sourceIp,targetIp,content):
        '''更新内容 '''
        log.info('开始更改把配置文件中的内容')
        flag = ''
        try:
            if content != '':
                # 替换多实例端口
                content = content.replace("3306", "3307")
                content = content.replace("3307/product", "3306/product")

                content = content.replace("3307/xnaccount", "3306/xnaccount")
                content = content.replace("3307/db_xnapp", "3308/db_xnapp")
                content = content.replace("3307/pcts", "3306/pcts")
                content = content.replace("3307/af88", "3306/af88")
                content = content.replace("db10-m.af88.com.cn:3307", "db10-m.af88.com.cn:3306")
                content = content.replace("db30-m.af88.com.cn:3307", "db30-m.af88.com.cn:3308")

                #2018-03-15添加
                content = content.replace("3333/xnaccount", "3306/xnaccount")
                content = content.replace("3333/product", "3306/product")

                # 2018-01-30 chenjingli添加(java版本时）
                if (targetIp == '172.20.20.114') or (targetIp == '172.20.20.111'):
                    # 替换jdbc连接数
                    content = content.replace("jdbc.pool.size.max=.*", "jdbc.pool.size.max=250")
                else:
                    # 如果原配置不是61的话还需要更新下载文件的里面的内容
                    content = content.replace("jdbc.pool.size.max=.*", "jdbc.pool.size.max=50")

                ### -------------- web-8000-be的配置中心的修改 --------------
                content = content.replace("db20-m.af88.com.cn:3306", "db20-m.af88.com.cn:3307")
                content = content.replace("db20-s.af88.com.cn:3306", "db20-s.af88.com.cn:3307")

                content = content.replace("db10-m.af88.com.cn:3308", "db10-m.af88.com.cn:3307")
                content = content.replace("db10-s.af88.com.cn:3308", "db10-s.af88.com.cn:3307")

                content = content.replace("db01.af88.com.cn:3307,db06.af88.com.cn:3306", "db01.af88.com.cn:3306,db06.af88.com.cn:3306")
                content = content.replace("db10-m.af88.com.cn:3306,db10-s.af88.com.cn:3307", "db10-m.af88.com.cn:3307,db10-s.af88.com.cn:3307")
                content = content.replace("db01.af88.com.cn:3307,db06.af88.com.cn:3306/af88", "db01.af88.com.cn:3306,db06.af88.com.cn:3306/af88")

                content = content.replace("mobile.app.httpclient.url=http://172.20.77.122:8079/API", "mobile.app.httpclient.url=http://" + targetIp + ":8079/API")

                ### -------------- app-6003 --------------

                ### -------------- app-6004-msg --------------
                # 替换6004上面发送短信和邮箱的配置
                content = content.replace("sms.default.channel=.*", "sms.default.channel=online")
                content = content.replace("email.smtp.host=.*", "email.smtp.host=smtp.xiaoniu88test.com")
                content = content.replace("email.default.password=.*", "email.default.password=test")
                content = content.replace("greenmail.remote.userid=.*", "greenmail.remote.userid=0000")
                content = content.replace("greenmail.salt=.*", "greenmail.salt=123456")
                content = content.replace("greenmail.send.url=.*", "greenmail.send.url=http://127.0.0.1/send_email.json")

                # 修改为短信挡板
                content = content.replace("sms.default.channel=.*", "sms.default.channel=online")
                content = content.replace("sms.channel.backup1=.*", "sms.channel.backup1=online")
                content = content.replace("sms.normal.channel=.*", "sms.normal.channel=online")
                content = content.replace("sms.channel.backup2=.*", "sms.channel.backup2=online")
                content = content.replace("sms.voice.channel=.*", "sms.voice.channel=online_voice")
                content = content.replace("sms.xw400.url=.*", "sms.xw400.url=172.20.20.160:9788/thirdplat/return0req")

                ###  -------------- app-6020 --------------
                # 6020不发送还款通知的配置修改
                content = content.replace("wechat.template.switch.enabled=.*", "wechat.template.switch.enabled=false")

                ###  -------------- app-6035 --------------
                # 修改6035的配置
                content = content.replace("dubbo.financier.version=.*", "dubbo.financier.version=2.0.0")
                content = content.replace("dubbo.payment.version=.*", "dubbo.payment.version=2.0.0")
                content = content.replace("dubbo.trade.version=.*", "dubbo.trade.version=2.0.0")

                ###  -------------- app-6037 --------------
                # 修改6037中生产的key为测试的key（2017-10-23添加：准生产已经过滤了一遍）
                content = content.replace("push.xinge.push.iso.env=.*", "push.xinge.push.iso.env=2")
                content = content.replace("push.xinge.push.iso.accessId=.*", "push.xinge.push.iso.accessId=2200266303")
                content = content.replace("push.xinge.push.iso.secredKey=.*", "push.xinge.push.iso.secredKey=97559800878346b5fdba6b56042ea18e")
                content = content.replace("push.xinge.push.andriod.accessId=.*", "push.xinge.push.andriod.accessId=2100266302")
                content = content.replace("push.xinge.push.andriod.secredKey=.*", "push.xinge.push.andriod.secredKey=6fb9c5ce55758d04c43fcc8141ad8180")
                content = content.replace("push.device.relation.exsit.flag.expired.second=.*", "push.device.relation.exsit.flag.expired.second=86400")

                ###  -------------- web-9018 --------------
                content = content.replace("partner.Captcha.=.*", "partner.Captcha.=true")
                # content = content.replace("app-6027-financier/resourceParam/jdbc.properties/mongodb.password=.*",
                #                           "app-6027-financier/resourceParam/jdbc.properties/mongodb.password=financier")

                ###  -------------- 以上是模糊替换，以下是精确替换 --------------
                # 替換6018配置
                content = content.replace("172.20.20.86:9788", "172.20.20.160:9788/thirdplat")

                # 替换9019的redis地址和名称
                content = content.replace("cc.sentinel.address=172.20.20.101:26379,172.20.20.102:26379,172.20.20.103:26379",
                                          "cc.sentinel.address=redis1.af88.com.cn:26379,redis2.af88.com.cn:26379,redis3.af88.com.cn:26379")
                content = content.replace("cc.sentinel.masterName=themaster", "cc.sentinel.masterName=mymaster")

                # 修改6022的配置
                nowDate = datetime.datetime.now()
                yesterDay = (nowDate+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
                content = content.replace("userEarningDate=", "userEarningDate=" + yesterDay + "")

                ###  -------------- app-6012 --------------
                # 修改6012的配置：牛鼎丰的配置从连接准生产修改为连接测试环境
                content = content.replace("sign.interfaceUrl=https://esign-pre.niudingfeng.com/signature-web/",
                                          "sign.interfaceUrl=http://10.17.2.173:2222/signature-web/")

                ###  -------------- 启动内存为768M --------------
                if targetIp == '172.20.20.114':
                    content = content.replace("-server -Xms[0-9]+[A-Za-z] -Xmx[0-9]+[A-Za-z]", "-server -Xms2G -Xmx2G")

                # 替换启动脚本（启动服务器所占用内存2017-10-20添加,排除性能环境）
                if targetIp != '172.20.20.114':
                    content = content.replace("-server -Xms[0-9]+[A-Za-z] -Xmx[0-9]+[A-Za-z]", "-server -Xms768M -Xmx768M")

                ###  -------------- web-8077刷pcts和product的日志时间修改 --------------
                content = content.replace("app.index.async.time=.*", "app.index.async.time=600000")
                content = content.replace("app.list.async.time=.*", "app.list.async.time=600000")
                content = content.replace("app.gold.price.interval=.*", "app.gold.price.interval=600000") # 这个是黄金的价格

                ###  -------------- web-9008刷pcts和product的日志时间修改 --------------
                content = content.replace("delay.index.current.list.time.ms=.*", "delay.index.current.list.time.ms=600000")
                content = content.replace("delay.index.experience.time.ms=.*", "delay.index.experience.time.ms=600000")
                content = content.replace("delay.index.product.list.time.ms=.*", "delay.index.product.list.time.ms=600000")
                content = content.replace("delay.index.yyn.list.time.ms=.*", "delay.index.yyn.list.time.ms=600000")

                ###  -------------- app-6048(2018-02-03添加) --------------
                # content = content.replace("app-6048-deposit/businessParam/notify_url=.*", "app-6048-deposit/businessParam/notify_url=http://web.xiaoniu88.com:9048/deposit/notify/gateway")
                # content = content.replace("bank.publicKey.path=.*", "bank.publicKey.path=/usr/local//xiaoniu/xn.pubKey/xn_pub.key")
                # content = content.replace("bank.api.url=.*", "bank.api.url=http://172.20.20.160:8280/xnzx-test-project/deposit/deposit")
                # content = content.replace("bank.autowithdraw.url=.*", "bank.autowithdraw.url=http://172.20.20.160:8280/xnzx-test-project/deposit/deposit/1001/withdraw/6615162675826787")
                # content = content.replace("/-pro/app-6048-deposit/businessParam/callback_url=.*", "/-pro/app-6048-deposit/businessParam/callback_url=http://web.xiaoniu88.com:9048/deposit/callback/gateway")

                content = content.replace("218.17.12.43:59048", "web.xiaoniu88.com:9048")

                ###  -------------- 所有mq的修改，mongdb(2018-02-03添加) --------------
                # 添加数据库用户名和密码的修改
                content = content.replace("jdbc.username=dev_pro", "jdbc.username=root")
                content = content.replace("jdbc.password=1pebuniAtjtbwgF#1ue2", "jdbc.password=123456")

                content = content.replace("db.login.name=dev_pro", "db.login.name=root")
                content = content.replace("db.login.password=1pebuniAtjtbwgF#1ue2", "db.login.password=123456")


                # 添加修改配置6043的金融办的配置（2018-03-20）
                content = content.replace("financeoffice.password=.*", "financeoffice.password=123456")
                content = content.replace("ftp_server_password=.*", "ftp_server_password=123456")


                # 存管修改为挡板的配置（6048-app的配置 2018-03-27添加）
                content = content.replace("bank.api.url=.*","bank.api.url=http://172.20.20.160:8280/xnzx-test-project/deposit")
                content = content.replace("bank.publicKey.path=.*","bank.publicKey.path=/usr/local//xiaoniu/bank.publicKey/xn_pub.key")

                # 修改所有的mongdb的集群模式改为单机模式(开发mq不支持单机模式，2017.9月又修改为集群模式)
                # content = content.replace("mongodb.replicaSet=m0.af88.com.cn:27017,m1.af88.com.cn:27017,m2.af88.com.cn:27017","mongodb.replicaSet=m0.af88.com.cn:27017");

                # content = content.replace()
            flag = 'true'
            log.info('配置文件中的内容更改完成')
        except:
            flag = 'false'
            content = '文件更新过程出现异常'
            log.info('配置文件更新过程出现异常')
        finally:
            return flag,content

    def deleteConfig(self,ip,cookie):
        ''' 删除同步目标服务器上配置文件 '''
        log.info('开始删除目标服务器 %s 上的配置文件' % ip)
        flag = ''
        deleteResContent = ''
        deleteUrl = 'http://'+ip+':9040/config/action/zk/nodeDel'
        headers = self.defaultHeader()
        nodePath = '/config-pro'
        zkUrl = 's1.af88.com.cn:2181,s2.af88.com.cn:2181,s3.af88.com.cn:2181'
        deletedata = {
            'nodePath': nodePath,
            'zkUrl': zkUrl
        }
        try:
            deleteRes = requests.post(deleteUrl,headers=headers,data=deletedata,cookies=cookie)
            deleteResContent = ((deleteRes.content).decode('utf-8'))
            if '删除成功' in deleteResContent:
                flag = 'true'
                log.info('目标服务器 %s上的配置文件删除成功' % ip)
            else:
                flag = 'false'
                log.info('目标服务器 %s上的配置文件删除失败')
        except:
            flag = 'false'
            log.info('目标服务器 %s上的配置文件删除过程中出现异常')
        finally:
            return flag,deleteResContent

    def backupTargetConfig(self,ip,cookie):
        ''' 备份目标服务器上配置文件 '''
        log.info('开始备份目标服务器 %s 上的配置文件' % ip)
        bflag = ''
        bakPath = os.path.join(settings.static_path, 'bakConfig')
        if not os.path.exists(bakPath):
            os.makedirs(bakPath)
        bakFileName = ip+'_configParams_'+time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.properties'
        dflag,downLoadContent = self.downLoadFiles(ip,cookie)
        if dflag == 'false':
            bflag = 'false'
            bakContent = '文件下载失败，导入前备份文件不成功'
            log.info('文件下载失败，导入前备份目标服务器 %s 上的配置文件%s不成功' % (ip,bakFileName))
        else:
            self.writeFiles(bakPath,bakFileName,downLoadContent)
            bflag = 'true'
            bakContent = '文件%s备份成功' % bakFileName
            log.info('备份目标服务器 %s 上的配置文件%s 成功' % (ip,bakFileName))
        return bflag,bakContent

    def readFileNameList(self,ip):
        ''' 读取文件名列表 '''
        log.info('开始读取备份文件')
        bakPath = os.path.join(settings.static_path, 'bakConfig')
        if not os.path.exists(bakPath):
            os.makedirs(bakPath)
        fileNameList = os.listdir(bakPath)
        chooseFileNameList = []
        for fileName in fileNameList:
            fileNameDiv = fileName.split('_')
            if fileNameDiv[0] == ip:
                chooseFileNameList.append(fileNameDiv[1]+'_'+fileNameDiv[2])
        return chooseFileNameList

    def recoveryBackupFile(self,ip,fileName):
            ''' 恢复备份文件 '''
            flag = 0
            msg = ''
            filenN = 'configParams.properties'
            bakFileName = ip+'_'+fileName
            bakPath = os.path.join(settings.static_path, 'bakConfig')
            if not os.path.exists(bakPath):
                os.makedirs(bakPath)
            fileNameList = os.listdir(bakPath)
            for fN in fileNameList:
                if fN == bakFileName:
                    bakContent = open(os.path.join(bakPath, bakFileName),'rb').read().decode('GB2312').encode('utf-8')
                    break
                else:
                    bakContent = ''
            if bakContent == '':
                flag = 1   # 备份文件内容为空
                msg = '备份文件内容为空，请检测该配置文件是否存在'
            else:
                lflage,lcookie = self.login(ip)
                if lflage == 'false':
                    flag = 2  # 登录还原备份文件的服务不成功
                    msg = '登录还原备份文件的服务不成功'
                else:
                    uflag,upRes = self.upLoadContent(ip,lcookie,filenN,bakContent)
                    if uflag == 'false':
                        flag = 3
                        msg = '还原备份文件导入不成功'
                    else:
                        flag = 4
                        msg = '还原备份文件成功'
            return flag,msg

    @gen.coroutine
    def login_bak(self,ip):
        # lcookie = ''
        # lflag = 0
        # url = "http://"+ip+":9040/config/login"
        # # urltest = "http://localhost:8000/test3"
        # lName,lPwd = self.defaultUserInfo(ip)
        # lheaders = self.defaultHeader()
        # client = AsyncHTTPClient()
        # try:
        #     response = yield client.fetch(url, method='GET',headers=lheaders)
        # except Exception as e:
        #     lcookie = str(e)
        #     lflag = 5
        # else:
        #     loginCookies = response.headers.get_list('Set-Cookie')
        #     cookies = loginCookies[0].split(';')
        #     lcookie = cookies[0]
        #     # print(response.headers)
        #     response.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        #     print(response.headers)
        #     # cookie={
        #     # 'JSESSIONID':lcookie
        #     # }
        #     RedImgX = 44
        #     RedImgY = 18
        #     logindata = {}
        #     logindata['loginName']=lName
        #     logindata['loginPwd']=lPwd
        #     logindata['RedImg.x']=RedImgX
        #     logindata['RedImg.y']=RedImgY
        #     print(logindata)
        #     try:
        #         # client = AsyncHTTPClient()
        #         # lresponse = yield client.fetch(url, method='POST', body=json.dumps(logindata),headers=response.headers)
        #         lresponse = yield client.fetch(url, method='POST', body=urlencode(logindata),headers=response.headers,follow_redirects=False)
        #         print((lresponse.body).decode('utf-8'))
        #     except httpclient.HTTPError as e:
        #         # log.info(e)
        #         print(e)
        #         lcookie = str(e)
        #         lflag = 3
        #     else:
        #         if '欢迎使用' in ((lresponse.body).decode('utf-8')):
        #             lflag = 1
        #             log.info('登陆服务器%s成功' % ip)
        #         elif  '登录名及密码不能为空' in ((lresponse.body).decode('utf-8')):
        #             lflag = 6
        #             lcookie = '登录服务器%s 登录名及密码不能为空' % ip
        #         elif '用户名或者密码错误' in ((lresponse.body).decode('utf-8')):
        #             lflag = 2
        #             lcookie = '登录服务器%s 用户名或者密码错误' % ip
        #         else:
        #             flag = 4
        #             lcookie = '登录服务器%s失败' % ip
        #     # finally:
        #     #     return lflag,lcookie
        # finally:
        #     return lflag,lcookie
        pass

    def on_response(self, resp):
     body = json.loads(resp.body)
     if body == None:
         self.write('error')
     else:
         self.write(body)
     return

if __name__ == '__main__':
    # path = os.getcwd()
    # print(path)
    # filename = 'configParams.properties'
    fileName = ''
    # serverIp='172.20.20.194' # 登录ip
    ip='172.20.20.114' # 登录ip
    # userName = 'admin66' # 你的用户名
    # password = '66admin' # 你的密码
    sc = SynConfig()
    flag,cookie = sc.login(ip)
    # bflag,bakContent = sc.backupTargetConfig(ip,cookie)
    # print(bflag,bakContent)
    # print(sc.readFileNameList(ip))
    # print(sc.recoveryBackupFile(ip,'configParams_20181015184055.properties'))
    # print("flag:%s cookie:%s\n " %(flag,cookie))
    # flag,downLoadContent = sc.downLoadFiles(serverIp,cookie)
    # # print(flag,downLoadContent)
    # print('下载状态：%s'% flag)
    # sc.writeFiles(path,filename,downLoadContent)
    # flag,upLoadContent = sc.upLoadFiles(serverIp,cookie,path,filename)
    # print(upLoadContent)
    # flag,upLoadContent = sc.upLoadContent(serverIp,cookie,filename,downLoadContent)
    # print(upLoadContent)
    # images_path = os.path.join(settings.get('static_path'), op)
    # images_path = os.path.join(settings.static_path)
    # print(images_path)
