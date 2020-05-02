#!/usr/bin/env python3
# coding: utf-8
import os
from unittest import TestSuite, TestLoader
from Core.Runner.test_runner import TestRunner
from Core.Runner.xmlrunner import XMLTestRunner
from Core.Runner.HtmlTestRunner import HTMLTestRunner
# 导入测试用例
# from TestCase.UserSystem.test_user_interface import UserInterface
from TestCase.UserSystem.test_user_gui import UserGUI
# from TestCase.FinancierSystem.test_financier_gui import FinancierGUI
# from TestCase.FinancierSystem.test_financier_interface import FinancierInterface
# from TestCase.PartnerSystem.test_channel_gui import ChannelGUI
# from TestCase.PartnerSystem.test_marketing_report import ChannelReport
# from TestCase.PartnerSystem.test_marketing_report import ChannelRechargeReport
# from TestCase.PartnerSystem.test_marketing_report import ChannelInvestReport
# from TestCase.PartnerSystem.test_marketing_report import ChannelFirstInvestReport
# from TestCase.PartnerSystem.test_marketing_report import ChannelRegisterInvestReport
# from TestCase.PartnerSystem.test_marketing_report import ChannelSourceDataDiff  # 比较耗内存
# from TestCase.PartnerSystem.test_marketing_report import ChannelStrategyReport
# from TestCase.PartnerSystem.test_marketing_report import ChannelRegisterTotleReport
# from TestCase.PartnerSystem.test_marketing_report import ChannelRegisterReport
# from TestCase.LoanSystem.test_loan_gui import LoanGUI


# 加载所有测试用例
def test_suites():
    test_loader = TestLoader()
    test_suite = TestSuite()
    be_run_tests = test_loader.loadTestsFromTestCase(UserGUI)
    if os.path.isfile('be_run_cases.txt'):
        with open('be_run_cases.txt', 'r', encoding='utf8') as fp:
            be_run_tests_list = list()
            for test in fp.readlines():
                if test.strip():
                    be_run_tests_list.append(test.strip())
            if be_run_tests_list:
                be_run_tests = test_loader.loadTestsFromNames(be_run_tests_list)
    test_suite.addTests([
        be_run_tests,
        ])
    return test_suite


# 执行测试
def main():
    # rerun  失败重试次数
    # tb_locals  日志中是否打印变量值
    runner = TestRunner(output='Results', verbosity=2, tb_locals=True, rerun=0, report_title='自动化测试报告')
    runner.run(test_suites())


if __name__ == '__main__':
    main()
