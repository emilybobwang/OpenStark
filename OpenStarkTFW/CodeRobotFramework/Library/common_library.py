# coding=utf8
from Resource.Variables.common import *
from Core.keys import database as db
from Core.keys import builtin as bln
from Core.keys import gen_data as gd
# from Core.keys import keyboard as kb
from Core.keys import webdriver as wd
from Core.keys import requests
import math
import random


class CommonLibrary(object):
    def mysql_query(self, sql, host=db_host, port=db_port, user=db_user, passwd=db_passwd, db_name=db_name, res_dict=False):
        """执行MYSQL查询语句"""
        db_connect_string="database='{}', user='{}', password='{}', host='{}', port={}, charset='UTF8'".format(
            db_name, user, passwd, host, port)
        if res_dict:
            db_connect_string += ', cursorclass=db_api_2.cursors.DictCursor'
        db.connect_to_database_using_custom_params(
            dbapiModuleName='pymysql', db_connect_string='{}'.format(db_connect_string)) 
        result = db.query(sql)
        db.disconnect_from_database()
        return result

    def mysql_update(self, sql, host=db_host, port=db_port, user=db_user, passwd=db_passwd, db_name=db_name):
        """执行MYSQL更新语句"""
        db.connect_to_database_using_custom_params(
            dbapiModuleName='pymysql', db_connect_string="database='{}', user='{}', password='{}', host='{}', port={}, charset='UTF8'".format(
            db_name, user, passwd, host, port)) 
        db.execute_sql_string(sqlString=sql)
        db.disconnect_from_database()

    def get_captcha(self, mobile, ctype='sms'):
        """获取验证码"""
        sql = "SELECT m.`content` FROM xnmsg.`sms_sendlog_his` m WHERE m.`mobile`='{}' ORDER BY m.id DESC LIMIT 10;".format(mobile) if ctype =='sms' else "select m.`content` from xnmsg.`email_sendlog_his` m where m.`email` = '{}' ORDER BY m.id DESC limit 10;".format(mobile)
        for i in range(1, 30):
            verifyCodeList = self.mysql_query(sql)
            if verifyCodeList:
                break
            bln.sleep(1)
        try:
            verifyCode = bln.should_match_regexp(verifyCodeList[0][0], '\\d+')
        except Exception as e:
            print('获取验证码失败# {}, 将使用万能验证码'.format(e))
            verifyCode = 123456
        return verifyCode

    def random_mobile(self, ex=0):
        """随机手机号"""
        if isinstance(ex, list):
            ex = random.choice(ex)
        ex = '135' if ex == 0 else str(ex)
        return ex + gd.gen_nums(8)

    def random_username(self, ex='XNW'):
        """随机用户名"""
        return ex + gd.gen_chars(8, 'L')

    def random_email(self, ext='automation.test'):
        """随机邮箱"""
        return gd.gen_chars(6, 'L') + '@' + ext

    def random_bank_card(self, ex=0):
        """随机卡号"""
        ex = '62258878' if ex == 0 else str(ex)
        return ex + gd.gen_nums(8)

    def get_user_returnAmount(self, isNew='false', users=list()):
        """查询用户待收"""
        amount = 0
        if users and not isinstance(users[0], tuple):
            users = [users]
        for row in users:
            if isNew == 'false':
                res = self.mysql_query("SELECT IFNULL(SUM(i.recivedPrincipal-i.hasPrincipal),0) FROM product.`t_invest` i JOIN product.`t_borrow` b ON b.`id`=i.`borrowId` WHERE i.`investor` = '{}' AND b.`borrowStatus`=4 AND b.`borrowType` NOT IN(11,14,15) AND b.`proType` <> 6 and b.`specialArea`<>10 AND DATE(b.`valueDate`)<'2017-05-01' AND TIMESTAMPDIFF(DAY,'{}',NOW())<=365 AND b.`valueDate` < CURRENT_DATE;".format(row[0], row[1]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name)
                res_pcts = self.mysql_query("SELECT IFNULL(SUM((i.principal-i.actualPrincipal)/100),0) FROM pcts.`t_product` p JOIN pcts.`t_invest` i ON p.`id`=i.`productId` WHERE i.`userId` = '{}' AND p.`productStatus`=40 AND DATE(p.`valueDate`)<'2017-05-01' AND TIMESTAMPDIFF(DAY,'{}',NOW())<=365 and p.`valueDate` < CURRENT_DATE;".format(row[0], row[1]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name)          
            elif isNew == 'true':
                res = self.mysql_query("SELECT IFNULL(SUM(i.recivedPrincipal-i.hasPrincipal),0) FROM product.`t_invest` i JOIN product.`t_borrow` b ON b.`id`=i.`borrowId` WHERE i.`investor`='{}' AND b.`borrowStatus`=4 AND b.`borrowType` NOT IN(11,14,15) and b.`specialArea`<>10 AND b.`proType` <> 6 AND TIMESTAMPDIFF(DAY,'{}',NOW())<=IF('{}'<'2017-05-01 00:00:00',365,90) AND TIMESTAMPDIFF(DAY,b.`valueDate`,NOW())<=90 AND DATE(b.`valueDate`)>='2017-05-01' AND b.`valueDate` < CURRENT_DATE;".format(row[0], row[1], row[1]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name) 
                res_pcts = self.mysql_query("SELECT IFNULL(SUM((i.principal-i.actualPrincipal)/100),0) FROM pcts.`t_product` p JOIN pcts.`t_invest` i ON p.`id`=i.`productId` WHERE i.`userId` = '{}' AND p.`productStatus`=40 AND TIMESTAMPDIFF(DAY,p.`valueDate`,NOW())<=90 AND TIMESTAMPDIFF(DAY,'{}',NOW())<=IF('{}'<'2017-05-01 00:00:00',365,90) AND DATE(p.`valueDate`)>='2017-05-01' and p.`valueDate` < CURRENT_DATE;".format(row[0], row[1], row[1]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name)   
            elif isNew == 'all':
                res = self.mysql_query("SELECT IFNULL(SUM(investAmount),0) FROM (SELECT IFNULL(SUM(i.recivedPrincipal-i.hasPrincipal),0) AS investAmount FROM product.`t_invest` i JOIN product.`t_borrow` b ON b.`id`=i.`borrowId` WHERE i.`investor` = '{}' AND b.`borrowStatus`=4 AND b.`borrowType` NOT IN(11,14,15) AND b.`proType` <> 6 and b.`specialArea`<>10 AND DATE(b.`valueDate`)<'2017-05-01' AND TIMESTAMPDIFF(DAY,'{}',NOW())<=365 AND b.`valueDate` < CURRENT_DATE UNION SELECT IFNULL(SUM(i.recivedPrincipal-i.hasPrincipal),0) AS investAmount FROM product.`t_invest` i JOIN product.`t_borrow` b ON b.`id`=i.`borrowId` WHERE i.`investor`='{}' AND b.`borrowStatus`=4 AND b.`borrowType` NOT IN(11,14,15) and b.`specialArea`<>10 AND b.`proType` <> 6 AND TIMESTAMPDIFF(DAY,'{}',NOW())<=IF('{}'<'2017-05-01 00:00:00',365,90) AND TIMESTAMPDIFF(DAY,b.`valueDate`,NOW())<=90 AND DATE(b.`valueDate`)>='2017-05-01' AND b.`valueDate` < CURRENT_DATE) AS tmp;".format(row[0], row[1], row[0], row[1], row[1]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name) 
                res_pcts = self.mysql_query("SELECT IFNULL(SUM(amount),0) FROM (SELECT IFNULL(SUM((i.principal-i.actualPrincipal)/100),0) AS amount FROM pcts.`t_product` p JOIN pcts.`t_invest` i ON p.`id`=i.`productId` WHERE i.`userId` = '{}' AND p.`productStatus`=40 AND DATE(p.`valueDate`)<'2017-05-01' AND TIMESTAMPDIFF(DAY,'{}',NOW())<=365 and p.`valueDate` < CURRENT_DATE UNION SELECT IFNULL(SUM((i.principal-i.actualPrincipal)/100),0) AS amount FROM pcts.`t_product` p JOIN pcts.`t_invest` i ON p.`id`=i.`productId` WHERE i.`userId` = '{}' AND p.`productStatus`=40 AND TIMESTAMPDIFF(DAY,p.`valueDate`,NOW())<=90 AND TIMESTAMPDIFF(DAY,'{}',NOW())<=IF('{}'<'2017-05-01 00:00:00',365,90) AND DATE(p.`valueDate`)>='2017-05-01' and p.`valueDate` < CURRENT_DATE) AS tmp;".format(row[0], row[1], row[0], row[1], row[1]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name) 
            else:
                res = self.mysql_query("SELECT IFNULL(SUM(investAmount),0) FROM (SELECT IFNULL(SUM(i.recivedPrincipal-i.hasPrincipal),0) AS investAmount FROM product.`t_invest` i JOIN product.`t_borrow` b ON b.`id`=i.`borrowId` WHERE i.`investor` = '{}' AND b.`borrowStatus`=4 AND b.`borrowType` NOT IN(11,14,15) and b.`specialArea`<>10 AND DATE(b.`valueDate`)<'2017-05-01' AND TIMESTAMPDIFF(DAY,'{}',NOW())<=730 AND b.`valueDate` < CURRENT_DATE UNION SELECT IFNULL(SUM(i.recivedPrincipal-i.hasPrincipal),0) AS investAmount FROM product.`t_invest` i JOIN product.`t_borrow` b ON b.`id`=i.`borrowId` WHERE i.`investor`='{}' AND b.`borrowStatus`=4 AND b.`borrowType` NOT IN(11,14,15) and b.`specialArea`<>10 AND TIMESTAMPDIFF(DAY,'{}',NOW())<=730 AND DATE(b.`valueDate`)>='2017-05-01' AND b.`valueDate` < CURRENT_DATE) AS tmp;".format(row[0], row[1], row[0], row[1]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name) 
                res_pcts = self.mysql_query("SELECT IFNULL(SUM(amount),0) FROM (SELECT IFNULL(SUM((i.principal-i.actualPrincipal)/100),0) AS amount FROM pcts.`t_product` p JOIN pcts.`t_invest` i ON p.`id`=i.`productId` WHERE i.`userId` = '{}' AND p.`productStatus`=40 AND DATE(p.`valueDate`)<'2017-05-01' AND TIMESTAMPDIFF(DAY,'{}',NOW())<=730 and p.`valueDate` < CURRENT_DATE UNION SELECT IFNULL(SUM((i.principal-i.actualPrincipal)/100),0) AS amount FROM pcts.`t_product` p JOIN pcts.`t_invest` i ON p.`id`=i.`productId` WHERE i.`userId` = '{}' AND p.`productStatus`=40 AND TIMESTAMPDIFF(DAY,'{}',NOW())<=730 AND DATE(p.`valueDate`)>='2017-05-01' and p.`valueDate` < CURRENT_DATE) AS tmp;".format(row[0], row[1], row[0], row[1]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name) 
            amount += res[0][0] if len(res)>0 else 0
            amount += res_pcts[0][0] if len(res_pcts)>0 else 0
            if isNew == 'false':
                res = self.mysql_query("SELECT IFNULL(SUM(i.principal),0) FROM product.t_borrow b,product.t_flex_invest i,product.t_flex f WHERE b.id = i.productId AND b.id = f.productid AND b.borrowStatus > 2 AND b.borrowStatus < 5 AND f.unLockdate > CURRENT_DATE AND b.valueDate < CURRENT_DATE AND b.valueDate < '2017-05-01 00:00:00' AND i.userId = '{}' GROUP BY i.userId".format(row[0]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name)
            else:
                res = self.mysql_query("SELECT IFNULL(SUM(i.principal),0) FROM product.t_borrow b,product.t_flex_invest i,product.t_flex f WHERE b.id = i.productId AND b.id = f.productid AND b.borrowStatus > 2 AND b.borrowStatus < 5 AND f.unLockdate > CURRENT_DATE AND b.valueDate < CURRENT_DATE AND b.valueDate >= '2017-05-01 00:00:00' AND b.valueDate < NOW() AND i.userId = '{}' GROUP BY i.userId".format(row[0]),
                    host=up_db_host, port=up_db_port, db_name=up_db_name)
            amount += res[0][0] if len(res)>0 else 0
        return float(amount)

    def calc_new_earnings_day(self, userId=list()):
        """计算新规每日收益"""
        earnings_day = 0
        for user in userId:
            returnAmount = float(self.get_user_returnAmount('true', user))
            if returnAmount>=2000 and returnAmount<10000:
                amount = returnAmount*0.002/365
            elif returnAmount>=10000 and returnAmount<100000:
                amount = returnAmount*0.003/365
            elif returnAmount>=100000:
                amount = returnAmount*0.004/365
            else:
                amount = 0
            earnings_day += amount
        return float(('%.4f' % earnings_day)[:-2])

    def register_user(self, mobile, password='t1234567', verifyCode='1234'):
        """注册用户"""
        bln.print_log('============通过浏览器注册用户=============')
        wd.go_to(portal_reg_url)
        wd.input_text('//*[@id="mobile"]', mobile)
        wd.input_password('//*[@id="password"]', password)
        wd.input_text('//*[@id="verifyCode"]', verifyCode)
        wd.click_element('id=agree')
        wd.click_button('//*[@id="reg-btn"]') 
        bln.sleep(1) 
        wd.click_button('//*[@id="mobile-code-btn"]')  
        wd.input_text('//*[@id="phoneCode"]', self.get_captcha(mobile))
        wd.click_button('//*[@id="reg-next-btn"]')
        bln.sleep(1)
        wd.wait_until_page_contains('注册成功')
        wd.go_to(portal_url)
        return wd.get_text('//li[@class="user logon"]/a').strip()

    def login_portal(self, username, password='t1234567', code='1234'):
        """登录官网"""
        bln.print_log('===========通过浏览器登录官网==========')
        wd.go_to(portal_login_url)
        wd.input_text('//*[@id="username"]', username)
        wd.input_password('//*[@id="password"]', password)
        wd.input_text('//*[@id="code"]', code)
        wd.select_checkbox('//*[@id="remember"]')
        wd.click_button('//*[@id="login-btn"]')
        try:
            wd.wait_until_page_contains('确认授权', 2)
            wd.click_link('id=confirm-authorization')
        except:
            pass
        wd.wait_until_page_contains('安全退出')
        return wd.get_text('//li[@class="user logon"]/a').strip()

    def login_be(self, username='admin', password='a123456', captcha='1234'):
        """登录BE后台"""
        bln.print_log('================登录BE后台================')
        wd.go_to(be_login_url)
        wd.input_text('id=username', username)
        wd.input_password('id=password', password)
        wd.input_text('id=captcha', 'captcha')
        wd.click_button('id=btn_submit')
        wd.wait_until_page_contains('退出')

    def register_user_inter(self, mobile, password=portal_login_passwd, verifyCode='1234', refferee=''):
        """接口注册用户"""
        reg = 'register'
        bln.print_log('通过接口注册用户{}'.format(mobile))
        requests.create_session(reg, portal_url)     
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        requests.get_request(reg, '/user/register/regcaptcha', headers=headers)
        data = dict(refferee_source='01', mobile=mobile, password=password, verifyCode=verifyCode, refferee=refferee, agree='on')
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        requests.get_request(reg, '/user/register/type/mobile/param/{}'.format(mobile), headers=headers)
        resp = requests.post_request(reg, '/user/register/step1', data, headers=headers)
        resp = requests.post_request(reg, '/user/register/sendcode', 'mobile={}&type=sms'.format(mobile), headers=headers)
        bln.sleep(10)
        code = self.get_captcha(mobile)
        data = dict(refferee_source='01', mobile=mobile, password=password, verifyCode='', refferee=refferee, agree='on', phoneCode=code)
        resp = requests.post_request(reg, '/user/register/commit', data, headers=headers)
        resp = requests.post_request(reg, 'user/register/result', headers=headers)
        bln.should_match_regexp(resp.text, '注册成功', '通过接口注册用户失败')
        resp = requests.get_request(reg, '/user/uasec', headers=headers)
        match, username = bln.should_match_regexp(resp.text, '<span class="account_name">(.*)</span>') 
        return reg, username

    def login_portal_inter(self, username, password=portal_login_passwd, code='1234'):
        """接口登录官网"""
        login = 'login_portal'
        bln.log('接口登录官网 {}'.format(username))
        requests.create_session(login, portal_url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        resp = requests.get_request(login, '/user/login/go', headers=headers)
        match, token_name = bln.should_match_regexp(resp.text, 'name="ooh.token.name" value="(.*)"')
        match, token_value = bln.should_match_regexp(resp.text, 'name="ooh.token.value" value="(.*)"')
        data = {'ooh.token.name': token_name, 'ooh.token.value': token_value, 'username': username, 'password': password, 'code': code}
        headers['Referer'] = portal_url + '/user/login/go'
        requests.get_request(login, '/user/captcha', headers=headers)
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        resp = requests.post_request(login, '/user/login', data=data, headers=headers)
        content = requests.to_json(resp.text)
        bln.should_be_equal_as_strings(content['resultCode'], 0, '通过接口登录官网失败')
        resp = requests.get_request(login, '/user/uasec', headers=headers)
        match, username = bln.should_match_regexp(resp.text, '<span class="account_name">(.*)</span>')
        return login, username

    def real_name(self, name=None, idcard=None):
        """实名认证"""
        wd.go_to(portal_url)
        wd.click_link('我的账户')
        wd.click_element('//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('xpath=//div[@class="column_msg"]//a[@class="showSetting"]')
        wd.input_text('id=smdj_username', name or '自动化测试')      
        wd.input_text('id=smdj_identity_num', idcard or gd.gen_idcard())
        wd.click_element('id=smdj_username')
        bln.sleep(0.5)
        wd.click_element('id=smdj_sub_btn')
        bln.sleep(0.5)
        wd.page_should_contain('已实名') 

    def real_name_inter(self, session):
        """接口实名"""
        idcard = gd.gen_idcard()
        data = dict(realName='自动化测试', idNo=idcard, idType=1, birthday='1998-02-06')
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        resp = requests.post_request(session, '/user/authrname', data, headers=headers)
        content = requests.to_json(resp.text)
        if content['status'] != 1:
            bln.fail('通过接口实名失败')
        return idcard

    # def binding_card_bank(self, card=None, passwd='123456'):
    #     """存管快捷绑卡"""
    #     wd.go_to(binding_bank_url)
    #     wd.input_text('id=banknum', card or self.random_bank_card(62258878))
    #     bln.sleep(0.5)
    #     wd.click_element('id=getcodeBtn')
    #     bln.sleep(0.5)
    #     wd.input_text('name=code', '123456')
    #     wd.click_element('id=getcodeBtn')
    #     wd.click_button('id=submitBtn')
    #     for i in range(10):
    #         try:
    #             wd.page_should_not_contain('请重新绑定')
    #             break
    #         except:
    #             wd.click_element('id=getcodeBtn')
    #             bln.sleep(0.5)
    #             wd.click_element('name=code')
    #             bln.sleep(0.5)
    #             wd.click_button('id=submitBtn')
    #     wd.wait_until_page_contains('您当前正在开立', 10)
    #     wd.click_button('id=getCode')
    #     wd.input_text('name=code', '123456')
    #     wd.click_element('//*[@id="password"]')
    #     bln.sleep(1)
    #     kb.key_input(passwd)
    #     wd.click_element('//*[@id="password_reset"]')
    #     bln.sleep(1)
    #     kb.key_input(passwd)
    #     wd.click_element('//*[@id="readProtocol"]/following-sibling::div')
    #     wd.click_button('开户')
    #     bln.sleep(0.5)
    #     wd.click_link('确定')
    #     wd.page_should_contain('成功开通存管账户', '开通存管账户失败')

    def binding_card_bank_inter(self, session, idcard=None):
        """接口存管绑卡"""
        idcard = idcard or gd.gen_idcard()
        bankid = '62258878' + str(gd.gen_nums(8))
        for i in range(10):
            data = dict(realName='自动化测试', bankTypeName='招商银行', bankCardNo=bankid, idNo=idcard, bankType='CMB', open='true')
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
            resp = requests.post_request(session, '/payment/deposit/account/apply', data, headers=headers)
            resp = requests.post_request(session, '/payment/bankcard/quickPayBindIndex', data, headers=headers)
            resp = requests.post_request(session, '/payment/bankcard/quickPayBindVerify', 'regCode=123456', headers=headers)
            content = requests.to_json(resp.text)
            if content['status'] == 0:
                break
            bln.sleep(1)
        if content['status'] != 0:
            bln.fail('通过接口绑卡失败')

    def binding_card_inter(self, session, idcard=None):
        """接口绑卡"""
        idcard = idcard or gd.gen_idcard()
        bankid = '62258878' + str(gd.gen_nums(8))
        for i in range(10):
            data = dict(realName='自动化测试', bankTypeName='招商银行', bankCardNo=bankid, idNo=idcard, bankType='CMB')
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
            resp = requests.post_request(session, '/payment/bankcard/quickPayBindIndex', data, headers=headers)
            resp = requests.post_request(session, '/payment/bankcard/quickPayBindVerify', 'regCode=123456', headers=headers)
            content = requests.to_json(resp.text)
            if content['status'] == 0:
                break
            bln.sleep(1)
        if content['status'] != 0:
            bln.fail('通过接口绑卡失败')

    # def recharge_bank(self, money=50000, passwd='123456'):
    #     """存管页面充值"""
    #     wd.go_to(recharge_bank_url)
    #     wd.input_text('//*[@id="money"]', money)
    #     wd.click_link('//*[@id="submit-btn"]')
    #     wd.wait_until_page_contains('电子账户充值', 30)
    #     wd.click_element('//*[@id="password"]')
    #     bln.sleep(1)
    #     kb.key_input(passwd)
    #     wd.click_button('确认')
    #     wd.wait_until_page_contains('充值申请成功', 10)
    #     wd.click_link('确定')
    #     wd.page_should_contain('充值成功', '存管充值失败')

    def recharge_inter(self, session, money=50000):
        """接口充值"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        num = int(money/10000)
        money = math.ceil(money%10000)
        for i in range(num):
            data = dict(money=10000, payCode='7ac34a1fb4c3ffffa373395786d45ed7906f9cb9b43c07a1a2c0993a882515a89f259d2d5296de3e1893f59c3a16cc7acd7687381a2d3be6f6e818568a01ef23fd64c7b2384bb04d3761fa167505ba00129b14798207bed35c327828c5af234dc1f741887a13dd2e4f625647f20692f87cde2b0ab6dd8be26091e6987454dbf3')
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            resp = requests.post_request(session, '/payment/recharge/quickpay/code', data, headers=headers)
            data = dict(money=10000, payCode='7ac34a1fb4c3ffffa373395786d45ed7906f9cb9b43c07a1a2c0993a882515a89f259d2d5296de3e1893f59c3a16cc7acd7687381a2d3be6f6e818568a01ef23fd64c7b2384bb04d3761fa167505ba00129b14798207bed35c327828c5af234dc1f741887a13dd2e4f625647f20692f87cde2b0ab6dd8be26091e6987454dbf3', validCode='123456') 
            resp = requests.post_request(session, '/payment/recharge/quickpay/index', data, headers=headers) 
            content = requests.to_json(resp.text)
            if content['status'] != 0:
                bln.fail('通过接口充值失败')
        num = 1 if money != 0 else 0
        for i in range(num):
            data = dict(money=money, payCode='7ac34a1fb4c3ffffa373395786d45ed7906f9cb9b43c07a1a2c0993a882515a89f259d2d5296de3e1893f59c3a16cc7acd7687381a2d3be6f6e818568a01ef23fd64c7b2384bb04d3761fa167505ba00129b14798207bed35c327828c5af234dc1f741887a13dd2e4f625647f20692f87cde2b0ab6dd8be26091e6987454dbf3')
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            resp = requests.post_request(session, '/payment/recharge/quickpay/code', data, headers=headers)
            data = dict(money=money, payCode='7ac34a1fb4c3ffffa373395786d45ed7906f9cb9b43c07a1a2c0993a882515a89f259d2d5296de3e1893f59c3a16cc7acd7687381a2d3be6f6e818568a01ef23fd64c7b2384bb04d3761fa167505ba00129b14798207bed35c327828c5af234dc1f741887a13dd2e4f625647f20692f87cde2b0ab6dd8be26091e6987454dbf3', validCode='123456')
            resp = requests.post_request(session, '/payment/recharge/quickpay/index', data, headers=headers)
            content = requests.to_json(resp.text)
            if content['status'] != 0:
                bln.fail('通过接口充值失败')

    def buy_borrow_inter(self, session, borrowType, amount=0, deadline=0, isDayThe=0, productId=0):
        """
        接口买标
        标的类型可选: 安心牛、散标、月息牛、新手标、转让标、体验标、天天牛、月月牛、周升牛、月升牛、双月牛、季升牛、年升牛、存续牛
        """
        if borrowType == '安心牛':
            where = 'b.`borrowType`=3 AND b.`proType`<>6'
        elif borrowType in ('月息牛', '散标'):
            where = 'b.`borrowType`=0 AND b.`proType`<>6'
        else:
            where = '1=1'
        if borrowType == '月息牛':
            where += ' AND b.`specialArea`=16'
        elif borrowType == '新手标':
            where += ' AND b.`specialArea`=2'
        elif borrowType == '体验标':
            where += ' AND b.`specialArea`=10'
        else:
            where += ' AND b.`specialArea`=1'
        if borrowType == '转让标':
            where += ' AND b.`proType`=6'
        if deadline != 0 or isDayThe != 0:
            where += ' AND b.`deadline`={} AND b.`isDayThe`={}'.format(deadline, isDayThe)
        if borrowType == '周升牛':
            where += " AND b.`borrowTitle` LIKE '%周升%'"
        elif borrowType == '月升牛':
            where += " AND b.`borrowTitle` LIKE '%月升%'"
        elif borrowType == '双月牛':
            where += " AND b.`borrowTitle` LIKE '%双月%'"
        elif borrowType == '季升牛':
            where += " AND b.`borrowTitle` LIKE '%季升%'"
        elif borrowType == '年升牛':
            where += " AND b.`borrowTitle` LIKE '%年升%'"
        elif borrowType == '天天牛' or borrowType == '月月牛':
            where += " AND b.`borrowTitle` LIKE '%{}%'".format(borrowType)
        if borrowType == '存续牛' and isDayThe == 0:
            isDayThe = 2
        elif borrowType == '存续牛' and isDayThe == 1:
            isDayThe = 1
        if borrowType == '存续牛' and deadline == 0 and isDayThe == 2:
            where = '1=1'
        elif borrowType == '存续牛':
            where = 'p.`productTerm`={} and p.`termMode`={}'.format(deadline, isDayThe)
        if borrowType == '存续牛' and amount == 0:
            borrow = self.mysql_query("SELECT p.`id`,p.`productName`,p.`minBuyAmount`/100,p.`exitMode`,(a.`productAmount`-a.`raisedAmount`)/100 FROM pcts.`t_product` p JOIN pcts.`t_product_amount` a ON p.`id`=a.`productId` WHERE {} AND p.`startBuyTime`<NOW() AND p.`productStatus`=20 AND a.`productAmount`-a.`raisedAmount`<>0 AND p.`endBuyTime` IS NULL ORDER BY a.`productAmount`-a.`raisedAmount`;".format(where), 
                host=up_db_host, port=up_db_port, db_name=up_db_name) 
        elif borrowType == '存续牛':
            borrow = self.mysql_query("SELECT p.`id`,p.`productName`,p.`minBuyAmount`/100,p.`exitMode`,(a.`productAmount`-a.`raisedAmount`)/100 FROM pcts.`t_product` p JOIN pcts.`t_product_amount` a ON p.`id`=a.`productId` WHERE {} AND p.`productStatus`=20 AND p.`startBuyTime`<NOW() AND a.`productAmount`-a.`raisedAmount`>={} AND (p.`endBuyTime` IS NULL OR p.`endBuyTime`>NOW()) ORDER BY a.`productAmount`-a.`raisedAmount` DESC;".format(where, amount), 
                host=up_db_host, port=up_db_port, db_name=up_db_name)
        elif amount == 0:
            borrow = self.mysql_query("SELECT b.`id`, b.`borrowTitle`, b.`minTenderedSum`, b.`borrowWay`, b.`borrowAmount`-b.`hasInvestAmount` FROM product.`t_borrow` b WHERE {} AND b.`borrowStatus`=2 AND b.`borrowAmount`-b.`hasInvestAmount` <> 0 ORDER BY b.`borrowAmount`-b.`hasInvestAmount`;".format(where),
                host=up_db_host, port=up_db_port, db_name=up_db_name)
        else:
            borrow = self.mysql_query("SELECT b.`id`, b.`borrowTitle`, b.`minTenderedSum`, b.`borrowWay`, b.`borrowAmount`-b.`hasInvestAmount` FROM product.`t_borrow` b WHERE {} AND b.`borrowStatus`=2 AND b.`borrowAmount`-b.`hasInvestAmount`>={} ORDER BY b.`borrowAmount`-b.`hasInvestAmount` DESC;".format(where, amount),
                host=up_db_host, port=up_db_port, db_name=up_db_name)
        if borrowType == '存续牛' and productId != 0:
            borrow = self.mysql_query("SELECT p.`id`,p.`productName`,p.`minBuyAmount`/100,p.`exitMode`,(a.`productAmount`-a.`raisedAmount`)/100 FROM pcts.`t_product` p JOIN pcts.`t_product_amount` a ON p.`id`=a.`productId` WHERE p.id={};".format(productId),
            host=up_db_host, port=up_db_port, db_name=up_db_name)
        elif borrowType != '存续牛' and productId != 0:
            borrow = self.mysql_query("SELECT b.`id`, b.`borrowTitle`, b.`minTenderedSum`, b.`borrowWay`, b.`borrowAmount`-b.`hasInvestAmount` FROM product.`t_borrow` b WHERE b.id={};".format(productId), 
                host=up_db_host, port=up_db_port, db_name=up_db_name)
        bln.should_not_be_empty(borrow, '无可买{}标的, 请先发标'.format(borrowType))
        borrowId = borrow[0][0]
        borrowTitle = borrow[0][1]
        minTenderedSum = borrow[0][2]
        borrowWay = borrow[0][3]
        amountLeft = borrow[0][4]
        amount = amountLeft if amount == 0 else amount
        bln.print_log('======通过接口购买产品{}======'.format(borrowTitle))
        if borrowType == '周升牛' or borrowType == '月升牛' or borrowType == '双月牛' or borrowType == '季升牛' or borrowType == '年升牛':
            uri = '/product/flex/detail/{}'.format(borrowId)
        elif borrowType == '体验标':
            uri = '/product/taste/detail/{}'.format(borrowId)
        elif borrowType == '存续牛':
            uri = '/product/duration/detail/{}'.format(borrowId)
        else:
            uri = '/product/bid/{}'.format(borrowId)
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        resp = requests.get_request(session, uri, headers=headers)
        match, token_name = bln.should_match_regexp(resp.text, 'name="ooh.token.name" value="(.*)"')  
        match, token_value = bln.should_match_regexp(resp.text, 'name="ooh.token.value" value="(.*)"')  
        resp = requests.get_request(session, '/product/financial/coupon/list', headers=headers) if borrowType == '体验标' else None
        content = list()
        if resp is not None:
            content = requests.to_json(resp.text)
        if resp is not None and len(content) > 0:
            coupon = content[0]
        elif borrowType == '体验标':
            bln.fail('没有理财金券, 请先为用户发放理财金券')
        if borrowType == '体验标':
            data = {'ooh.token.name': token_name, 'ooh.token.value': token_value, 'buyAmount': coupon['couponAmount'],
                    'platform': 1, 'productId': borrowId, 'couponId': coupon['couponId'], 'paramMap.platform': 1,
                    'paramMap.id': borrowId, 'paramMap.minTenderedSum': minTenderedSum, 'paramMap.repayDate': '', 
                    'paramMap.borrowWay': borrowWay, 'paramMap.borrowTitle': borrowTitle} 
        else:
            data = {'ooh.token.name': token_name, 'ooh.token.value': token_value, 'buyAmount': amount, 'platform':1,
                    'productId': borrowId, 'bonusId': '', 'addRateId': '', 'createAutoInvestPlan': 'false', 'currentId': 2,
                    'accrualTime': '', 'valueDays': 1}
        requests.post_request(session, '/cms/assess/setDefault/EFCA1', headers=headers)
        if borrowType == '存续牛':
            resp = requests.post_request(session, '/product/trade/new/buy', data=data, headers=headers)  
        else:
            resp = requests.post_request(session, '/product/trade/buy', data=data, headers=headers)
        bln.should_match_regexp(resp.text, '您已成功购买', '通过接口买标失败')
        return borrowId, amountLeft

    def login_be_inter(self, username='admin', password='c43db7358fba1a0566ab9b70996b7da4356858080b2fd095de0b771385dc7edca64a7bef8402688b071434a3699c14d42c29b7bfdf9987b12cedaef1ac251ef3cb943c71ebb2cd54f698cb2dfd59a4a8762c17490e3d9a8d40fd46d70b3adf9b27c32b6a91f9a00724e27ab70cd837a3ce7e11d72b28a1bbcee3faa68b662375', code='1234'):
        """接口登录BE"""
        login = 'login_be'
        requests.create_session(login, be_url)
        data = dict(username=username, password=password, code=code)
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        resp = requests.post_request(login, '/be/login', data=data, headers=headers)
        bln.should_match_regexp(resp.text, username, '通过接口登录BE失败')
        return login    # 返回登录后session

    def send_financial_inter(self, username, amount=1000):
        """接口发放理财金"""
        session = self.login_be_inter() 
        data = dict(userName=username, amount=amount, source='自动化测试', activateDate='2017-02-24 00:00:00', 
                  expireDate='2017-12-24 23:59:59', fundAccount='31005')
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        resp = requests.post_request(session, '/be/bonus/experience/coupon/singleSend', data=data, headers=headers)
        content = requests.to_json(resp.text)
        bln.should_be_equal_as_integers(content['result'], 1)
        resp = requests.get_request(session, '/be/bonus/experience/coupon/toSend.json?userName={}&page=1&rows=20'.format(username), headers=headers)
        content = requests.to_json(resp.text)
        ids = content['rows'][0]['id']
        data = dict(ids=ids, status=1)
        resp = requests.post_request(session, '/be/bonus/experience/coupon/batchUpdate', data=data, headers=headers)
        content = requests.to_json(resp.text)
        bln.should_be_equal_as_integers(content['result'], 1, '发送理财金失败')

    def exec_job_inter(self, jobName):
        """接口执行定时任务"""
        session = self.login_be_inter()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        resp = requests.get_request(session, '/be/task/list.json?systemId=&keyWord={}&startHour=&endHour=&page=1&rows=20'.format(jobName), headers=headers)
        content = requests.to_json(resp.text)
        bln.should_be_equal_as_integers(content['total'], 0, '定时任务{}不存在'.format(jobName))
        ids = content['rows'][0]['id']
        base64Name = content['rows'][0]['base64Name']
        resp = requests.get_request(session, '/be/task/trigger/{}.json?id={}'.format(base64Name, ids), headers=headers)
        bln.should_be_equal_as_strings(resp.text, '"success"', '执行定时任务{}失败'.format(jobName))

    def buy_borrow_amount_left_inter(self, borrowType, productId, amount, username='af88', password='74b0c4f3eebee15bbbd9c271635f6943dc517b15dab94266f4651c6189839d94c80ab608e9763d9fd78680fd209afe81681b1c3cd154e0bb5ae946d43ae78a1cdd999f115910786531a4f8e728e879345a393a1a79dfd99019804f8c17f4a1fe1b37ee938037126c5874ce7901eaf2d9843da1ea4b59a352e5f515c0080dbc9a'):
        """买满指定标"""
        bln.print_log('买满指定标的所有剩余金额')
        session = self.login_portal_inter(username=username, password=password)
        try:
            self.binding_card_inter(session)
        except Exception as e:
            pass
        self.recharge_inter(session, amount)
        self.buy_borrow_inter(session, borrowType, productId=productId)

    def publish_borrow_inter(self, amount=10000, btype='散标', host=host):
        """接口发标"""
        product = 'publish_product'
        requests.create_session(product, 'http://172.20.20.160:9788')
        tyb = 0 if btype == '散标' else 1
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        if btype == '存续牛':
            data = dict(account=1, repayMode=0, borrowAmount=amount, period=12, monthFee=20.00, host=host)
            resp = requests.post_request(product, '/interface/product/loan/', data, headers=headers)
            data = dict(productnum=1, intest=6.00, productTerm=3, repayMode=0,
                        zr=0, lockTerm=1, host=host)
            resp = requests.post_request(product, '/interface/product/pcts/', data, headers=headers)
        else:
            data = dict(borrowAmount=amount, annualRate=8.00, paymentMode=3, specialArea=1, assClaim=0, isAutoBid=1,
                        holdMonth=1, optionsRadios=1, deadline=12, host=host, tyb=tyb)
            resp = requests.post_request(product, '/interface/product/listing/', data, headers=headers)
        bln.sleep(3)
        return resp

    def channel_register(self, url, platform='PC', mobile=None, channel_index='02c861126c3957ac', word='AutoTest'):
        """渠道页注册"""
        url = '{}?channelIndex={}&word={}'.format(url, channel_index, word)
        mobile = mobile or self.random_mobile()
        wd.go_to(url)
        if platform == 'PC':
            wd.input_text('//*[@id="mobile"]', mobile)
            wd.input_password('//*[@id="password"]', 't1234567')
            wd.input_text('//*[@id="imgCode"]', '123456')
            wd.click_element('//span[text()="获取验证码"]')
            code = self.get_captcha(mobile)
            wd.input_text('//*[@id="vilidataNum"]', code)
            wd.click_link('//*[@id="reg_btn"]')
            try:
                wd.page_should_contain('欢迎来到')
            except:
                wd.page_should_contain('注册成功')
        else:
            wd.input_text('//*[@id="mobile"]', mobile)
            wd.input_password('//*[@id="password"]', 't1234567')
            wd.input_text('//*[@id="imgCode"]', '123456')
            wd.click_link('获取验证码')
            code = self.get_captcha(mobile)
            wd.input_text('//*[@id="code"]', code)
            wd.click_link('//*[@id="step_one"]')
            try:
                wd.page_should_contain('欢迎来到')
            except:
                wd.page_should_contain('注册成功')

    def channel_template_register(self, url, platform='PC', mobile=None, word='AutoTest_template'):
        """渠道模板页注册"""
        url = '{}?word={}'.format(url, word)
        mobile = mobile or self.random_mobile()
        wd.go_to(url)
        if platform == 'PC':
            wd.input_text('//*[@id="mobile"]', mobile)
            wd.input_password('//*[@name="password"]', 't1234567')
            wd.input_text('//*[@id="imgCode"]', '123456')
            wd.click_link('获取验证码')
            code = self.get_captcha(mobile)
            wd.input_text('//*[@name="phoneCode"]', code)
            wd.click_element('//span[@class="check_icon not_agree"]')
            wd.click_link('//*[@id="regBtn"]')
            wd.page_should_contain('欢迎来到')
        else:
            wd.click_link('去注册')
            wd.input_text('//*[@id="mobile"]', mobile)
            wd.input_password('//*[@id="password"]', 't1234567')
            wd.input_text('//*[@id="imgCode"]', '123456')
            wd.click_link('获取验证码')
            code = self.get_captcha(mobile)
            wd.input_text('//*[@id="code"]', code)
            wd.click_link('注册领好礼')
            wd.page_should_contain('会员中心')
