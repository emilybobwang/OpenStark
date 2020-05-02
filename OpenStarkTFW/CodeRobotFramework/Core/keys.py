# encoding=utf8


from .Keywords.appium import CRFAppium
from .Keywords.archive import CRFArchive
from .Keywords.builtin import CRFBuiltIn
from .Keywords.database import CRFDatabase
from .Keywords.diff import CRFDiff
# from .Keywords.Ftp import CRFFtp
# from .Keywords.Mongo import CRFMongo
from .Keywords.data_generator import DataGenerator
from .Keywords.requests import CRFRequests
from .Keywords.selenium import CRFSelenium
# from .Keywords.keyboard import Keyboard


# 初始化关键字
webdriver = CRFSelenium()
requests = CRFRequests()
gen_data = DataGenerator()
# mongo = CRFMongo()
# ftp = CRFFtp()
diff = CRFDiff()
database = CRFDatabase()
archive = CRFArchive()
appdriver = CRFAppium()
builtin = CRFBuiltIn()
# keyboard = Keyboard()
