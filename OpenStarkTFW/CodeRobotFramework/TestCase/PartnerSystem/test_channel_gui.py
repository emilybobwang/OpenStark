# coding=utf8
import unittest
import os
from Core.keys import webdriver as wd
from Library.common_library import CommonLibrary
from Core.test_data_generator import TestDataGenerator
from parameterized import parameterized, param


local_path = os.path.dirname(__file__)
# 导入自定义库
gen_td = TestDataGenerator()
comlib = CommonLibrary()


class ChannelGUI(unittest.TestCase):
    """渠道营销自动化用例 GUI版"""
    # 用例执行过滤标签
    tag = 'debug'

    @classmethod
    def setUpClass(cls):
        cls.driver = web  # 用于用例执行失败后自动截图, 变量为固定格式, 请勿更改, 不需要失败截图可注释
        wd.set_selenium_speed(0.1)
        wd.set_selenium_implicit_wait(5)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # wd.open_wdBrowser('http://www.xiaoniu88.com')
        pass

    def tearDown(self):
        # wd.close_browser()
        pass

    @parameterized.expand([
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_yingxiao2', comlib.random_mobile('161')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_yingxiao', comlib.random_mobile('161')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_201701fanxianquan', comlib.random_mobile('161')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_518activity', comlib.random_mobile('161')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_Billsimpleadvert', comlib.random_mobile('161')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_iccadvert', comlib.random_mobile('161')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_Billsimpleskill', comlib.random_mobile('161')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_iccskill', comlib.random_mobile('161')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_huijia288', comlib.random_mobile('161')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_201701fanxianquan', comlib.random_mobile('161')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_518activity', comlib.random_mobile('161')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_Billsimpleadvert', comlib.random_mobile('161')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_Billsimpleskill', comlib.random_mobile('161')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_iccadvert', comlib.random_mobile('161')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_iccskill', comlib.random_mobile('161')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_huijia288', comlib.random_mobile('161')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_yingxiao2', comlib.random_mobile('161')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_yingxiao', comlib.random_mobile('161')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_yingxiao2', comlib.random_mobile('191')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_yingxiao', comlib.random_mobile('191')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_201701fanxianquan', comlib.random_mobile('191')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_518activity', comlib.random_mobile('191')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_Billsimpleadvert', comlib.random_mobile('191')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_iccadvert', comlib.random_mobile('191')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_Billsimpleskill', comlib.random_mobile('191')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_iccskill', comlib.random_mobile('191')),
        (1, 'PC', 'https://www.xiaoniu88.com/partner/landing/p_huijia288', comlib.random_mobile('191')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_201701fanxianquan', comlib.random_mobile('191')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_518activity', comlib.random_mobile('191')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_Billsimpleadvert', comlib.random_mobile('191')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_Billsimpleskill', comlib.random_mobile('191')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_iccadvert', comlib.random_mobile('191')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_iccskill', comlib.random_mobile('191')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_huijia288', comlib.random_mobile('191')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_yingxiao2', comlib.random_mobile('191')),
        (1, 'WAP', 'https://www.xiaoniu88.com/partner/landing/w_yingxiao', comlib.random_mobile('191'))
    ])
    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_C0001(self, _, platform, url, mobile):
        """C0001_渠道着陆页手机号码格式验证
        """
        comlib.channel_register(url, platform, mobile=mobile)

    @parameterized.expand(
        param.explicit(kwargs=gen_td.load_test_data(line, dict(mobile=comlib.random_mobile(['191', '161']))))
        for line in open('{}/channel_gui/test_C0002.json'.format(local_path))
    )
    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_C0002(self, _, platform, url, mobile):
        """C0002_渠道着陆页模板手机号码格式验证
        """
        comlib.channel_template_register(url, platform, mobile=mobile)

    @unittest.skipUnless(tag == 'debug', '已忽略执行')
    def test_C0003(self):
        """C0003_渠道着陆页模板手机号码格式验证
        """
        wd.open_wdBrowser('https://www.xiaoniu88.com/product/financial', browser='Headless')
        wd.capture_page_screenshot('C:\\Users\\xn031951\\Downloads\\test.png')
        wd.close_browser()
