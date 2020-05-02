# coding=utf8
import unittest
import random
from Core.keys import webdriver as wd
from Core.keys import builtin as bln
from Core.keys import gen_data as gd
from Core.keys import requests
# from Core.keys import keyboard as kb
from Library.common_library import CommonLibrary
from Resource.Variables.common import *


class LoanGUI(unittest.TestCase):
    """借款人模块自动化用例 GUI版"""
    # 用例执行过滤标签
    tag = 'debug'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.driver = web  # 用于用例执行失败后自动截图, 变量为固定格式, 请勿更改, 不需要失败截图可注释
        wd.set_selenium_speed(0.1)
        wd.set_selenium_implicit_wait(5)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_L0000(self):
        """Debug"""
        wd.open_wdBrowser('http://172.20.20.160:8280/xnzx-test-project/loan/front/openAccount', 'Headless')
        for i in range(3):
            host = '172.20.20.184'
            name = gd.gen_name()
            bank_card = self.comlib.random_bank_card(62258878)
            card_id = gd.gen_idcard()
            mobile = self.comlib.random_mobile()
            types = 1
            month = random.choice([0])
            period = random.choice([100])
            repayType = random.choice([3])
            amount = random.choice([100000])
            accountType = 0

            # wd.go_to('http://172.20.20.160:8280/xnzx-test-project/loan/front/openAccount')
            # wd.input_text('//*[@id="test_ip"]', host)
            # wd.input_text('//*[@id="form1"]/label[6]/input', 'NEO200000')
            # wd.input_text('//*[@id="form1"]/label[7]/input', name)
            # wd.input_text('//*[@id="form1"]/label[8]/input', bank_card)
            # wd.input_text('//*[@id="form1"]/label[9]/input', 'CMB')
            # wd.input_text('//*[@id="form1"]/label[10]/input', types)
            # wd.input_text('//*[@id="form1"]/label[11]/input', card_id)
            # wd.input_text('//*[@id="form1"]/label[12]/input', mobile)
            # wd.click_element('//*[@id="submitBtn1"]')
            # bln.sleep(0.5)
            # wd.click_element('//*[@id="submitBtn2"]')
            # wd.wait_until_page_contains('您当前正在开立', 30)
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
            # try:
            #     wd.page_should_contain('处理成功')
            # except:
            #     continue
            # wd.go_to('http://172.20.20.160:8280/xnzx-test-project/loan/front/withdrawSign')
            # wd.input_text('//*[@id="test_ip"]', host)
            # wd.input_text('//*[@id="form1"]/label[6]/input', 'NEO200000')
            # wd.input_text('//*[@id="form1"]/label[7]/input', name)
            # wd.input_text('//*[@id="form1"]/label[9]/input', card_id)
            # wd.input_text('//*[@id="form1"]/label[8]/input', types)
            # wd.input_text('//*[@id="form1"]/label[11]/input', '2018-12-10 17:25:51')
            # wd.input_text('//*[@id="form1"]/label[12]/input', '500000')
            # wd.click_element('//*[@id="submitBtn1"]')
            # bln.sleep(0.5)
            # wd.click_element('//*[@id="submitBtn2"]')
            # wd.click_element('//*[@id="password"]')
            # kb.key_input('123456')
            # bln.sleep(0.5)
            # wd.click_button('确认')
            # bln.sleep(0.5)
            # wd.click_link('确定')
            # try:
            #     wd.page_should_contain('处理成功')
            # except:
            #     continue
            # wd.go_to('http://172.20.20.160:8280/xnzx-test-project/loan/front/payAndRepaySign')
            # wd.input_text('//*[@id="test_ip"]', host)
            # wd.input_text('//*[@id="form1"]/label[6]/input', 'NEO200000')
            # wd.input_text('//*[@id="form1"]/label[7]/input', name)
            # wd.input_text('//*[@id="form1"]/label[9]/input', card_id)
            # wd.input_text('//*[@id="form1"]/label[8]/input', types)
            # wd.input_text('//*[@id="form1"]/label[10]/input', '2018-01-10 17:25:51')
            # wd.input_text('//*[@id="form1"]/label[11]/input', '2018-12-10 17:25:51')
            # wd.input_text('//*[@id="form1"]/label[12]/input', '2018-01-10 17:25:51')
            # wd.input_text('//*[@id="form1"]/label[13]/input', '2018-12-10 17:25:51')
            # wd.input_text('//*[@id="form1"]/label[14]/input', 100)
            # wd.input_text('//*[@id="form1"]/label[15]/input', 500000)
            # wd.click_element('//*[@id="submitBtn1"]')
            # bln.sleep(0.5)
            # wd.click_element('//*[@id="submitBtn2"]')
            # wd.click_element('//*[@id="password"]')
            # kb.key_input('123456')
            # bln.sleep(0.5)
            # wd.click_button('确认')
            # bln.sleep(0.5)
            # wd.click_link('确定')
            # try:
            #     wd.page_should_contain('处理成功')
            # except:
            #     continue
            wd.go_to('http://172.20.20.160:8280/xnzx-test-project/import/loan/gotomain.action')
            wd.input_text('//*[@id="path"]', 'http://{}:9038/loan/api/import/loan'.format(host))
            wd.input_text('//*[@id="form1"]/label[4]/input', 'NEO200000')
            wd.select_from_list_by_value('//*[@id="form1"]/label[8]/select', 'a')
            wd.select_from_list_by_value('//*[@id="form1"]/label[12]/select', str(month))
            wd.input_text('//*[@id="form1"]/label[13]/input', period)
            wd.select_from_list_by_value('//*[@id="form1"]/label[14]/select', str(repayType))
            wd.input_text('//*[@id="form1"]/label[15]/input', amount)
            wd.input_text('//*[@id="form1"]/label[16]/input', amount)
            wd.select_from_list_by_value('//*[@id="form1"]/label[25]/select', '1')
            wd.select_from_list_by_value('//*[@id="form1"]/label[26]/select', 'a1')
            wd.select_from_list_by_value('//*[@id="form1"]/label[29]/select', str(accountType))
            wd.select_from_list_by_value('//*[@id="form1"]/label[30]/select', str(types))
            wd.input_text('//*[@id="form1"]/label[31]/input', card_id)
            wd.input_text('//*[@id="form1"]/label[32]/input', name)
            wd.input_text('//*[@id="form1"]/label[33]/input', bank_card)
            wd.select_from_list_by_value('//*[@id="form1"]/label[34]/select', 'CMB')
            wd.input_text('//*[@id="form1"]/label[37]/input', '招商银行南山分行')
            wd.input_text('//*[@id="form1"]/label[38]/input', name)
            wd.select_from_list_by_value('//*[@id="form1"]/label[39]/select', str(types))
            wd.input_text('//*[@id="form1"]/label[40]/input', card_id)
            wd.input_text('//*[@id="form1"]/label[41]/input', mobile)
            wd.input_text('//*[@id="form1"]/label[42]/input', bank_card)
            wd.select_from_list_by_value('//*[@id="form1"]/label[43]/select', 'CMB')
            wd.input_text('//*[@id="form1"]/label[46]/input', '招商银行南山分行')
            wd.click_element('//*[@id="submitBtn1"]')
            bln.sleep(0.5)
            wd.click_element('//*[@id="submitBtn2"]')
        wd.close_browser()
