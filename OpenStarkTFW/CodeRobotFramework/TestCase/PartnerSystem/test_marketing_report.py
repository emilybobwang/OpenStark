# coding=utf8
import unittest
from Resource.Variables.common import *
from Library.common_library import CommonLibrary
from Core.keys import builtin as bln
from Core.keys import requests
from Library.data_diff_library import DataDiffLibrary
from datetime import datetime, timedelta
import time


class ChannelRegisterReport(unittest.TestCase):
    """营销报表渠道用户注册效果数据核算"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.diff = DataDiffLibrary()
        cls.cookie = cls.diff.login_interface(be_login_url, be_login_user_passwd)
       
    def setUp(self):
        self.start_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.ymd = time.strftime('%Y-%m-%d')
        self.ymdhms = time.strftime('%Y%m%d%H%M%S')

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MR0001(self):
        """MR0001_用户注册效果_按注册日期查询
        操作步骤:
        用户注册效果_按注册日期查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginTime=self.start_date, endTime=self.end_date, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', username='', mobile='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/cpa/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册效果报表.sql', sql_earch) 
        self.diff.diff_data(left, right, ['dcCreator'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MR0002(self):
        """MR0002_用户注册效果_按渠道名称查询
        操作步骤:
        用户注册效果_按渠道名称查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginTime=self.start_date, endTime=self.end_date, channelname='迅雷', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='迅雷', username='', mobile='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/cpa/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册效果报表.sql', sql_earch) 
        self.diff.diff_data(left, right, ['dcCreator'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MR0003(self):
        """MR0003_用户注册效果_按用户名称查询
        操作步骤:
        用户注册效果_按用户名称查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginTime=self.start_date, endTime=self.end_date, username='xl', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', username='xl', mobile='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/cpa/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册效果报表.sql', sql_earch) 
        self.diff.diff_data(left, right, ['dcCreator'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MR0004(self):
        """MR0004_用户注册效果_按手机号码查询
        操作步骤:
        用户注册效果_按手机号码查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginTime=self.start_date, endTime=self.end_date, mobile='13', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', username='', mobile='13', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/cpa/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册效果报表.sql', sql_earch) 
        self.diff.diff_data(left, right, ['dcCreator'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MR0005(self):
        """MR0005_用户注册效果_综合查询
        操作步骤:
        用户注册效果_综合查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginTime=self.start_date, endTime=self.end_date, channelname='迅雷', username='xl', mobile='13', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='迅雷', username='xl', mobile='13', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/cpa/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册效果报表.sql', sql_earch) 
        self.diff.diff_data(left, right, ['dcCreator'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MR0006(self):
        """MR0006_用户注册效果_扣量恢复
        操作步骤:
        用户注册效果_扣量恢复
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginTime=self.start_date, endTime=self.end_date, channelname='', username='', mobile='', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', username='', mobile='', rows=50000) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册效果报表.sql', sql_earch, file=False) 
        sid = int(right[0]['id'])
        userId = int(right[0]['userId'])
        channelId = int(right[0]['channelId'])
        bindingType = int(right[0]['bindingType'])
        update_be = dict(deductState=0, id=sid, userId=userId, channelId=channelId, bindingType=bindingType)
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/uniqueUpdate'.format(be_url), method='POST', body=update_be, cookie=self.cookie, file=False) 
        bln.should_be_equal_as_strings(left, 'success')
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/cpa/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册效果报表.sql', sql_earch) 
        self.diff.diff_data(left, right, ['dcCreator'])    


class ChannelRegisterTotleReport(unittest.TestCase):
    """营销报表渠道注册总量数据核算"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.diff = DataDiffLibrary()
        cls.cookie = cls.diff.login_interface(be_login_url, be_login_user_passwd)
       
    def setUp(self):
        self.start_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.ymd = time.strftime('%Y-%m-%d')
        self.ymdhms = time.strftime('%Y%m%d%H%M%S')

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRT0001(self):
        """MCRT0001_渠道注册总量_按注册日期查询
        操作步骤:
        渠道注册总量_按注册日期查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelindex='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/totle/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册总量报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRT0002(self):
        """MCRT0002_渠道注册总量_按渠道名称查询
        操作步骤:
        渠道注册总量_按渠道名称查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelname='迅雷', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='迅雷', channelindex='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/totle/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册总量报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRT0003(self):
        """MCRT0003_渠道注册总量_按渠道索引查询
        操作步骤:
        渠道注册总量_按渠道索引查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelindex='e0705ba7008004c7', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelindex='e0705ba7008004c7', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/totle/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册总量报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRT0004(self):
        """MCRT0004_渠道注册总量_综合查询
        操作步骤:
        渠道注册总量_综合查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelname='迅雷', channelindex='e07', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='迅雷', channelindex='e07', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/totle/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册总量报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    


class ChannelStrategyReport(unittest.TestCase):
    """营销报表渠道效果策略管理数据核算"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.diff = DataDiffLibrary()
        cls.cookie = cls.diff.login_interface(be_login_url, be_login_user_passwd)
       
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MS0001(self):
        """MS0001_渠道效果策略管理_按渠道索引查询
        操作步骤:
        渠道效果策略管理_按渠道索引查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelindex='700800', page=1, rows=50000)
        sql_earch = dict(channelindex='700800', channelname='', channelGroup='', channelPlatform='', realname='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['cid'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MS0002(self):
        """MS0002_渠道效果策略管理_按渠道名称查询
        操作步骤:
        渠道效果策略管理_按渠道名称查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelname='迅雷', page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='迅雷', channelGroup='', channelPlatform='', realname='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['cid'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MS0003(self):
        """MS0003_渠道效果策略管理_按渠道所属平台查询
        操作步骤:
        渠道效果策略管理_按渠道所属平台查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelPlatform='迅雷', page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='', channelGroup='', channelPlatform='迅雷', realname='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['cid'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MS0004(self):
        """MS0004_渠道效果策略管理_按渠道所属功能组查询
        操作步骤:
        渠道效果策略管理_按渠道所属功能组查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelGroup='2', page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='', channelGroup='2', channelPlatform='', realname='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['cid'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MS0005(self):
        """MS0005_渠道效果策略管理_按负责人查询
        操作步骤:
        渠道效果策略管理_按负责人查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(realname='陈意', page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='', channelGroup='', channelPlatform='', realname='陈意', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['cid'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MS0006(self):
        """MS0006_渠道效果策略管理_综合查询
        操作步骤:
        渠道效果策略管理_综合查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelindex='f', channelname='电', channelGroup='2', channelPlatform='其他', realname='陈意', page=1, rows=50000)
        sql_earch = dict(channelindex='f', channelname='电', channelGroup='2', channelPlatform='其他', realname='陈意', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['cid'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MS0007(self):
        """MS0007_渠道效果策略管理_执行扣量
        操作步骤:
        渠道效果策略管理_执行扣量
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelindex='b9c90ffb908fcb3c', page=1, rows=50000)
        sql_earch = dict(channelindex='b9c90ffb908fcb3c', channelname='', channelGroup='', channelPlatform='', realname='', rows=50000) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd,
            "SELECT * FROM partner.`t_channel_deduct_context` c WHERE c.`channelId`='10466';", sql_earch, file=False) 
        sid = int(right[0]['id'])
        strategyId = int(right[0]['strategyId'])
        update_be = dict(contextId=sid, channelId='10466', deductConfig='(0,100]{1/10}|(100,1000]{1/100}', state=0, strategyId=strategyId,
            cpaDeductConfig='', deductModel=1, channelName='融360wap', rangesList='', crmReportDelayFlag=0, crmReportDelay=0, deductType=1)
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/insert'.format(be_url), method='POST', body=update_be, cookie=self.cookie, key='', content_type='FORM', file=False) 
        res = left['data']
        bln.should_be_true(res)
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows', file=False) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch, file=False) 
        self.diff.diff_data(left, right, ['cid'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MS0008(self):
        """MS0008_渠道效果策略管理_停止扣量
        操作步骤:
        渠道效果策略管理_停止扣量
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelindex='b9c90ffb908fcb3c', page=1, rows=50000)
        sql_earch = dict(channelindex='b9c90ffb908fcb3c', channelname='', channelGroup='', channelPlatform='', realname='', rows=50000) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd,
           "SELECT * FROM partner.`t_channel_deduct_context` c WHERE c.`channelId`='10466';", sql_earch, file=False) 
        sid = int(right[0]['id'])
        strategyId = int(right[0]['strategyId'])
        update_be = dict(contextId=sid, channelId='10466', deductConfig='(0,100]{1/10}|(100,1000]{1/100}', state=1, strategyId=strategyId,
            cpaDeductConfig='', deductModel=1, channelName='融360wap', rangesList='', crmReportDelay=0)
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/update'.format(be_url), method='POST', body=update_be, cookie=self.cookie, key='', content_type='FORM', file=False) 
        res = left['data']
        bln.should_be_true(res)
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows', file=False) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch, file=False) 
        self.diff.diff_data(left, right, ['cid'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MS0009(self):
        """MS0009_渠道效果策略管理_批量恢复扣量
        操作步骤:
        渠道效果策略管理_批量恢复扣量
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelindex='b9c90ffb908fcb3c', page=1, rows=50000)
        sql_earch = dict(channelindex='b9c90ffb908fcb3c', channelname='', channelGroup='', channelPlatform='', realname='', rows=50000) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch, file=False) 
        channelId = int(right[0]['channelId'])
        update_be = dict(channelId=channelId, limit=1, deductModel=1)
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/batchUpdate'.format(be_url), method='POST', body=update_be, cookie=self.cookie, key='', content_type='FORM', file=False) 
        bln.should_be_equal_as_strings(left, 'success')
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/deduct/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows', file=False) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道效果策略管理.sql', sql_earch, file=False) 
        self.diff.diff_data(left, right, []) 


class ChannelSourceDataDiff(unittest.TestCase):
    """营销报表数据源数据核算"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.diff = DataDiffLibrary()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCSD0001(self):
        """MCSD0001_数据源_t_channel_user_recharge_account表校验
        操作步骤:
        数据源_t_channel_user_recharge_account表校验
        ======
        预期结果:         
        查询成功, 数据正确
        """
        left, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'SELECT * FROM partner.`t_channel_user_recharge_account` r ORDER BY r.`userId` DESC LIMIT 300000;') 
        left, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'SELECT * FROM partner.`t_channel_user_recharge_account` r ORDER BY r.`userId` DESC LIMIT 300000, 300000;', add_data=left) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/t_channel_user_recharge_account数据核对.sql', {"offset":0, "limit":300000}) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/t_channel_user_recharge_account数据核对.sql', {"offset":300000, "limit":300000}, add_data=right) 
        self.diff.diff_data(left, right, ["id", "createTime", "modifyTime"]) 

    @unittest.skip('跨库无法执行')
    def test_MCSD0002(self):
        """MCSD0002_数据源_t_channel_account表校验
        操作步骤:
        数据源_t_channel_account表校验
        ======
        预期结果:         
        查询成功, 数据正确
        """
        left, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'SELECT * FROM partner.`t_channel_account` a ORDER BY a.`channelId` DESC, a.`accountingTime` DESC LIMIT 300000;') 
        left, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'SELECT * FROM partner.`t_channel_account` a ORDER BY a.`channelId` DESC, a.`accountingTime` DESC LIMIT 300000, 300000;', add_data=left) 
        right, count = self.diff.get_database_data(up_db_host, up_db_port, up_db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/t_channel_account数据核对.sql', {"offset":0, "limit":300000}) 
        right, count = self.diff.get_database_data(up_db_host, up_db_port, up_db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/t_channel_account数据核对.sql', {"offset":300000, "limit":300000}, add_data=right) 
        self.diff.diff_data(left, right, ["id", "createTime", "modifyTime"])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCSD0003(self):
        """MCSD0003_数据源_t_channel_user_account_relationship表校验
        操作步骤:
        数据源_t_channel_user_account_relationship表校验
        ======
        预期结果:         
        查询成功, 数据正确
        """
        res = self.comlib.mysql_query('SELECT DISTINCT i.`investor` FROM product.`t_invest` i WHERE i.`result`=1 UNION SELECT DISTINCT i.userId as investor from pcts.t_invest i;', up_db_host, up_db_port, db_user, db_passwd, up_db_name)
        users = ''
        for user in res:
            users += ',{}'.format(user[0])
        left, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'SELECT * FROM partner.`t_channel_user_recharge_account` r ORDER BY r.`userId` DESC LIMIT 300000;') 
        left, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'SELECT * FROM partner.`t_channel_user_recharge_account` r ORDER BY r.`userId` DESC LIMIT 300000, 300000;', add_data=left) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/t_channel_user_recharge_account数据核对.sql', {"users": users[1:], "offset":0, "limit":300000}) 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/t_channel_user_recharge_account数据核对.sql', {"users": users[1:], "offset":300000, "limit":300000}, add_data=right) 
        self.diff.diff_data(left, right, ["id", "createTime", "modifyTime"])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCSD0004(self):
        """MCSD0004_数据源_t_channel_user_invest_account表校验
        操作步骤:
        数据源_t_channel_user_invest_account表校验
        ======
        预期结果:         
        查询成功, 数据正确
        """
        res = self.comlib.mysql_query('SELECT DISTINCT tcu.`userId` AS userId FROM partner.`t_channel_user` AS tcu WHERE tcu.`bindingType` IN (1,2,4,5)')
        users = ''
        for user in res:
            users += ',{}'.format(user[0])
        left, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'SELECT * FROM partner.`t_channel_user_invest_account` i ORDER BY i.`userId` DESC LIMIT 300000;') 
        left, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'SELECT * FROM partner.`t_channel_user_invest_account` i ORDER BY i.`userId` DESC LIMIT 300000, 300000;', add_data=left) 
        right, count = self.diff.get_database_data(up_db_host, up_db_port, up_db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/t_channel_user_invest_account数据核对.sql', {"users": users[1:], "offset":0, "limit":300000}) 
        right, count = self.diff.get_database_data(up_db_host, up_db_port, up_db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/t_channel_user_invest_account数据核对.sql', {"users": users[1:], "offset":300000, "limit":300000}, add_data=right) 
        self.diff.diff_data(left, right, ["id", "createTime", "modifyTime"])    


class ChannelRegisterInvestReport(unittest.TestCase):
    """营销报表渠道用户注册投资数据核算"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.diff = DataDiffLibrary()
        cls.cookie = cls.diff.login_interface(be_login_url, be_login_user_passwd)
       
    def setUp(self):
        self.start_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.ymd = time.strftime('%Y-%m-%d')
        self.ymdhms = time.strftime('%Y%m%d%H%M%S')

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRI0001(self):
        """MCRI0001_渠道用户注册投资_按注册日期查询
        操作步骤:
        渠道用户注册投资_按注册日期查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', keyWord='', username='', channelPlatform='', deductState='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/keyWord/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册投资报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRI0002(self):
        """MCRI0002_渠道用户注册投资_按渠道名称查询
        操作步骤:
        渠道用户注册投资_按渠道名称查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelname='迅雷', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='迅雷', keyWord='', username='', channelPlatform='', deductState='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/keyWord/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册投资报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRI0003(self):
        """MCRI0003_渠道用户注册投资_按关键词查询
        操作步骤:
        渠道用户注册投资_按关键词查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, keyWord='xunlei', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', keyWord='xunlei', username='', channelPlatform='', deductState='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/keyWord/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册投资报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRI0004(self):
        """MCRI0004_渠道用户注册投资_按用户名查询
        操作步骤:
        渠道用户注册投资_按用户名查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, userName='rong0616', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', keyWord='', username='rong0616', channelPlatform='', deductState='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/keyWord/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册投资报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRI0005(self):
        """MCRI0005_渠道用户注册投资_按渠道所属平台查询
        操作步骤:
        渠道用户注册投资_按渠道所属平台查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelPlatform='迅雷', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', keyWord='', username='', channelPlatform='迅雷', deductState='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/keyWord/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册投资报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRI0006(self):
        """MCRI0006_渠道用户注册投资_按数据类型查询
        操作步骤:
        渠道用户注册投资_按数据类型查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, deductState=0, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', keyWord='', username='', channelPlatform='', deductState=0, channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/keyWord/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册投资报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRI0007(self):
        """MCRI0007_渠道用户注册投资_按渠道种类-理财师渠道查询
        操作步骤:
        渠道用户注册投资_按渠道种类-理财师渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelMode=1, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', keyWord='', username='', channelPlatform='', deductState='', channelMode=1, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/keyWord/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册投资报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRI0008(self):
        """MCRI0008_渠道用户注册投资_按渠道种类-虚拟渠道查询
        操作步骤:
        渠道用户注册投资_按渠道种类-虚拟渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelMode=2, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', keyWord='', username='', channelPlatform='', deductState='', channelMode=2, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/keyWord/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册投资报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCRI0009(self):
        """MCRI0009_渠道用户注册投资_综合查询
        操作步骤:
        渠道用户注册投资_综合查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelname='迅雷', channelPlatform='迅雷', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='迅雷', keyWord='', username='', channelPlatform='迅雷', deductState='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/keyWord/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户注册投资报表.sql', sql_earch) 
        self.diff.diff_data(left, right, [])    


class ChannelFirstInvestReport(unittest.TestCase):
    """营销报表渠道用户初次投资数据核算"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.diff = DataDiffLibrary()
        cls.cookie = cls.diff.login_interface(be_login_url, be_login_user_passwd)
       
    def setUp(self):
        self.start_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.ymd = time.strftime('%Y-%m-%d')
        self.ymdhms = time.strftime('%Y%m%d%H%M%S')

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCFI0001(self):
        """MCFI0001_渠道用户初次投资_按初投日查询
        操作步骤:
        渠道用户初次投资_按初投日查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(firstInvestDateStart=self.start_date, firstInvestDateEnd=self.end_date, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelUserName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/invest/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCFI0002(self):
        """MCFI0002_渠道用户初次投资_按渠道名称查询
        操作步骤:
        渠道用户初次投资_按渠道名称查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(firstInvestDateStart=self.start_date, firstInvestDateEnd=self.end_date, channelname='迅雷', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='迅雷', channelUserName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/invest/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCFI0003(self):
        """MCFI0003_渠道用户初次投资_按渠道所属平台查询
        操作步骤:
        渠道用户初次投资_按渠道所属平台查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(firstInvestDateStart=self.start_date, firstInvestDateEnd=self.end_date, channelPlatform='其他', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelUserName='', channelPlatform='其他', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/invest/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCFI0004(self):
        """MCFI0004_渠道用户初次投资_按渠道种类-理财师渠道查询
        操作步骤:
        渠道用户初次投资_按渠道种类-理财师渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(firstInvestDateStart=self.start_date, firstInvestDateEnd=self.end_date, channelMode=1, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelUserName='', channelPlatform='', channelMode=1, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/invest/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCFI0005(self):
        """MCFI0005_渠道用户初次投资_按渠道种类-虚拟渠道查询
        操作步骤:
        渠道用户初次投资_按渠道种类-虚拟渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(firstInvestDateStart=self.start_date, firstInvestDateEnd=self.end_date, channelMode=2, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelUserName='', channelPlatform='', channelMode=2, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/invest/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCFI0006(self):
        """MCFI0006_渠道用户初次投资_按负责人查询
        操作步骤:
        渠道用户初次投资_按负责人查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(firstInvestDateStart=self.start_date, firstInvestDateEnd=self.end_date, channelUserName='', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelUserName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/invest/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCFI0007(self):
        """MCFI0007_渠道用户初次投资_综合查询
        操作步骤:
        渠道用户初次投资_综合查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(firstInvestDateStart=self.start_date, firstInvestDateEnd=self.end_date, channelname='迅雷', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='迅雷', channelUserName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/invest/report/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道用户初次投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    


class ChannelInvestReport(unittest.TestCase):
    """营销报表渠道注册投资数据核算"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.diff = DataDiffLibrary()
        cls.cookie = cls.diff.login_interface(be_login_url, be_login_user_passwd)
       
    def setUp(self):
        self.start_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.ymd = time.strftime('%Y-%m-%d')
        self.ymdhms = time.strftime('%Y%m%d%H%M%S')

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0001(self):
        """MCI0001_渠道注册投资_按注册时间查询
        操作步骤:
        渠道注册投资_按注册时间查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=0, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=0, channelname='', channelUseName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0002(self):
        """MCI0002_渠道注册投资_按7日注册投资查询
        操作步骤:
        渠道注册投资_按7日注册投资查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=6, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=6, channelname='', channelUseName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0003(self):
        """MCI0003_渠道注册投资_按30日注册投资查询
        操作步骤:
        渠道注册投资_按30日注册投资查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=29, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=29, channelname='', channelUseName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0004(self):
        """MCI0004_渠道注册投资_按45日注册投资查询
        操作步骤:
        渠道注册投资_按45日注册投资查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=44, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=44, channelname='', channelUseName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0005(self):
        """MCI0005_渠道注册投资_按90日注册投资查询
        操作步骤:
        渠道注册投资_按90日注册投资查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=89, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=89, channelname='', channelUseName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0006(self):
        """MCI0006_渠道注册投资_按渠道名称查询
        操作步骤:
        渠道注册投资_按渠道名称查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=0, channelname='迅雷', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=0, channelname='迅雷', channelUseName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0007(self):
        """MCI0007_渠道注册投资_按渠道所属平台查询
        操作步骤:
        渠道注册投资_按渠道所属平台查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=0, channelMode=0, channelPlatform='其他', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=0, channelname='', channelUseName='', channelPlatform='其他', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0008(self):
        """MCI0008_渠道注册投资_按渠道种类-理财师渠道查询
        操作步骤:
        渠道注册投资_按渠道种类-理财师渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=0, channelMode=1, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=0, channelname='', channelUseName='', channelPlatform='', channelMode=1, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0009(self):
        """MCI0009_渠道注册投资_按渠道种类-虚拟渠道查询
        操作步骤:
        渠道注册投资_按渠道种类-虚拟渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=0, channelMode=2, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=0, channelname='', channelUseName='', channelPlatform='', channelMode=2, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0010(self):
        """MCI0010_渠道注册投资_按负责人查询
        操作步骤:
        渠道注册投资_按负责人查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=0, channelMode=0, channelUseName='', page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=0, channelname='', channelUseName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCI0011(self):
        """MCI0011_渠道注册投资_综合查询
        操作步骤:
        渠道注册投资_综合查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, day=0, channelname='迅雷', channeltype=1, channelGroup=2, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, day=0, channelname='迅雷', channelUseName='', channelPlatform='', channelMode=0, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/invest/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道注册投资报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, ['channelEmpName'])    


class ChannelRechargeReport(unittest.TestCase):
    """营销报表渠道充值数据核算"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.diff = DataDiffLibrary()
        cls.cookie = cls.diff.login_interface(be_login_url, be_login_user_passwd)
       
    def setUp(self):
        self.start_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.ymd = time.strftime('%Y-%m-%d')
        self.ymdhms = time.strftime('%Y%m%d%H%M%S')

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCR0001(self):
        """MCR0001_渠道充值_按注册日期查询
        操作步骤:
        渠道充值_按注册日期查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelMode=0, channelgroup='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/channelRecharge/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCR0002(self):
        """MCR0002_渠道充值_按渠道名称查询
        操作步骤:
        渠道充值_按渠道名称查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate='2016-01-01', endDate=self.end_date, channelname='迅雷', channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime='2016-01-01', endTime=self.end_date, channelname='迅雷', channelMode=0, channelgroup='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/channelRecharge/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCR0003(self):
        """MCR0003_渠道充值_按渠道所属功能组查询
        操作步骤:
        渠道充值_按渠道所属功能组查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelGroup=3, channelMode=0, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelMode=0, channelgroup=3, rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/channelRecharge/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCR0004(self):
        """MCR0004_渠道充值_按渠道种类-理财师渠道查询
        操作步骤:
        渠道充值_按渠道种类-理财师渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelMode=1, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelMode=1, channelgroup='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/channelRecharge/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCR0005(self):
        """MCR0005_渠道充值_按渠道种类-虚拟渠道查询
        操作步骤:
        渠道充值_按渠道种类-虚拟渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelMode=2, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='', channelMode=2, channelgroup='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/channelRecharge/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, [])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MCR0006(self):
        """MCR0006_渠道充值_综合查询
        操作步骤:
        渠道充值_综合查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(beginDate=self.start_date, endDate=self.end_date, channelname='PC', channelMode=1, page=1, rows=50000)
        sql_earch = dict(startTime=self.start_date, endTime=self.end_date, channelname='PC', channelMode=1, channelgroup='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/user/channelRecharge/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表.sql', sql_earch) 
        right, count = right, count if not count else self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道充值报表汇总.sql', sql_earch, right) 
        self.diff.diff_data(left, right, [])    


class ChannelReport(unittest.TestCase):
    """营销报表渠道管理数据核算"""
    # 用例执行过滤标签
    tag = 'run'

    @classmethod
    def setUpClass(cls):
        # 导入自定义库
        cls.comlib = CommonLibrary()
        cls.diff = DataDiffLibrary()
        cls.cookie = cls.diff.login_interface(be_login_url, be_login_user_passwd)
       
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MC0001(self):
        """MC0001_渠道管理_默认条件查询
        操作步骤:
        渠道管理_默认条件查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='', username='', channelMode='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/manage/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['apiState', 'callbackState', 'recordState', 'channelEmpId', 'channelSupplierId'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MC0002(self):
        """MC0002_渠道管理_按渠道索引查询
        操作步骤:
        渠道管理_按渠道索引查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelindex='988e8787b63a25e0', page=1, rows=50000)
        sql_earch = dict(channelindex='988e8787b63a25e0', channelname='', username='', channelMode='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/manage/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['apiState', 'callbackState', 'recordState', 'channelEmpId', 'channelSupplierId'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MC0003(self):
        """MC0003_渠道管理_按渠道名称查询
        操作步骤:
        渠道管理_按渠道名称查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelname='迅雷', page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='迅雷', username='', channelMode='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/manage/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['apiState', 'callbackState', 'recordState', 'channelEmpId', 'channelSupplierId'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MC0004(self):
        """MC0004_渠道管理_按负责人查询
        操作步骤:
        渠道管理_按负责人查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='', username='', channelMode='', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/manage/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['apiState', 'callbackState', 'recordState', 'channelEmpId', 'channelSupplierId'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MC0005(self):
        """MC0005_渠道管理_按渠道种类-市场渠道查询
        操作步骤:
        渠道管理_按渠道种类-市场渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelMode=0, page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='', username='', channelMode='0', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/manage/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['apiState', 'callbackState', 'recordState', 'channelEmpId', 'channelSupplierId'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MC0006(self):
        """MC0006_渠道管理_按渠道种类-理财师渠道查询
        操作步骤:
        渠道管理_按渠道种类-理财师渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelMode=1, page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='', username='', channelMode='1', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/manage/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['apiState', 'callbackState', 'recordState', 'channelEmpId', 'channelSupplierId'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MC0007(self):
        """MC0007_渠道管理_按渠道种类-虚拟渠道查询
        操作步骤:
        渠道管理_按渠道种类-虚拟渠道查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelMode=2, page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='', username='', channelMode='2', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/manage/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['apiState', 'callbackState', 'recordState', 'channelEmpId', 'channelSupplierId'])    

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_MC0008(self):
        """MC0008_渠道管理_综合查询
        操作步骤:
        渠道管理_综合查询
        ======
        预期结果:         
        查询成功, 数据正确
        """
        be_search = dict(channelname='迅雷', username='', channelMode=0, page=1, rows=50000)
        sql_earch = dict(channelindex='', channelname='迅雷', username='', channelMode='0', rows=50000) 
        left, count = self.diff.get_interface_data(url='{}/be/marketing/channel/manage/list.json'.format(be_url), method='GET', body=be_search, cookie=self.cookie, key='rows') 
        right, count = self.diff.get_database_data(db_host, db_port, db_name, db_user, db_passwd, 
            'Resource/TestData/SQL/渠道管理.sql', sql_earch) 
        self.diff.diff_data(left, right, ['apiState', 'callbackState', 'recordState', 'channelEmpId', 'channelSupplierId'])    
