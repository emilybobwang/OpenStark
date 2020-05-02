# encoding=utf8


import os
from selenium import webdriver
from SeleniumLibrary.base.robotlibcore import PY2
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords import (AlertKeywords,
                                      BrowserManagementKeywords,
                                      CookieKeywords,
                                      ElementKeywords,
                                      FormElementKeywords,
                                      FrameKeywords,
                                      JavaScriptKeywords,
                                      RunOnFailureKeywords,
                                      ScreenshotKeywords,
                                      SelectElementKeywords,
                                      TableElementKeywords,
                                      WaitingKeywords,
                                      WindowKeywords)
from .builtin import CRFBuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError
from Resource.Variables.common import remote_url


class CRFSelenium(
    AlertKeywords,
    BrowserManagementKeywords,
    CookieKeywords,
    ElementKeywords,
    FormElementKeywords,
    FrameKeywords,
    JavaScriptKeywords,
    RunOnFailureKeywords,
    ScreenshotKeywords,
    SelectElementKeywords,
    TableElementKeywords,
    WaitingKeywords,
    WindowKeywords
):
    def __init__(self):
        ctx = SeleniumLibrary(screenshot_root_directory='Results')
        BrowserManagementKeywords.__init__(self, ctx)
        WindowKeywords.__init__(self, ctx)
        self.screenshot_directory = ctx.screenshot_root_directory
        self.builtIn = CRFBuiltIn()

    @property
    def log_dir(self):
        try:
            if os.path.isdir(self.screenshot_directory):
                return os.path.abspath(self.screenshot_directory)
            else:
                os.makedirs(self.screenshot_directory)
                return os.path.abspath(self.screenshot_directory)
        except RobotNotRunningError:
            return os.getcwd() if PY2 else os.getcwd()

    def open_wdBrowser(self, url, browser='Chrome', alias=None, remote_url=remote_url,
            desired_capabilities=None, ff_profile_dir=None, device=None, maximize_browser=True):
        """
        启动浏览器类型，可选：Firefox、Chrome、Headless, 可模拟移动设备
        """
        if browser.lower() not in ['firefox', 'chrome', 'headless']:
            raise Exception('浏览器类型不对, 仅可选: Firefox, Chrome, Headless')
        chrome_options = webdriver.ChromeOptions()
        if browser.lower() == 'headless':
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options = chrome_options.to_capabilities()
        elif device and browser.lower() == 'chrome':
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            mobile_emulation = {'deviceName': device}
            chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
            chrome_options = chrome_options.to_capabilities()
        elif browser.lower() == 'chrome':
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options = chrome_options.to_capabilities()
        else:
            chrome_options = None
        browser = self.create_webdriver(driver_name='Remote', alias=alias, command_executor=remote_url, desired_capabilities=desired_capabilities or chrome_options)
        self.go_to(url=url)
        maximize_browser and self.maximize_browser_window()
        return browser

    def make_element_visible(self, xpath):
        """Make Element Visible"""
        self.builtIn.print_log('============使节点元素 {} 可见==========='.format(xpath))
        self.wait_until_page_contains_element(xpath)
        self.execute_javascript("document.evaluate('{}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.style.display = 'block';".format(xpath))
        self.wait_until_element_is_visible(xpath)
