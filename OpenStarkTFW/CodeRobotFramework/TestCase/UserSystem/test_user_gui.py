# coding=utf8
import unittest
from Core.keys import webdriver as wd
from Core.keys import builtin as bln
from Core.keys import gen_data as gd
from Core.keys import requests
# from Core.keys import keyboard as kb
from Library.common_library import CommonLibrary
from Resource.Variables.common import *


class UserGUI(unittest.TestCase):
    """用户模块自动化用例 GUI版"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.driver = wd  # 用于用例执行失败后自动截图, 变量为固定格式, 请勿更改, 不需要失败截图可注释

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'debug', '已忽略执行')
    def test_U0000(self):
        """Debug"""
        pass

    @unittest.skip('已取消')
    def test_U0001(self):
        """U0001_用户名注册
        操作步骤:
        1、进入注册页面
        2、输入6-16位账户名(非数字开头的英文、下划线和数字组合)、手机号(13、14、15、18、17开头)、登录密码(8-20位字符，至少含数字、大写字母、小写字母、符号中的2种)、验证码(6位)、选择推荐人，输入系统中存在的推荐人用户名或手机号
        3、勾选‘我已阅读并同意《小牛在线服务协议》’
        4、点击【下一步】
        5、点击【获取验证码】
        6、输入6位验证码，点击【确认】
        ======
        预期结果:         
        注册成功
        """
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0002(self):
        """U0002_手机号码注册
        操作步骤:
        1、进入注册页面
        2、输入手机号(13、14、15、18、17开头)、登录密码(8-20位字符，至少含数字、大写字母、小写字母、符号中的2种)、验证码(6位)、选择推荐人，输入系统中存在的推荐人用户名或手机号
        3、勾选‘我已阅读并同意《小牛在线服务协议》’
        4、点击【下一步】
        5、点击【获取验证码】
        6、输入6位验证码，点击【确认】
        ======
        预期结果:
        1、打开注册页面并正确显示页面元素信息
        2、各项输入项校验正确
        3、成功勾选
        4、跳转到验证码获取页面
        5、接收到6位验证码
        6、注册成功
        """
        mobile = self.comlib.random_mobile()
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser)
        username = self.comlib.register_user(mobile)
        bln.should_start_with(username, 'xn', '通过手机号码注册失败')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0003(self):
        """U0003_用户名登录
        操作步骤:
        1、进入登录页面
        2、输入6-16位账户名(非数字开头的英文、下划线和数字组合)、登录密码(8-20位字符，至少含数字、大写字母、小写字母、符号中的2种)、验证码(6位)
        3、点击【登录】
        ======
        预期结果:
        1、登录页面各元素都正确
        2、输入成功
        3、登录成功，返回首页
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile) 
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        user = self.comlib.login_portal(username) 
        bln.should_start_with(username, 'xn', '通过用户名登录失败')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0004(self):
        """U0004_手机号登录
        操作步骤:
        1、进入登录页面
        2、输入系统中存在的11位手机号(13、14、15、18、17开头)、登录密码(8-20位字符，至少含数字、大写字母、小写字母、符号中的2种)、验证码(6位)
        3、点击【登录】
        ======
        预期结果:
        1、登录页面各元素都正确
        2、输入成功
        3、登录成功，返回首页
        """
        mobile = self.comlib.random_mobile()
        self.comlib.register_user_inter(mobile)    
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        username = self.comlib.login_portal(mobile) 
        bln.should_start_with(username, 'xn', '通过手机号码登录失败')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0005(self):
        """U0005_邮箱登录
        操作步骤:
        1、进入登录页面
        2、输入系统中存在的邮箱(中间有@符)、登录密码(8-20位字符，至少含数字、大写字母、小写字母、符号中的2种)、验证码(6位)
        3、点击【登录】
        ======
        预期结果:
        1、登录页面各元素都正确
        2、输入成功
        3、登录成功，返回首页
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        email = self.comlib.random_email()
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}     
        data = dict(email=email)
        requests.post_request(session, '/user/isemailexist', data, headers=headers)
        data = dict(email=email, sendType=2, bizCode=3, msgTemp='ese')
        requests.post_request(session, '/user/sendverifycode_nm', data, headers=headers)
        bln.sleep(1)
        code = self.comlib.get_captcha(email, 'email')
        data = dict(email=email, verifyCode=code)
        resp = requests.post_request(session, '/user/setemail', data, headers=headers)
        content = requests.to_json(resp.text)
        bln.should_be_equal_as_integers(content['status'], 1, '接口设置邮箱失败')
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        username = self.comlib.login_portal(email)
        bln.should_start_with(username, 'xn', '通过邮箱登录登录失败')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0006(self):
        """U0006_账户安全-实名认证
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、实名认证列点击'设置'
        3、输入真实姓名(2-4位汉字)、证件号码(18位数字,最后1位可用字母)、出生日期(YYYY-MM-DD)
        4、点击【确定】
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入实名认证设置页面，各元素显示正确
        3、校验成功
        4、实名认证设置成功，设置链接变成'已实名'
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_element('//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('xpath=//div[@class="column_msg"]//a[@mytarget="smdj_rz"]')
        wd.input_text('id=realName', '张三')      
        idcard = gd.gen_idcard()
        wd.input_text('id=idnumber', idcard)
        card = self.comlib.random_bank_card(62258878)
        wd.input_text('id=banknum', card)
        wd.select_from_list_by_value('//*[@id="bindcardForm"]//select', 'CMB')
        bln.sleep(0.5)
        wd.click_element('id=getcodeBtn')
        bln.sleep(0.5)
        wd.click_element('name=code')
        wd.input_text('name=code', '123456')
        bln.sleep(0.5)
        wd.click_button('id=submitBtn')
        for i in range(10):
            try:
                wd.page_should_not_contain('请重新绑定')
            except:
                wd.click_element('id=getcodeBtn')
                bln.sleep(0.5)
                wd.click_element('name=code')
                bln.sleep(0.5)
                wd.click_button('id=submitBtn')
        wd.page_should_contain('成功绑定银行卡') 
        wd.close_browser()

    @unittest.skip('已更换为存管绑卡开户')
    def test_U0007_skip(self):
        """U0007_账户安全-银行卡快捷认证
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、银行卡认证列点击'设置'
        3、选择开户银行
        4、根据各银行的卡号规则，输入正确的银行卡号(16、18、19、22位)
        5、输入银行预留手机号(13、14、15、18、17开头的11数字)
        6、点击【免费获取】获取验证码
        7、输入接收到的验证码
        8、勾选‘我已阅读并同意《资金管理服务协议》’
        9、点击【立即绑定】
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入银行卡认证设置页面，系统自动获取姓名及证件号码且不可修改，其他各元素显示正确
        3、可选择支持的开户银行
        4、输入成功
        5、输入成功
        6、预留手机号接收4位验证码
        7、输入成功
        8、勾选成功
        9、绑卡成功
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        self.comlib.real_name_inter(session)
        card = self.comlib.random_bank_card(62258878)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_link('银行卡管理')
        wd.input_text('id=banknum', card)
        bln.sleep(1)
        wd.click_element("xpath=//div[@class='selected']")
        bln.sleep(1)
        wd.click_element('//span[@class="getcode clk"]')
        bln.sleep(1)
        wd.input_text('id=bk_code', '123456')
        wd.click_link('立即绑定')
        for i in range(10):
            try:
                wd.page_should_not_contain('请重新绑定')
                break
            except:
                wd.click_element('//span[@class="getcode clk"]')
                bln.sleep(0.5)
                wd.click_element('id=bk_code')
                bln.sleep(0.5)
                wd.click_link('立即绑定')
        bln.sleep(1)
        wd.page_should_contain('已开通认证支付')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0007(self):
        """U0007_账户安全-银行卡存管快捷认证
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、银行卡认证列点击'设置'
        3、选择开户银行
        4、根据各银行的卡号规则，输入正确的银行卡号(16、18、19、22位)
        5、输入银行预留手机号(13、14、15、18、17开头的11数字)
        6、点击【免费获取】获取验证码
        7、输入接收到的验证码
        8、勾选‘我已阅读并同意《资金管理服务协议》’
        9、点击【立即绑定】
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入银行卡认证设置页面，系统自动获取姓名及证件号码且不可修改，其他各元素显示正确
        3、可选择支持的开户银行
        4、输入成功
        5、输入成功
        6、预留手机号接收4位验证码
        7、输入成功
        8、勾选成功
        9、绑卡成功
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        self.comlib.real_name_inter(session)
        card = self.comlib.random_bank_card(62258878)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser)
        self.comlib.login_portal(username)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_link('银行卡管理')
        wd.input_text('id=banknum', card)
        wd.select_from_list_by_value('//*[@id="bindcardForm"]//select', 'CMB')
        bln.sleep(0.5)
        wd.click_element('id=getcodeBtn')
        bln.sleep(0.5)
        wd.click_element('name=code')
        wd.input_text('name=code', '123456')
        bln.sleep(0.5)
        wd.click_button('id=submitBtn')
        for i in range(10):
            try:
                wd.page_should_not_contain('请重新绑定')
            except:
                wd.click_element('id=getcodeBtn')
                bln.sleep(0.5)
                wd.click_element('name=code')
                bln.sleep(0.5)
                wd.click_button('id=submitBtn')
        # wd.wait_until_page_contains('您当前正在开立', 10)
        # wd.click_button('id=getCode')
        # wd.input_text('name=code', '123456')
        # wd.click_element('//*[@id="password"]')
        # kb.key_input('123456')
        # bln.sleep(0.5)
        # wd.click_element('//*[@id="password_reset"]')
        # kb.key_input('123456')
        # bln.sleep(0.5)
        # wd.click_element('//*[@id="readProtocol"]/following-sibling::div')
        # wd.click_button('开户')
        # bln.sleep(0.5)
        # wd.click_link('确定')
        wd.page_should_contain('成功绑定银行卡')
        wd.close_browser()

    @unittest.skip('新版已取消此功能')
    def test_U0008(self):
        """U0008_账户安全-银行卡打款验证
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、银行卡认证列点击'设置'
        3、点击‘打款验证方式绑卡’
        4、选择银行，根据已选的银行卡号规则，输入正确的银行卡号(16、18、19、22位)
        5、点击【提交】
        6、在卡号提醒页面，点击【提交】
        7、输入金额，点击【提交】
        8、点击【确定】
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入银行卡认证设置页面，系统自动获取姓名及证件号码且不可修改，其他各元素显示正确
        3、进入打款验证方式绑卡页面，自动获取开户名且不可修改，其他各元素显示正确
        4、选择及输入成功
        5、弹出卡号提醒核对页面
        6、提交成功并发送一条带有金额的短信至手机，进入到绑卡最后一步骤页面
        7、提示‘恭喜您，绑卡成功’
        8、回到的我的银行卡页面，显示已经绑卡成功的卡信息
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        self.comlib.real_name_inter(session)
        card = self.comlib.random_bank_card(62258878)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_link('银行卡管理')
        wd.click_link('打款验证方式绑卡')
        wd.input_text('id=cardNo', card)
        wd.click_element('xpath=//*[@id="bankCode"]')
        wd.click_element('xpath=//*[@id="bankCode"]/ul/li[5]')
        wd.click_link('id=submitToCheck')
        wd.wait_until_element_is_visible('id=coverdiv1') 
        wd.click_link('id=submitToCheckBank')
        wd.wait_until_page_contains('汇款到账结果正在处理中', 10, '打款绑卡失败')
        res = self.comlib.mysql_query("SELECT r.`userId`,r.`amount`,r.`status` FROM payment.`t_bind_card_record` r WHERE r.`amount` IS NOT NULL AND r.`userName`='{}' ORDER BY r.`id` DESC LIMIT 1;".format(username))
        userId = res[0][0]
        amount = res[0][1]
        self.comlib.mysql_update("UPDATE payment.`t_bind_card_record` r SET r.`status`=3 WHERE r.`userId`={} AND r.`amount`={};".format(userId, amount))    
        amount = str(amount)
        wd.reload_page()
        wd.input_text('id=moneyForCheck', amount)
        wd.click_link('id=submitButtonV')
        bln.sleep(1)
        wd.page_should_contain('成功绑定银行卡')
        wd.close_browser()
        
    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0009(self):
        """U0009_账户安全-设置交易密码
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、交易密码列点击'请设置'
        3、点击【获取验证码】，输入6位验证码，点击【下一步】
        4、输入8-20位字符的密码及确认密码，点击【下一步】
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入密码设置步骤-验证身份
        3、将收到的验证码输入并流转到交易密码设置页面
        4、设置成功
        """
        global mobile
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
        bln.sleep(1)
        wd.click_element('xpath=//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('//div[@class="column_msg"]//a[@mytarget="step_1"]')
        wd.click_element("xpath=//a[@class='get_code inline_block']//span[@class='get_code_text']")
        bln.sleep(3)
        code = self.comlib.get_captcha(mobile)
        wd.input_text('id=jymm_rz_step1_phonecode', code)
        wd.click_link('id=jymm_rz_step1_submit')
        bln.sleep(1)
        wd.input_text('id=jymm_rz_step2_new_pwd', 'a1234567')
        wd.input_text('id=jymm_rz_step2_new_pwd_qr', 'a1234567')
        wd.click_link('id=jymm_rz_step2_submit')
        bln.sleep(1)
        wd.page_should_contain('设置密码成功')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0010(self):
        """U0010_账户安全-修改交易密码
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、交易密码列点击'修改'
        3、输入原交易密码、新交易密码、确认新密码，点击【获取验证码】，输入6位验证码，点击【确认】
        4、提现操作输入新密码
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入交易密码修改步骤
        3、修改交易密码成功
        4、提现成功
        """
        global mobile
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(mobile)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_element('xpath=//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('xpath=//div[@class="column_msg"]//a[@mytarget="jymm_xg"]')
        wd.input_text('id=jymm_xg_old_trapwd', 'a1234567')
        wd.input_text('id=jymm_xg_trapwd', '123456aa')
        wd.input_text('id=jymm_xg_trapwd_qr', '123456aa')
        wd.click_element('id=jymm_xg_getcode')
        bln.sleep(3)
        code = self.comlib.get_captcha(mobile)
        wd.input_text('id=jymm_xg_code', code)
        wd.click_link('id=jymm_xg_sub_btn')
        bln.sleep(1)
        wd.element_should_not_be_visible('id=jymm_xg_old_trapwd')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0011(self):
        """U0011_账户安全-找回交易密码
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、交易密码列点击'找回'
        3、输入原交易密码，点击【获取验证码】，输入6位验证码，点击【确认】
        4、输入新密码、确认新密码，点击【下一步】
        5、提现操作输入新密码
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入交易密码修改步骤-身份验证
        3、进入修改密码步骤-修改密码
        4、设置成功
        5、提现成功
        """
        global mobile
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(mobile)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_element('xpath=//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('xpath=//div[@class="column_msg"]//a[@mytarget="step_1"]')
        wd.click_link('id=jymm_zh_step1_getcode')
        bln.sleep(3)
        code = self.comlib.get_captcha(mobile)
        wd.input_text('id=jymm_zh_step1_phnoecode', code)
        wd.click_link('id=jymm_zh_step1_submit')
        bln.sleep(1)
        wd.input_text('id=jymm_zh_step2_newpwd', '123456qq')       
        wd.input_text('id=jymm_zh_step2_newpwd_qr', '123456qq')        
        wd.click_link('id=jymm_zh_step2_submit') 
        bln.sleep(1)
        wd.page_should_contain('设置密码成功')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0012(self):
        """U0012_账户安全-修改登录密码
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、登录密码列点击'修改'
        3、输入原登录密码、新登录密码、确认新密码，点击【获取验证码】，输入6位验证码，点击【确认】
        4、退出系统，用新密码重新登录系统
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入登录密码修改步骤
        3、修改登录密码成功
        4、登陆成功
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(mobile)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_element('xpath=//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('xpath=//div[@class="column_msg"]//a[@mytarget="dlmm_xg"]')
        wd.input_text('id=dlmm_xg_old_pwd', 't1234567')
        wd.input_text('id=dlmm_xg_new_pwd', 't12345678')
        wd.input_text('id=dlmm_xg_new_pwd_qr', 't12345678')
        wd.click_element("xpath=//a[@id='dl_xg_code']")
        bln.sleep(3)
        code = self.comlib.get_captcha(mobile)
        wd.input_text('id=dl_xg_cdtx', code)
        wd.execute_javascript('scrollTo(0,document.body.scrollHeight)')
        wd.click_link('//*[@id="dlmm_xg_submit"]')
        bln.sleep(1)
        wd.page_should_contain('恭喜您修改登录密码成功，请重新登录')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0013(self):
        """U0013_账户安全-设置邮箱
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、认证邮箱列点击'请设置'
        3、输入邮箱地址(带@且有效的地址)，点击【获取验证码】，输入6位验证码，点击【下一步】
        4、用邮箱登录系统
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入邮箱设置页面
        3、设置成功
        4、登录成功
        """
        global mobile
        global email
        mobile = self.comlib.random_mobile()
        email = self.comlib.random_email()
        session, username = self.comlib.register_user_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(mobile)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_element('xpath=//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('xpath=//div[@class="column_msg"]//a[@mytarget="yxrz_rz"]')
        wd.input_text('id=yxrz_rz_email', email)
        wd.click_link('id=yxrz_rz_getecode')
        bln.sleep(3)
        code = self.comlib.get_captcha(email, email)
        wd.input_text('id=yxrz_rz_ecode', code)
        wd.execute_javascript('scrollTo(0,document.body.scrollHeight)')
        wd.click_link("xpath=//div[@class='yxrz_rz']//a[@class='sbm_btn inline_block']")
        bln.sleep(1)
        wd.element_should_not_be_visible('id=yxrz_rz_ecode')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0014(self):
        """U0014_账户安全-修改邮箱
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、认证邮箱列点击'修改'
        3、输入交易密码，点击【获取验证码】，输入6位验证码，点击【下一步】
        4、输入新的邮箱，点击【下一步】
        5、用新的邮箱地址登录系统
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入邮箱修改-验证身份页面
        3、进入邮箱修改页面
        4、修改成功
        5、登录成功
        """
        global mobile
        global email
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(mobile)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_element('xpath=//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('xpath=//div[@class="column_msg"]//a[@mytarget="use_email"]')
        wd.click_link('id=yxrz_changeToPhoneCheck')
        wd.click_link('id=yxrz_xg_step1_getpcode')
        wd.execute_javascript('scrollTo(0,document.body.scrollHeight)')
        bln.sleep(3)
        code = self.comlib.get_captcha(mobile)
        wd.input_text('id=yxrz_xg_step1_pcode', code)
        wd.click_link('id=yxrz_xg_step1_submit_use_phone')
        email = self.comlib.random_email()
        bln.sleep(1)
        wd.input_text('id=yxrz_xg_step2_email', email)
        wd.click_link('id=yxrz_xg_step2_getemailcode')
        bln.sleep(3)
        code = self.comlib.get_captcha(email, email)
        wd.input_text('id=yxrz_xg_step2_emailcode', code)
        wd.click_link('id=yxrz_xg_step2_submit')
        bln.sleep(1)
        wd.page_should_contain('修改成功')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0015(self):
        """U0015_账户安全-设置紧急联系人
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、紧急联系人列点击'请设置'
        3、选择联系人关系、输入联系人姓名及联系人手机号(13、14、15、18、17开头的11数字)，点击【确认】
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入邮箱设置页面
        3、设置成功
        """
        global mobile
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(mobile)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_element('xpath=//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('xpath=//div[@class=\'column\']//a[@mytarget="jjlxr_rz"]')
        wd.click_element('id=jjlxr_rz_type')  
        wd.click_element('xpath=//*[@id="jjlxr_form"]//ul[@class="options"]//li[@val="1"]')
        wd.execute_javascript('scrollTo(0,document.body.scrollHeight)')
        wd.input_text('id=jjlxr_rz_name', '李思')
        wd.input_text('id=jjlxr_rz_mobile', '13048884557')
        wd.click_link('id=jjlxr_rz_submit')
        bln.sleep(1)
        wd.page_should_contain('李')   
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0016(self):
        """U0016_账户安全-修改紧急联系人
        操作步骤:
        1、已登录系统，点击我的账户-账户安全
        2、紧急联系人列点击'修改'
        3、点击【下一步】，选择联系人关系、输入联系人姓名及联系人手机号(13、14、15、18、17开头的11数字)，点击【确认】
        ======
        预期结果:
        1、进入账户安全页面，各信息显示正确
        2、进入紧急联系人确认页面，各信息显示正确
        3、修改成功
        """
        global mobile
        session, username = self.comlib.login_portal_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(mobile)
        wd.click_link('我的账户')
        try:
            wd.page_should_not_contain('知道了')
        except:
            wd.click_button('知道了')
            bln.sleep(0.5)
        wd.click_element('xpath=//ul[@class="g-cf left-menu"]//li[@data-type="datum"]')
        wd.click_link('xpath=//div[@myid="contact"]//a[@class="showSetting"]') 
        wd.execute_javascript('scrollTo(0,document.body.scrollHeight)')
        wd.click_link('id=jjlxr_xg_step1_submit') 
        wd.click_element('id=jjlxr_xg_step2_type')
        wd.click_element('xpath=//*[@id="jjlxr_form"]//ul[@class="options"]//li[@val="1"]')  
        wd.input_text('id=jjlxr_xg_step2_name', '李思思')
        wd.input_text('id=jjlxr_xg_step2_mobile', '13048884557')
        wd.click_link('id=jjlxr_xg_step2_submit')
        bln.sleep(1)
        wd.page_should_contain('修改成功')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0017(self):
        """U0017_会员首页
        操作步骤:
        1、进入会员体系首页
        2、查看页面元素
        ======
        预期结果:
        1、展示当前用户成长值、积分
        2、会员等级展示当前等级的会员权益
        3、展示成长任务链接
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser)
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        bln.print_log('检查成长值和积分')
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name)
        point = self.comlib.mysql_query("SELECT p.`balance` FROM activity.`t_point_account` p WHERE p.`username`='{}';".format(username))
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        jifen = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[2]')
        score = score[0][0] if len(score) > 0 else 0
        point = point[0][0] if len(point) > 0 else 0
        bln.should_be_equal_as_integers(score, upgrade, '成长值不对')
        bln.should_be_equal_as_integers(point, jifen, '积分值不对')
        bln.print_log('检查会员权益')
        one = wd.get_text('//*[@id="rights-slide-list"]/li[@class="right-item bouns enable"]/a')
        two = wd.get_text('//*[@id="rights-slide-list"]/li[@class="right-item interestVoucher enable"]/a')
        three = wd.get_text('//*[@id="rights-slide-list"]/li[@class="right-item birthdayGift enable"]/a')
        bln.should_be_equal(one, '专享红包')
        bln.should_be_equal(two, '增利券')
        bln.should_be_equal(three, '会员生日好礼')
        bln.print_log('检查任务链接')
        wd.click_link('http://www.xiaoniu88.com/user/member/tasks/task')
        bln.sleep(2)
        wd.select_window('会员任务—小牛在线')
        bln.sleep(1)
        wd.page_should_contain('成长经历')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0018(self):
        """U0018_会员等级
        操作步骤:
        1、点击【会员等级】链接
        ======
        预期结果:
        1、显示当前用户的成长值
        2、显示【去赚取成长值】按钮，点击跳转成长任务界面
        3、显示各项成长任务对应成长值
        4、显示成长值的计算方式
        5、显示会员升级与保级说明
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile) 
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser)
        self.comlib.login_portal(username, 't1234567') 
        wd.click_link('会员中心')
        wd.click_link('会员等级')
        wd.page_should_contain('成长值 = 待收初始化成长值+新手任务成长值+进阶任务成长值+投标任务成长值+推荐任务成长值') 
        bln.print_log('检查成长值')    
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        upgrade = wd.get_text('//div[@class="point-value"]//a')
        score = score[0][0] if len(score) > 0 else 0
        bln.should_be_equal_as_integers(score, upgrade, '成长值不对') 
        bln.print_log('检查去赚成长值按钮')    
        wd.click_link('去赚成长值')    
        wd.select_window('会员任务—小牛在线') 
        bln.sleep(1)   
        wd.page_should_contain('成长经历')    
        wd.close_window()
        wd.select_window()
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0019(self):
        """U0019_会员权益
        操作步骤:
        1、点击【会员权益】链接
        ======
        预期结果:
        1、显示当前用户的成长值及对应权益
        2、显示所有会员权益说明以及各个权益对应说明
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser)
        self.comlib.login_portal(username, 't1234567')     
        wd.click_link('会员中心')    
        wd.click_link('会员权益')   
        bln.print_log('检查成长值')    
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name)
        upgrade = wd.get_text('//div[@class="value"]//a')    
        score = score[0][0] if len(score) > 0 else 0
        bln.should_be_equal_as_integers(score, upgrade, '成长值不对') 
        bln.print_log('检查会员权益')    
        one = wd.get_text('//*[@id="my-rights"]/li[@class="enable"][1]/span[@class="tip1"]')    
        two = wd.get_text('//*[@id="my-rights"]/li[@class="enable"][2]/span[@class="tip1"]')    
        three = wd.get_text('//*[@id="my-rights"]/li[@class="last enable"]/span[@class="tip1"]')
        bln.should_be_equal(one, '专享红包') 
        bln.should_be_equal(two, '增利券') 
        bln.should_be_equal(three, '会员生日好礼')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0020(self):
        """U0020_成长任务-页面检查
        操作步骤:
        1、点击“成长任务”
        ======
        预期结果:
        1、链接成长任务界面
        """
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser)
        self.comlib.login_portal(username, 't1234567')    
        wd.click_link('会员中心')    
        wd.click_link('成长任务')   
        wd.title_should_be('会员任务—小牛在线')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0021(self):
        """U0021_成长任务-新手任务-绑定手机
        操作步骤:
        新手任务（绑定手机）
        ======
        预期结果:
        注册成功，成长值为10，“去完成”按钮显示为“已完成”
        """
        global username
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser)        
        self.comlib.login_portal(username, 't1234567')    
        wd.click_link('会员中心')   
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        bln.should_be_equal_as_integers(upgrade, 10, '绑定手机成长值没有增加')
        wd.click_link('成长任务')   
        lis = wd.get_webelements('//li[@class="li-done"]') 
        lis = len(lis) + 1
        count = 0
        for i in range(1, lis):
            ele = wd.get_text('//li[@class="li-done"][{}]/span'.format(i))   
            link = wd.get_text('//li[@class="li-done"][{}]/a'.format(i))   
            if ele == '绑定手机':
                bln.should_be_equal(link, '')
                count += 1
        bln.should_be_equal_as_integers(count, 1, '绑定手机任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0022(self):
        """U0022_成长任务-新手任务-实名绑卡
        操作步骤:
        1、新手任务（实名认证）（如果鉴权实效了重新实名不会获得成长值）
        2、新手任务（绑定银行卡）（如果鉴权实效了重新绑卡不会获得成长值）
        3、新注册用户，绑卡时进行实名操作
        ======
        预期结果:
        1、实名认证成功，成长值增加10，“去完成”按钮显示为“已完成”
        2、绑卡成功，成长值增加10，“去完成”按钮显示为“已完成”
        3、成长值增加20，“去完成”按钮显示为“已完成”
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.binding_card_bank_inter(session)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser)
        self.comlib.login_portal(username, 't1234567')    
        wd.click_link('会员中心')    
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')   
        score = score[0][0] if len(score) > 0 else 0
        score += 20
        bln.should_be_equal_as_integers(upgrade, score, '实名绑卡成长值没有增加')
        wd.click_link('成长任务')    
        lis = wd.get_webelements('//li[@class="li-done"]')
        lis = len(lis)+1
        count = 0
        for i in range(1, lis):
            ele = wd.get_text('//li[@class="li-done"][{}]/span'.format(i))
            link = wd.get_text('//li[@class="li-done"][{}]/a'.format(i))
            if ele == '实名认证':
                bln.should_be_equal(link, '')
                count += 1
            if ele == '绑定银行卡':
                bln.should_be_equal(link, '')
                count += 1
        bln.should_be_equal_as_integers(count, 2, '实名绑卡任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0023(self):
        """U0023_成长任务-新手任务-首次充值大于100
        操作步骤:
        新手任务（首次充值>=100元)
        ======
        预期结果:
        成长值增加20，“去完成”按钮显示为“已完成”
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.recharge_inter(session, 1000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 20
        bln.should_be_equal_as_integers(upgrade, score, '首次充值成长值没有增加')
        wd.click_link('成长任务')    
        lis = wd.get_webelements('//li[@class="li-done"]')    
        lis = len(lis) + 1
        count = 0
        for i in range(1, lis):
            ele = wd.get_text('//li[@class="li-done"][{}]/span'.format(i))
            link = wd.get_text('//li[@class="li-done"][{}]/a'.format(i))
            if ele == '首次充值≥100元':
                bln.should_be_equal(link, '')
                count += 1
        bln.should_be_equal_as_integers(count, 1, '首次充值任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0024(self):
        """U0024_成长任务-进阶任务-首次投资理财金
        操作步骤:
        进阶任务（首次投资理财体验标）
        ======
        预期结果:
        购买成功，成长值增加10
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        try:
            self.comlib.publish_borrow_inter(1000, '体验标')
        except Exception as e:
            pass
        self.comlib.send_financial_inter(username, 1000)
        self.comlib.buy_borrow_inter(session, '体验标', 1000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 10
        bln.should_be_equal_as_integers(upgrade, score, '首次投资理财金体验标成长值没有增加')  
        wd.click_link('成长任务')   
        title = wd.get_webelements('//li[contains(@class,"li-done")]/span')    
        status = wd.get_webelements('//li[contains(@class,"li-done")]/a')
        bln.should_be_equal_as_integers(len(title), len(status), '首次投资理财金体验标任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0025(self):
        """U0025_成长任务-进阶任务-首次投资天天牛
        操作步骤:
        进阶任务（首次投资灵活产品）
        ======
        预期结果:
        购买成功，成长值增加10
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.recharge_inter(session, 1000)
        self.comlib.buy_borrow_inter(session, '天天牛', 1000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 20 # 任意投资增加 投资金额/100 个成长值
        bln.should_be_equal_as_integers(upgrade, score, '首次投资天天牛成长值没有增加')
        wd.click_link('成长任务')    
        title = wd.get_webelements('//li[contains(@class,"li-done")]/span')    
        status = wd.get_webelements('//li[contains(@class,"li-done")]/a')
        bln.should_be_equal_as_integers(len(title), len(status), '首次投资天天牛任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0026(self):
        """U0026_成长任务-进阶任务-首次投资存续牛
        操作步骤:
        进阶任务（首次投资固收理财）
        ======
        预期结果:
        成长值增加15
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.recharge_inter(session, 1000)
        try:
            self.comlib.publish_borrow_inter(1000, '存续牛')
        except Exception as e:
            pass
        self.comlib.buy_borrow_inter(session, '存续牛', 1000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 25
        bln.should_be_equal_as_integers(upgrade, score, '首次投资存续牛成长值没有增加')
        wd.click_link('成长任务')
        title = wd.get_webelements('//li[contains(@class,"li-done")]/span')    
        status = wd.get_webelements('//li[contains(@class,"li-done")]/a')
        bln.should_be_equal_as_integers(len(title), len(status), '首次投资存续牛任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0027(self):
        """U0027_成长任务-进阶任务-首次投资存续牛大于3000
        操作步骤:
        进阶任务（单笔投资固收≥3000元）
        ======
        预期结果:
        成长值增加15
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.recharge_inter(session, 3000)
        try:
            self.comlib.publish_borrow_inter(3000, '存续牛')
        except Exception as e:
            pass
        self.comlib.buy_borrow_inter(session, '存续牛', 3000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 45
        bln.should_be_equal_as_integers(upgrade, score, '首次投资存续牛大于3000成长值没有增加')
        wd.click_link('成长任务')    
        title = wd.get_webelements('//li[contains(@class,"li-done")]/span')    
        status = wd.get_webelements('//li[contains(@class,"li-done")]/a')
        bln.should_be_equal_as_integers(len(title), len(status), '首次投资存续牛大于3000任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0028(self):
        """U0028_成长任务-投资任务-每月首投固收大于5000
        操作步骤:
        1、投资金额=5000
        2、10000>投资金额>5000
        ======
        预期结果:
        
        1、增加成长值60，投资固收理财>=5000按钮改为“已完成”
        2、增加成长值60，投资固收理财>=5000按钮改为“已完成”
        
        （投资任务前面的四个条件和投资任意一笔可获得成长值做比较，取较高的。前面四个条件是每月触发一次，当月完成时显示已完成，下个月又会变成去完成）
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.recharge_inter(session, 5000)
        try:
            self.comlib.publish_borrow_inter(5000, '存续牛')
        except Exception as e:
            pass
        self.comlib.buy_borrow_inter(session, '存续牛', 5000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 60
        bln.should_be_equal_as_integers(upgrade, score, '每月首投固收大于5000成长值没有增加')
        wd.click_link('成长任务')
        title = wd.get_webelements('//li[contains(@class,"li-done")]/span')    
        status = wd.get_webelements('//li[contains(@class,"li-done")]/a')
        bln.should_be_equal_as_integers(len(title), len(status), '每月首投固收大于5000任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0029(self):
        """U0029_成长任务-投资任务-每月首投固收大于10000
        操作步骤:
        1、投资金额=10000
        2、30000>投资金额>10000
        ======
        预期结果:
        1、增加成长值120，投资固收理财>=10000按钮改为“已完成”
        2、增加成长值120，投资固收理财>=10000按钮改为“已完成”
        （投资任务前面的四个条件和投资任意一笔可获得成长值做比较，取较高的。前面四个条件是每月触发一次，当月完成时显示已完成，下个月又会变成去完成）
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.recharge_inter(session, 10000)
        try:
            self.comlib.publish_borrow_inter(10000, '存续牛')
        except Exception as e:
            pass
        self.comlib.buy_borrow_inter(session, '存续牛', 10000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 120
        bln.should_be_equal_as_integers(upgrade, score, '每月首投固收大于10000成长值没有增加')
        wd.click_link('成长任务')
        title = wd.get_webelements('//li[contains(@class,"li-done")]/span')    
        status = wd.get_webelements('//li[contains(@class,"li-done")]/a')
        bln.should_be_equal_as_integers(len(title), len(status), '每月首投固收大于10000任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0030(self):
        """U0030_成长任务-投资任务-每月首投固收大于30000
        操作步骤:
        1、投资金额30000
        2、50000>投资金额>30000
        ======
        预期结果:
        1、增加成长值400，投资固收理财>=30000按钮改为“已完成”
        2、增加成长值400，投资固收理财>=30000按钮改为“已完成”
        （投资任务前面的四个条件和投资任意一笔可获得成长值做比较，取较高的。前面四个条件是每月触发一次，当月完成时显示已完成，下个月又会变成去完成）
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.recharge_inter(session, 30000)
        try:
            self.comlib.publish_borrow_inter(30000, '存续牛')
        except Exception as e:
            pass
        self.comlib.buy_borrow_inter(session, '存续牛', 30000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 400
        bln.should_be_equal_as_integers(upgrade, score, '每月首投固收大于30000成长值没有增加')
        wd.click_link('成长任务')
        title = wd.get_webelements('//li[contains(@class,"li-done")]/span')    
        status = wd.get_webelements('//li[contains(@class,"li-done")]/a')
        bln.should_be_equal_as_integers(len(title), len(status), '每月首投固收大于30000任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0031(self):
        """U0031_成长任务-投资任务-每月首投固收大于50000
        操作步骤:
        1、投资金额=50000
        2、投资金额>50000
        ======
        预期结果:
        1、增加成长值600，投资固收理财>=50000按钮改为“已完成”
        2、增加成长值600，投资固收理财>=50000按钮改为“已完成”
        （投资任务前面的四个条件和投资任意一笔可获得成长值做比较，取较高的。前面四个条件是每月触发一次，当月完成时显示已完成，下个月又会变成去完成）
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.recharge_inter(session, 50000)
        try:
            self.comlib.publish_borrow_inter(100000, '存续牛')
        except Exception as e:
            pass
        self.comlib.buy_borrow_inter(session, '存续牛', 50000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 600
        bln.should_be_equal_as_integers(upgrade, score, '每月首投固收大于50000成长值没有增加')
        wd.click_link('成长任务')
        title = wd.get_webelements('//li[contains(@class,"li-done")]/span')    
        status = wd.get_webelements('//li[contains(@class,"li-done")]/a')
        bln.should_be_equal_as_integers(len(title), len(status), '每月首投固收大于50000任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0032(self):
        """U0032_成长任务-投资任务-任意一笔固收投资
        操作步骤:
        1、投资金额<5000
        ======
        预期结果:
        1、增加成长值 投资金额/100
        （投资任务前面的四个条件和投资任意一笔可获得成长值做比较，取较高的。前面四个条件是每月触发一次，当月完成时显示已完成，下个月又会变成去完成）
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name) 
        session, username = self.comlib.login_portal_inter(username)
        self.comlib.recharge_inter(session, 4000)
        try:
            self.comlib.publish_borrow_inter(4000, '存续牛')
        except Exception as e:
            pass
        self.comlib.buy_borrow_inter(session, '存续牛', 4000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 40
        bln.should_be_equal_as_integers(upgrade, score, '任意一笔固收投资成长值没有增加')
        wd.click_link('成长任务')
        title = wd.get_webelements('//li[@class="li-done" or @class="l-t2 li-done"]/span')
        status = wd.get_webelements('//li[@class="li-done" or @class="l-t2 li-done"]/a') 
        bln.should_be_equal_as_integers(len(title), len(status), '任意一笔固收投资任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0033(self):
        """U0033_成长任务-推荐任务
        操作步骤:
        1、推荐好友
        ======
        预期结果:
        1、成长值增加20，按钮改为“已完成”
        """
        global username
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name)
        mobile = self.comlib.random_mobile()
        session, user = self.comlib.register_user_inter(mobile, refferee=username)
        self.comlib.binding_card_bank_inter(session)
        self.comlib.recharge_inter(session, 50000)
        self.comlib.buy_borrow_inter(session, '存续牛', 1000)
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        upgrade = wd.get_text('//*[@id="streamerModel"]//p[@class="points"]//a[1]')
        score = score[0][0] if len(score) > 0 else 0
        score += 20
        bln.should_be_equal_as_integers(upgrade, score, '推荐任务成长值没有增加')
        wd.click_link('成长任务')
        title = wd.get_webelements('//li[@class="li-done" or @class="l-t2 li-done"]/span')
        status = wd.get_webelements('//li[@class="li-done" or @class="l-t2 li-done"]/a')
        bln.should_be_equal_as_integers(len(title), len(status), '推荐任务完成状态没变')
        wd.close_browser()

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0034(self):
        """U0034_成长任务-成长经历
        操作步骤:
        1、点击时间输入框
        2、开始时间>结束时间，点击“查询”
        3、开始时间<结束时间，点击“查询”
        4、开始时间=结束时间，点击“查询”
        ======
        预期结果:
        1、弹出时间选择框空间，无法输入
        2、列表数据根据所选时间过滤
        3、提示“开始时间不可小于结束时间”
        4、列表数据根据所选时间过滤
        """
        global username
        wd.open_wdBrowser('http://www.xiaoniu88.com/', browser) 
        self.comlib.login_portal(username, 't1234567')
        wd.click_link('会员中心')
        wd.click_link('成长任务')
        wd.click_element('//*[@id="my-task-tab"]/li[2]')  
        wd.click_element('//*[@id="start-time"]')
        wd.click_element('//*[@id="laydate_ok"]')
        wd.click_element('//*[@id="end-time"]')
        wd.click_element('//*[@id="laydate_ok"]')
        wd.click_link('查询')    
        bln.sleep(2)
        wd.page_should_contain('没有数据', '成长经历页面查询功能异常')
        score = self.comlib.mysql_query("SELECT l.`score` FROM xnaccount.`t_member_level` l WHERE l.`userName`='{}';".format(username), 
            host=up_db_host, port=up_db_port, db_name=up_db_name)
        score = score[0][0] if len(score) > 0 else 0
        upgrade = wd.get_text('//span[@class="growth-value"]')
        bln.should_be_equal_as_strings(upgrade, '当前成长值总额：{}点'.format(score), '成长经历页面的成长值显示不对') 
        wd.close_browser()
