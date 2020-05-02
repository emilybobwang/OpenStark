# coding=utf8
import unittest
from Core.keys import webdriver as wd
from Core.keys import builtin as bln
from Library.common_library import CommonLibrary
from Resource.Variables.common import *


class FinancierGUI(unittest.TestCase):
    """理财师模块自动化用例 GUI版"""
    # 导入自定义库
    comlib = CommonLibrary()
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        cls.driver = wd
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_F0001(self):
        pass
