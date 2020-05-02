# coding=utf8
import unittest
from Resource.Variables.common import *
from Library.common_library import CommonLibrary
from Core.keys import builtin as bln
from Core.keys import requests


class UserInterface(unittest.TestCase):
    """用户模块自动化用例 接口版"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
       
    def setUp(self):
        pass

    def tearDown(self):
        requests.delete_all_sessions()

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
        global username
        mobile = self.comlib.random_mobile()
        session, username = self.comlib.register_user_inter(mobile)
        bln.should_start_with(username, 'xn', '手机号码注册失败')

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
        global username
        session, user = self.comlib.login_portal_inter(username)
        bln.should_be_equal(username, user, '以用户名登录失败')

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
        session, username = self.comlib.login_portal_inter(mobile)
        bln.should_start_with(username, 'xn', '手机号码登录失败')

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
        session, username = self.comlib.login_portal_inter(email)
        bln.should_start_with(username, 'xn', '以邮箱登录登录失败')

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
        self.comlib.real_name_inter(session)

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_U0007(self):
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
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        data = dict(bankType='CMB', bankTypeName='招商银行', bankCardNo=card)
        requests.post_request(session, '/payment/bankcard/quickPayBindIndex', data, headers=headers)
        data = dict(regCode='123456')
        resp = requests.post_request(session, '/payment/bankcard/quickPayBindVerify' ,data, headers=headers)
        content = requests.to_json(resp.text) 
        bln.should_be_equal_as_integers(content['status'], 0, '接口快捷绑卡失败')
        
    @unittest.skipUnless(tag == 'run', '已忽略执行')
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
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        data = dict(bankCardNo=card)
        requests.post_request(session, '/payment/bankcard/checkCredit.json', data, headers=headers)
        data = dict(bankType='cmb', bankCardNo=card, isDefault=1, barchaddr='', ad_province='', areaname='', ad_city='', cityname='')
        resp = requests.post_request(session, '/payment/bankcard.json', data, headers=headers)
        content = requests.to_json(resp.text)
        res = self.comlib.mysql_query("SELECT r.`userId`,r.`amount`,r.`status` FROM payment.`t_bind_card_record` r WHERE r.`amount` IS NOT NULL AND r.`userName`='{}' ORDER BY r.`id` DESC LIMIT 1;".format(username))
        userId = res[0][0]
        amount = res[0][1]
        self.comlib.mysql_update("UPDATE payment.`t_bind_card_record` r SET r.`status`=3 WHERE r.`userId`={} AND r.`amount`={};".format(userId, amount))
        amount = str(amount)
        data = dict(amount=amount, txnId=content['key_value'])
        requests.post_request(session, '/payment/bankcard/checkAmount.json', data, headers=headers)
        resp = requests.get_request(session, '/payment/bankcard/finished', headers=headers)
        bln.should_be_equal_as_integers(resp.status_code, 200, '接口打款绑卡失败')

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
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        data = dict(sendType=1, bizCode=1, msgTemp='ssp')
        requests.post_request(session, '/user/sendverifycode', data, headers=headers)
        bln.sleep(1)
        code = self.comlib.get_captcha(mobile)
        data = dict(verifyCode=code, bizCode=1) 
        requests.post_request(session, '/user/authid/vcode', data, headers=headers)
        data = dict(payCode='51942f3c49480e9f09498108c8229eed352a2600496e9554d6366afedaa25b82da7c91c400a922f2f565d607b649d33d164038c658839c0ad81926775d71a1e4f817416a84f18d1f156932d25c6a705c574421f0f0c73eca69c3187fb24e20c6040e2c0c14bd5c1c8a183c6bf46b9ca3d4e14e22e3f76ca4be1e5223af4b2d54')   
        resp = requests.post_request(session, '/user/setpaycode', data, headers=headers)
        content = requests.to_json(resp.text)
        bln.should_be_equal_as_integers(content['status'], 1, '接口设置交易密码失败')

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
        session, username = self.comlib.login_portal_inter(mobile)
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        data = dict(sendType=1, curDealPassword='6b40de08d49d986009244ed37f82d30b2c43d3c29018235c5e0a70388541572001efff4399f0ccc4c70d8c11ea4cf57a358c23089642bb635ef6eec297dba6893a0f73a507fa9f39b045e4903f74c18c4c5ca43e92bf102f5ec2ca8f11a1752518988ae427854e053a468f784576270187538d4a8f8107d479d4370e30a29b29')  
        requests.post_request(session, '/user/modifypaycode/sendverify', data, headers=headers)
        bln.sleep(1)
        code = self.comlib.get_captcha(mobile)
        data = dict(verifyCode=code, curPayCode='24ac7f5b29b010009c9e99116f9cebf0302f5f395130b660a22a5dcd185fab1b1d6ebee57c6a381eb3a83e0827dae94fded619c792677f94f656525f0bda7c0624c588572bca5d257b239844bef4384338939558e9c1fa8bc33c7d2d2d14e2bcc574f658fc096f925a496936fc5f70fe12fab7aa939894cafec2f57ce6770976', newPayCode='0487ef22f9244912e5b4fc7cf227626e1f18953b2e989725d9bfc68f70f0434fb48527a58af85557fd2432385bc9d0077c974b7368af45fd8866f4cbc5239f75898185da849cd002afad2ce3bd3b75ace84b74fd537bb2fa3b11393d77cb62e2d833b54991077e00f29bab7341b4262cb847505b9cea595fc9fed922e6a45dcf')   
        resp = requests.post_request(session, '/user/modifypaycode', data, headers=headers)
        content = requests.to_json(resp.text) 
        bln.should_be_equal_as_integers(content['status'], 1, '接口修改交易密码失败')    

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
        session, username = self.comlib.login_portal_inter(mobile)
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        data = dict(sendType=1, bizCode=1, msgTemp='sfp') 
        requests.post_request(session, '/user/sendverifycode', data, headers=headers)
        bln.sleep(1)
        code = self.comlib.get_captcha(mobile)
        data = dict(verifyCode=code, bizCode=1)    
        requests.post_request(session, '/user/authid/vcode', data, headers=headers)
        data = dict(payCode='67b6e012beb4857d8dff0ac2b2b6de9c6d3377ec64ae39aad92220ab778b9bae45f83226d0e38977a46a01f6de729a2cddd2cfc2aaba914f0b55cb6aa11ef84f0a87578aca4b38258eda74ad558d45d3fda4c8bc03024d9367b18cda9ed40062b5ca74fee540c0d3eabafacf93afdcd2d947d6d590e87b6a847387e974f1ddfc')    
        resp = requests.post_request(session, '/user/setpaycode', data, headers=headers) 
        content = requests.to_json(resp.text) 
        bln.should_be_equal_as_integers(content['status'], 1, '接口找回交易密码失败') 

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
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        data = dict(loginPwd='30e27fa0a8302dd3576c0287b708b1aea303a4e881b552a1668e98c2fd7067e07d1f9ba7cabb7f245244989d6893f8d92d6ec72763a0f1ee6c2450f92c548d3b17acb604d79614f8133b6f939a9c61108e48f6d8af4f0c232102f4778b414a43c4e11a1ea4685501f5198676ff6f4a54f1c70f892226943abbabc6b0c1798046')    
        requests.post_request(session, '/user/authid/lpwd', data, headers=headers) 
        data = dict(sendType=1, bizCode=4, msgTemp='smlp')     
        requests.post_request(session, '/user/sendverifycode', data, headers=headers) 
        bln.sleep(1)
        code = self.comlib.get_captcha(mobile)
        data = dict(curUserPwd='c55302be91bda5671d318f5c179818793c01da72fa217d205c8b2a1ef095422477aae1d7de44b9cb88eb3a630967bdcff924e02109ce5c2db02def97722f002b4281d5b987ba0943aa90a8ee0ca2df778f8cb6eb3eb9ef04428c47c1f09686d331778814229060bb052af4dba8d5cb75f06301c06f7346a2f362e5d3f19b4859', newUserPwd='0aa9847a9fd17d24bac5dde71cbba89dfdc40f2bea6ef6d1164a2447236a352caa9dd44737f8b1dda6890e4d2190770396009b3d38ba21596453e025325057c1f55d44956246f2198fdf2f7e80379abda3a74d8f76268d1ad0f5ede17b8d6cc0634d5f08230341171b81ed66c44b06592dbf333d2cfe7f367e8e1bcce15e6378', verifyCode=code)  
        resp = requests.post_request(session, '/user/modifyuserpwd', data, headers=headers) 
        content = requests.to_json(resp.text) 
        bln.should_be_equal_as_integers(content['status'], 1, '接口修改登录密码失败')

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
        session, username = self.comlib.login_portal_inter(mobile)
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        data = dict(sendType=2, bizCode=3, msgTemp='eme')
        requests.post_request(session, '/user/sendverifycode', data, headers=headers)
        bln.sleep(1)
        code = self.comlib.get_captcha(email, 'email')
        data = dict(bizCode=3, verifyCode=code)
        requests.post_request(session, '/user/authid/vcode', data, headers=headers)
        email = self.comlib.random_email()
        data = dict(email=email)
        resp = requests.post_request(session, '/user/isemailexist', data, headers=headers)
        data = dict(email=email, sendType=2, bizCode=3, msgTemp='eme') 
        resp = requests.post_request(session, '/user/sendverifycode_nm', data, headers=headers)
        bln.sleep(1)
        code = self.comlib.get_captcha(email, 'email')
        data = dict(email=email, verifyCode=code)
        resp = requests.post_request(session, '/user/modifyemail/vcode', data, headers=headers)
        content = requests.to_json(resp.text)
        bln.should_be_equal_as_integers(content['status'], 1, '接口修改邮箱失败')

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
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        data = dict(relation=1, name='李思', mobile='13048884557')     
        resp = requests.post_request(session, '/user/setemergency', data, headers=headers)
        content = requests.to_json(resp.text)  
        bln.should_be_equal_as_integers(content['status'], 1, '接口设置紧急联系人失败')

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
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        data = dict(relation=1,name='李思', mobile='13048884559')
        resp = requests.post_request(session, '/user/setemergency', data, headers=headers)
        content = requests.to_json(resp.text)
        bln.should_be_equal_as_integers(content['status'], 1, '接口修改紧急联系人失败')
