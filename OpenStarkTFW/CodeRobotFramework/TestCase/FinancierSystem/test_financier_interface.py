# coding=utf8
import unittest
from Resource.Variables.common import *
from Library.common_library import CommonLibrary
from Core.keys import builtin as bln


class FinancierInterface(unittest.TestCase):
    """理财师模块自动化用例 接口版"""
    # 导入自定义库
    comlib = CommonLibrary()
    # 用例执行过滤标签
    tag = 'run'

    @unittest.skip('手动执行定时任务进行初始化')
    def test_L1000(self):
        """L1000_理财师数据核算测试数据准备
        操作步骤:
        初始化理财师相关测试数据，新规新建理财师关系、老用户新建理财师关系、老用户老关系新投资
        ======
        预期结果:
        """
        his_time = self.comlib.mysql_query("SELECT e.earningDate FROM financier.`t_fp_earnings_day` e WHERE e.`type`=3 order by e.earningDate DESC limit 1;")    
        his_time = his_time[0][0]
        his_count = self.comlib.mysql_query("SELECT COUNT(*) FROM financier.`t_fp_earnings_day` e WHERE e.`earningDate` = DATE(ADDDATE('{}', INTERVAL -1 DAY)) and e.`type`=3;".format(his_time))
        count = self.comlib.mysql_query("SELECT COUNT(*) FROM financier.`t_fp_earnings_day` e WHERE e.`earningDate` = DATE(ADDDATE(Now(), INTERVAL -1 DAY)) and e.`type`=3;") 
        if count[0][0] == 0:
            self.comlib.exec_job_inter('新增理财师角色定级和收益发放任务')   
        for i in range(7200):
            count = self.comlib.mysql_query("SELECT COUNT(*) FROM financier.`t_fp_earnings_day` e WHERE e.`earningDate` = DATE(ADDDATE(Now(), INTERVAL -1 DAY)) and e.`type`=3;")        
            if count[0][0]>5000 and count[0][0]>his_count[0][0]-50:
                break
            else:
                bln.sleep(1)

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1001(self):
        """L1001_新用户新关系-新规则-好友待收2000<=D<10000
        操作步骤:
        每日待收
        核算新用户新关系，好友待收2000<=D<10000
        ======
        预期结果:
        好友1新待收*0.2%+…好友N*0.2% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY) ORDER BY r.`plannerId` DESC;") 
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`, r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>=2000 and amount<10000:
                break
        earnings_day = self.comlib.calc_new_earnings_day(res)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1002(self):
        """L1002_新用户新关系-新规则-好友待收10000<=D<100000
        操作步骤:
        每日待收
        核算新用户新关系，好友待收10000<=D<100000
        ======
        预期结果:
        好友1新待收*0.3%+…好友N*0.3% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY) ORDER BY r.`plannerId` DESC;") 
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>=10000 and amount<100000:
                break
        earnings_day = self.comlib.calc_new_earnings_day(res)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1003(self):
        """L1003_新用户新关系-新规则-好友待收>=100000
        操作步骤:
        每日待收
        核算新用户新关系，好友待收>=100000
        ======
        预期结果:
        好友1新待收*0.4%+…好友N*0.4% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY) ORDER BY r.`plannerId` DESC;") 
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>=100000:
                break
        earnings_day = self.comlib.calc_new_earnings_day(res)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1004(self):
        """L1004_新用户新关系-新规则-好友待收<2000
        操作步骤:
        每日待收
        核算新用户新关系，好友待收<2000
        ======
        预期结果:
        收益=0
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY) ORDER BY r.`plannerId` DESC;") 
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount<2000 and amount>0:
                break
        earnings_day = float(0)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1005(self):
        """L1005_老用户新关系-新规则-好友待收2000<=D<10000
        操作步骤:
        每日待收
        核算老用户新关系，好友待收2000<=D<10000
        ======
        预期结果:
        好友1新待收*0.2%+…好友N*0.2% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY);")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>=2000 and amount<10000:
                break
        earnings_day = self.comlib.calc_new_earnings_day(res)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1006(self):
        """L1006_老用户新关系-新规则-好友待收10000<=D<100000
        操作步骤:
        每日待收
        核算老用户新关系，好友待收10000<=D<100000
        ======
        预期结果:
        好友1新待收*0.3%+…好友N*0.3% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY);")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>=10000 and amount<100000:
                break
        earnings_day = self.comlib.calc_new_earnings_day(res)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1007(self):
        """L1007_老用户新关系-新规则-好友待收>=100000
        操作步骤:
        每日待收
        核算老用户新关系，好友待收>=100000
        ======
        预期结果:
        好友1新待收*0.4%+…好友N*0.4% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY);")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>=100000:
                break
        earnings_day = self.comlib.calc_new_earnings_day(res)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1008(self):
        """L1008_老用户新关系-新规则-好友待收<2000
        操作步骤:
        每日待收
        核算老用户新关系，好友待收<2000
        ======
        预期结果:
        收益=0
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY);")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>0 and amount<2000:
                break
        earnings_day = float(0)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1009(self):
        """L1009_老用户历史好友新投资-新规则-好友待收2000<=D<10000
        操作步骤:
        每日待收
        核算历史好友新投资，好友待收2000<=D<10000
        ======
        预期结果:
        好友1新待收*0.2%+…好友N*0.2% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`isOld`=1 AND r.`registerTime`<'2017-05-01' ORDER BY r.`plannerId` DESC;")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>=2000 and amount<10000:
                break
        earnings_day = self.comlib.calc_new_earnings_day(res)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1010(self):
        """L1010_老用户历史好友新投资-新规则-好友待收10000<=D<100000
        操作步骤:
        每日待收
        核算历史好友新投资，好友待收10000<=D<100000
        ======
        预期结果:
        好友1新待收*0.3%+…好友N*0.3% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`isOld`=1 AND r.`registerTime`<'2017-05-01' ORDER BY r.`plannerId` DESC;")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>=10000 and amount<100000:
                break
        earnings_day = self.comlib.calc_new_earnings_day(res)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1011(self):
        """L1011_老用户历史好友新投资-新规则-好友待收>=100000
        操作步骤:
        每日待收
        核算历史好友新投资，好友待收>=100000
        ======
        预期结果:
        好友1新待收*0.4%+…好友N*0.4% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`isOld`=1 AND r.`registerTime`<'2017-05-01' ORDER BY r.`plannerId` DESC;")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>=100000:
                break
        earnings_day = self.comlib.calc_new_earnings_day(res)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1012(self):
        """L1012_老用户历史好友新投资-新规则-好友待收<2000
        操作步骤:
        每日待收
        核算历史好友新投资，好友待收<2000
        ======
        预期结果:
        收益=0
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT * FROM financier.`t_fp_relationship` r JOIN financier.`t_user_role` fu ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` NOT IN (1,4) GROUP BY r.`plannerId` HAVING r.`isOld`=1 AND r.`registerTime`<'2017-05-01' ORDER BY r.`plannerId` DESC;")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={}".format(planterId)) 
            amount = self.comlib.get_user_returnAmount('true', res)
            if amount>0 and amount<2000:
                break
        earnings_day = float(0)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=3;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1013(self):
        """L1013_老用户历史好友-历史投资普通理财师1~4好友
        操作步骤:
        普通理财师待收大于5000，历史投资，1~4个历史好友
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`=0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1014(self):
        """L1014_老用户历史好友-历史投资普通理财师5~9好友
        操作步骤:
        普通理财师待收大于5000，历史投资，5~9个历史好友
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 AND fu.`returnAmount`>5000 AND fu.`newReturnAmount`=0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")    
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1015(self):
        """L1015_老用户历史好友-历史投资普通理财师10个好友及以上
        操作步骤:
        普通理财师待收大于5000，历史投资，10个以上历史好友
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`=0 group by r.`plannerId` having count(r.`plannerId`)>9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1016(self):
        """L1016_老用户历史好友-历史投资普通理财师待收<5000
        操作步骤:
        普通理财师待收小于5000
        ======
        预期结果:
        收益按新规则计算
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`<5000  and fu.`newReturnAmount`=0 group by r.`plannerId`;")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        if amount_one>=2000 and amount_one<10000:
            earnings_day = float(('%.4f' % ((amount_one*0.002)/365))[:-2])
        elif amount_one>=10000 and amount_one<100000:
            earnings_day = float(('%.4f' % ((amount_one*0.003)/365))[:-2])
        elif amount_one>=100000:
            earnings_day = float(('%.4f' % ((amount_one*0.004)/365))[:-2])
        else:
            earnings_day = float(0)
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1017(self):
        """L1017_老用户历史好友-历史投资金牌理财师1~4好友
        操作步骤:
        历史投资金牌理财师推荐好友1~4好友时
        ======
        预期结果:
        (好友*0.01+好友推荐好友*0.002)/365)
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId` = fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` = 3 AND fu.`returnAmount` > 50000 AND fu.`newReturnAmount` = 0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`) < 4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId` = rr.`plannerId` WHERE fuu.`returnAmount` > 0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(), INTERVAL - 1 YEAR)));")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01+amount_two*0.002)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1018(self):
        """L1018_老用户历史好友-历史投资金牌理财师5~9好友
        操作步骤:
        历史投资金牌理财师推荐好友5~9好友时
        ======
        预期结果:
        (好友*0.01+好友推荐好友*0.003)/365)
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`=0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1019(self):
        """L1019_老用户历史好友-历史投资金牌理财师10个好友及以上
        操作步骤:
        历史投资金牌理财师推荐好友10个好友以上
        ======
        预期结果:
        (好友*0.01+好友推荐好友*0.004)/365)
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 and fu.`returnAmount`>50000 and fu.`newReturnAmount`=0 group by r.`plannerId` having count(r.`plannerId`)>9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));") 
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01+amount_two*0.004)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1020(self):
        """L1020_老用户历史好友-历史投资金牌理财师待收5000<M<50000-1~4好友
        操作步骤:
        历史投资金牌理财师待收5000<M<50000 1~4个好友
        ======
        预期结果:
        (好友*0.006+好友推荐好友*0.002)/365)
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId` = fu.`userId` WHERE fu.`isDel` = 0 AND fu.`returnAmount` BETWEEN 5000 AND 50000 AND fu.`newReturnAmount` = 0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId` = rr.`plannerId` WHERE fuu.`returnAmount` > 0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(), INTERVAL - 1 YEAR)));")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.006+amount_two*0.002)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1021(self):
        """L1021_老用户历史好友-历史投资金牌理财师待收5000<M<50000-5~9好友
        操作步骤:
        历史投资理财师待收5000<M<50000 5~9个好友
        ======
        预期结果:
        (好友*0.006+好友推荐好友*0.003)/365)
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId` = fu.`userId` WHERE fu.`isDel` = 0 AND fu.`returnAmount` BETWEEN 5000 AND 50000 AND fu.`newReturnAmount` = 0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId` = rr.`plannerId` WHERE fuu.`returnAmount` > 0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(), INTERVAL - 1 YEAR)));")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.006+amount_two*0.003)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1022(self):
        """L1022_老用户历史好友-历史投资金牌理财师待收5000<M<50000-10个好友及以上
        操作步骤:
        历史投资理财师待收5000<M<50000 10个好友以上
        ======
        预期结果:
        (好友*0.006+好友推荐好友*0.004)/365)
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId` = fu.`userId` WHERE fu.`isDel` = 0 AND fu.`returnAmount` BETWEEN 5000 AND 50000 AND fu.`newReturnAmount` = 0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`) >10 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId` = rr.`plannerId` WHERE fuu.`returnAmount` > 0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(), INTERVAL - 1 YEAR)));")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.006+amount_two*0.004)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(e.`earnings`,0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY)) AND e.`type`=1;".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1023(self):
        """L1023_老用户历史好友-历史投资金牌理财师待收<5000
        操作步骤:
        历史投资理财师待收<5000
        ======
        预期结果:
        理财师待收小于5000，收益为0
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId` = fu.`userId` WHERE fu.`isDel` = 0 AND fu.`returnAmount` < 5000 AND fu.`newReturnAmount` = 0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`) AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId` = rr.`plannerId` WHERE fuu.`returnAmount` > 0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(), INTERVAL - 1 YEAR)));")
        for row in result:
            planterId = row[1]
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[2]))
            amount = self.comlib.get_user_returnAmount('false', res)
            if amount!=0:
                break
        result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.006+amount_two*0.002)/365))[:-2])
        earnings_day_actual = float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1024(self):
        """L1024_老用户历史好友-历史+新投资普通理财师1~4好友-好友待收2000<=D<10000
        操作步骤:
        历史好友新投资+历史投资，1<=好友数<=4，2000<=好友待收<10000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.2%+一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1025(self):
        """L1025_老用户历史好友-历史+新投资普通理财师1~4好友-好友待收10000<=D<100000
        操作步骤:
        历史好友新投资+历史投资，1<=好友数<=4，2000<=好友待收<10000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.2%+一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=10000 and amount_all<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1026(self):
        """L1026_老用户历史好友-历史+新投资普通理财师1~4好友-好友待收>=100000
        操作步骤:
        历史好友新投资+历史投资，1<=好友数<=4，2000<=好友待收<10000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.2%+一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1027(self):
        """L1027_老用户历史好友-历史+新投资普通理财师5~9好友-好友待收2000<=D<10000
        操作步骤:
        普通理财师，历史+新投资，5<=好友数<=9，2000<=好友新待收<10000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.3%+一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1028(self):
        """L1028_老用户历史好友-历史+新投资普通理财师5~9好友-好友待收10000<=D<100000
        操作步骤:
        普通理财师，历史+新投资，5<=好友数<=9，10000<=好友新待收<100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.3%+一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=10000 and amount_all<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1029(self):
        """L1029_老用户历史好友-历史+新投资普通理财师5~9好友-好友待收>=100000
        操作步骤:
        普通理财师，历史+新投资，5<=好友数<=9，好友新待收>=100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.3%+一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1030(self):
        """L1030_老用户历史好友-历史+新投资普通理财师10个好友及以上-好友待收2000<=D<10000
        操作步骤:
        普通理财师，历史+新投资，好友数>10，2000<=好友新待收<10000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.4%+一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)>9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1031(self):
        """L1031_老用户历史好友-历史+新投资普通理财师10个好友及以上-好友待收10000<=D<100000
        操作步骤:
        普通理财师，历史+新投资，好友数>10，10000<=好友新待收<100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.4%+一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)>9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=10000 and amount_all<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1032(self):
        """L1032_老用户历史好友-历史+新投资普通理财师10个好友及以上-好友待收>=100000
        操作步骤:
        普通理财师，历史+新投资，好友数>10，好友新待收>=100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.4%+一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 and fu.`returnAmount`>5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)>9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1033(self):
        """L1033_老用户历史好友-历史+新投资普通理财师待收<5000,>0-好友待收2000<=D<10000
        操作步骤:
        普通理财师，历史+新投资，待收<5000，2000<=好友新待收<10000
        ======
        预期结果:
        收益=一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 AND fu.`newReturnAmount` BETWEEN 2000 AND 10000 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)<4 AND r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY) ORDER BY r.`plannerId` DESC;")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1034(self):
        """L1034_老用户历史好友-历史+新投资普通理财师待收<5000,>0-好友待收10000<=D<100000
        操作步骤:
        普通理财师，历史+新投资，待收<5000，10000<好友新待收<100000
        ======
        预期结果:
        收益=一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 AND fu.`newReturnAmount` BETWEEN 10000 AND 100000 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)<4 AND r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY) ORDER BY r.`plannerId` DESC;")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1035(self):
        """L1035_老用户历史好友-历史+新投资普通理财师待收<5000,>0-好友待收>=100000
        操作步骤:
        普通理财师，历史+新投资，待收<5000，好友新待收>=100000
        ======
        预期结果:
        收益=一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 AND fu.`newReturnAmount` > 100000 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)<4 AND r.`registerTime`< ADDDATE(NOW(),INTERVAL -2 DAY) ORDER BY r.`plannerId` DESC;")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1036(self):
        """L1036_老用户历史好友-历史+新投资普通理财师无历史投资-好友待收2000<=D<10000
        操作步骤:
        历史好友关系，无待收，2000<=好友待收<10000
        ======
        预期结果:
        收益=0
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 AND fu.`returnAmount`=0;")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1037(self):
        """L1037_老用户历史好友-历史+新投资普通理财师无历史投资-好友待收10000<=D<100000
        操作步骤:
        历史好友关系，无待收，10000<=好友待收<100000
        ======
        预期结果:
        收益=0
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 AND fu.`returnAmount`=0;")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1038(self):
        """L1038_老用户历史好友-历史+新投资普通理财师无历史投资-好友待收>=100000
        操作步骤:
        历史好友关系，无待收，好友待收>=100000
        ======
        预期结果:
        收益=0
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =2 AND fu.`returnAmount`=0;")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1039(self):
        """L1039_老用户历史好友-历史+新投资金牌理财师1~4好友-好友待收2000<=D<10000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师1~4好友-好友待收2000<=D<10000
        ======
        预期结果:
        收益=一级总待收*1%+二级总待收*0.2%+一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`>0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1040(self):
        """L1040_老用户历史好友-历史+新投资金牌理财师1~4好友-好友待收10000<=D<100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师1~4好友-好友待收10000<=D<100000
        ======
        预期结果:
        收益=一级总待收*1%+二级总待收*0.2%+一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`>0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=10000 and amount_all<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1041(self):
        """L1041_老用户历史好友-历史+新投资金牌理财师1~4好友-好友待收>=100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师1~4好友-好友待收>=100000
        ======
        预期结果:
        收益=一级总待收*1%+二级总待收*0.2%+一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`>0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1042(self):
        """L1042_老用户历史好友-历史+新投资金牌理财师5~9好友-好友待收2000<=D<10000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师5~9好友-好友待收2000<=D<10000
        ======
        预期结果:
        收益=一级总待收*1%+二级总待收*0.3%+一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`>0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`) between 5 and 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1043(self):
        """L1043_老用户历史好友-历史+新投资金牌理财师5~9好友-好友待收10000<=D<100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师5~9好友-好友待收10000<=D<100000
        ======
        预期结果:
        收益=一级总待收*1%+二级总待收*0.3%+一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`>0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`) between 5 and 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=10000 and amount_all<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1044(self):
        """L1044_老用户历史好友-历史+新投资金牌理财师5~9好友-好友待收>=100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师5~9好友-好友待收>=100000
        ======
        预期结果:
        收益=一级总待收*1%+二级总待收*0.3%+一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`>0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`) between 5 and 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1045(self):
        """L1045_老用户历史好友-历史+新投资金牌理财师10个好友及以上-好友待收2000<=D<10000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师10个好友及以上-好友待收2000<=D<10000
        ======
        预期结果:
        收益=一级总待收*1%+二级总待收*0.4%+一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`>0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)>=10 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1046(self):
        """L1046_老用户历史好友-历史+新投资金牌理财师10个好友及以上-好友待收10000<=D<100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师10个好友及以上-好友待收10000<=D<100000
        ======
        预期结果:
        收益=一级总待收*1%+二级总待收*0.4%+一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`>0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)>=10 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=10000 and amount_all<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1047(self):
        """L1047_老用户历史好友-历史+新投资金牌理财师10个好友及以上-好友待收>=100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师10个好友及以上-好友待收>=100000
        ======
        预期结果:
        收益=一级总待收*1%+二级总待收*0.4%+一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu JOIN financier.`t_fp_relationship` r ON r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` =3 AND fu.`returnAmount`>50000 AND fu.`newReturnAmount`>0 GROUP BY r.`plannerId` HAVING COUNT(r.`plannerId`)>=10 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1048(self):
        """L1048_老用户历史好友-历史+新投资金牌理财师待收<50000-1~4好友-好友待收2000<=D<10000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师待收<50000-1~4好友-好友待收2000<=D<10000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.2%+一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` not in (1,4) and fu.`returnAmount` BETWEEN 5000 AND 50000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1049(self):
        """L1049_老用户历史好友-历史+新投资金牌理财师待收<50000-1~4好友-好友待收10000<=D<100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师待收<50000-1~4好友-好友待收10000<=D<100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.2%+一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` not in (1,4) and fu.`returnAmount` BETWEEN 5000 AND 50000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=10000 and amount_all<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1050(self):
        """L1050_老用户历史好友-历史+新投资金牌理财师待收<50000-1~4好友-好友待收>=100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师待收<50000-1~4好友-好友待收>=100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.2%+一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` not in (1,4) and fu.`returnAmount` BETWEEN 5000 AND 50000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1051(self):
        """L1051_老用户历史好友-历史+新投资金牌理财师待收<50000-5~9好友-好友待收2000<=D<10000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师待收<50000-5~9好友-好友待收2000<=D<10000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.3%+一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` not in (1,4) and fu.`returnAmount` BETWEEN 5000 AND 50000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1052(self):
        """L1052_老用户历史好友-历史+新投资金牌理财师待收<50000-5~9好友-好友待收10000<=D<100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师待收<50000-5~9好友-好友待收10000<=D<100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.3%+一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` not in (1,4) and fu.`returnAmount` BETWEEN 5000 AND 50000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=10000 and amount_all<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1053(self):
        """L1053_老用户历史好友-历史+新投资金牌理财师待收<50000-5~9好友-好友待收>=100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师待收<50000-5~9好友-好友待收>=100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.3%+一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` not in (1,4) and fu.`returnAmount` BETWEEN 5000 AND 50000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1054(self):
        """L1054_老用户历史好友-历史+新投资金牌理财师待收<50000-10个好友及以上-好友待收2000<=D<10000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师待收<50000-10个好友及以上-好友待收2000<=D<10000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.4%+一级新待收*0.2%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` not in (1,4) and fu.`returnAmount` BETWEEN 5000 AND 50000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)>9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=2000 and amount_all<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1055(self):
        """L1055_老用户历史好友-历史+新投资金牌理财师待收<50000-10个好友及以上-好友待收10000<=D<100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师待收<50000-10个好友及以上-好友待收10000<=D<100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.4%+一级新待收*0.3%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId`not in (1,4) and fu.`returnAmount` BETWEEN 5000 AND 50000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=10000 and amount_all<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1056(self):
        """L1056_老用户历史好友-历史+新投资金牌理财师待收<50000-10个好友及以上-好友待收>=100000
        操作步骤:
        老用户历史好友-历史+新投资金牌理财师待收<50000-10个好友及以上-好友待收>=100000
        ======
        预期结果:
        收益=一级总待收*0.6%+二级总待收*0.4%+一级新待收*0.4%
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId`not in (1,4) and fu.`returnAmount` BETWEEN 5000 AND 50000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)>9 AND r.`plannerId` IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -1 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(planterId))
            amount_all = self.comlib.get_user_returnAmount('all', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount_all>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('false', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('false', res)
            amount_two += amount
        amount_new = self.comlib.calc_new_earnings_day(result)
        earnings_day = float(('%.4f' % ((amount_one*0.006)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])+amount_new
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1057(self):
        """L1057_老用户历史好友-历史+新投资内部理财师待收<5000-1~4好友-好友待收2000<=D<10000
        操作步骤:
        老用户历史好友-历史+新投资内部理财师待收<5000-1~4好友-好友待收2000<=D<10000
        ======
        预期结果:
        收益=好友1新待收*0.2%+…好友N*0.2% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` = 1 and fu.`returnAmount`< 5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` not IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r WHERE r.`plannerId`={} AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR));".format(planterId))
            amount = self.comlib.get_user_returnAmount('xiaoniu', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount>=2000 and amount<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('xiaoniu', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('xiaoniu', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1058(self):
        """L1058_老用户历史好友-历史+新投资内部理财师待收<5000-1~4好友-好友待收10000<=D<100000
        操作步骤:
        老用户历史好友-历史+新投资内部理财师待收<5000-1~4好友-好友待收10000<=D<100000
        ======
        预期结果:
        收益=好友1新待收*0.3%+…好友N*0.3% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` = 1 and fu.`returnAmount`<5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` not IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r WHERE r.`plannerId`={} AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR));".format(planterId))
            amount = self.comlib.get_user_returnAmount('xiaoniu', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount>=10000 and amount<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('xiaoniu', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('xiaoniu', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1059(self):
        """L1059_老用户历史好友-历史+新投资内部理财师待收<5000-1~4好友-好友待收>=100000
        操作步骤:
        老用户历史好友-历史+新投资内部理财师待收<5000-1~4好友-好友待收>=100000
        ======
        预期结果:
        收益=好友1新待收*0.4%+…好友N*0.4% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` = 1 and fu.`returnAmount`<5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)<4 AND r.`plannerId` not IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r WHERE r.`plannerId`={} AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR));".format(planterId))
            amount = self.comlib.get_user_returnAmount('xiaoniu', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('xiaoniu', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('xiaoniu', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.002)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1060(self):
        """L1060_老用户历史好友-历史+新投资内部理财师待收<5000-5~9好友-好友待收2000<=D<10000
        操作步骤:
        老用户历史好友-历史+新投资内部理财师待收<5000-5~9好友-好友待收2000<=D<10000
        ======
        预期结果:
        收益=好友1新待收*0.2%+…好友N*0.2% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` = 1 and fu.`returnAmount`<5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` not IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r WHERE r.`plannerId`={} AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR));".format(planterId))
            amount = self.comlib.get_user_returnAmount('xiaoniu', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount>=2000 and amount<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('xiaoniu', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('xiaoniu', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1061(self):
        """L1061_老用户历史好友-历史+新投资内部理财师待收<5000-5~9好友-好友待收10000<=D<100000
        操作步骤:
        老用户历史好友-历史+新投资内部理财师待收<5000-5~9好友-好友待收10000<=D<100000
        ======
        预期结果:
        收益=好友1新待收*0.3%+…好友N*0.3% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0  AND fu.`roleId` = 1 and fu.`returnAmount`<5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` not IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r WHERE r.`plannerId`={} AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR));".format(planterId))
            amount = self.comlib.get_user_returnAmount('xiaoniu', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount>=10000 and amount<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('xiaoniu', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('xiaoniu', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1062(self):
        """L1062_老用户历史好友-历史+新投资内部理财师待收<5000-5~9好友-好友待收>=100000
        操作步骤:
        老用户历史好友-历史+新投资内部理财师待收<5000-5~9好友-好友待收>=100000
        ======
        预期结果:
        收益=好友1新待收*0.4%+…好友N*0.4% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` = 1 and fu.`returnAmount`<5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` not IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r WHERE r.`plannerId`={} AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR));".format(planterId))
            amount = self.comlib.get_user_returnAmount('xiaoniu', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('xiaoniu', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('xiaoniu', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.003)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1063(self):
        """L1063_老用户历史好友-历史+新投资内部理财师待收<5000-10个好友及以上-好友待收2000<=D<10000
        操作步骤:
        老用户历史好友-历史+新投资内部理财师待收<5000-10个好友及以上-好友待收2000<=D<10000
        ======
        预期结果:
        收益=好友1新待收*0.2%+…好友N*0.2% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` = 1 and fu.`returnAmount`<5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)>9 AND r.`plannerId` not IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r WHERE r.`plannerId`={} AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR));".format(planterId))
            amount = self.comlib.get_user_returnAmount('xiaoniu', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount>=2000 and amount<10000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('xiaoniu', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('xiaoniu', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1064(self):
        """L1064_老用户历史好友-历史+新投资内部理财师待收<5000-10个好友及以上-好友待收10000<=D<100000
        操作步骤:
        老用户历史好友-历史+新投资内部理财师待收<5000-10个好友及以上-好友待收10000<=D<100000
        ======
        预期结果:
        收益=好友1新待收*0.3%+…好友N*0.3% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` = 1 and fu.`returnAmount`<5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`) BETWEEN 5 AND 9 AND r.`plannerId` not IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r WHERE r.`plannerId`={} AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR));".format(planterId))
            amount = self.comlib.get_user_returnAmount('xiaoniu', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount>=10000 and amount<100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('xiaoniu', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('xiaoniu', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 

    @unittest.skipUnless(tag == 'run', '已忽略执行')
    def test_L1065(self):
        """L1065_老用户历史好友-历史+新投资内部理财师待收<5000-10个好友及以上-好友待收>=100000
        操作步骤:
        老用户历史好友-历史+新投资内部理财师待收<5000-10个好友及以上-好友待收>=100000
        ======
        预期结果:
        收益=好友1新待收*0.4%+…好友N*0.4% &&90天收益
        """
        planterId = 0
        result = self.comlib.mysql_query("SELECT r.* FROM financier.`t_user_role` fu join financier.`t_fp_relationship` r on r.`plannerId`=fu.`userId` WHERE fu.`isDel` = 0 AND fu.`roleId` = 1 and fu.`returnAmount`<5000 and fu.`newReturnAmount`>0 group by r.`plannerId` having count(r.`plannerId`)>9 AND r.`plannerId` not IN (SELECT rr.`userId` FROM financier.`t_fp_relationship` rr JOIN financier.`t_user_role` fuu ON fuu.`userId`=rr.`plannerId` WHERE fuu.`returnAmount`>0 AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR)));")
        for row in result:
            planterId = row[1]
            result = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r WHERE r.`plannerId`={} AND DATE(r.`createTime`) > DATE(ADDDATE(NOW(),INTERVAL -2 YEAR));".format(planterId))
            amount = self.comlib.get_user_returnAmount('xiaoniu', result)
            amount_new = self.comlib.get_user_returnAmount('true', result)
            if amount>=100000 and amount_new>0:
                break
        amount_one = self.comlib.get_user_returnAmount('xiaoniu', result)
        amount_two = 0
        for row in result:
            res = self.comlib.mysql_query("SELECT r.`userId`,r.`createTime` FROM financier.`t_fp_relationship` r where r.`plannerId`={} and date(r.`createTime`) > date(adddate(now(),interval -1 year));".format(row[0]))
            amount = self.comlib.get_user_returnAmount('xiaoniu', res)
            amount_two += amount
        earnings_day = float(('%.4f' % ((amount_one*0.01)/365))[:-2])+float(('%.4f' % ((amount_two*0.004)/365))[:-2])
        earnings_day_actual = self.comlib.mysql_query("SELECT IFNULL(SUM(e.`earnings`),0) FROM financier.`t_fp_earnings_day` e WHERE e.`plannerId`={} AND e.`earningDate` = DATE(ADDDATE(NOW(), INTERVAL -1 DAY));".format(planterId))
        earnings_day_actual = bln.convert_to_number(earnings_day_actual[0][0]) if len(earnings_day_actual)>0 else float(0)
        self.assertAlmostEqual(earnings_day, earnings_day_actual, msg='理财师收益核对不一致', delta=0.01) 
