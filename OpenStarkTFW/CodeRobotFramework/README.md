# CodeRobotFramework(CRF)
不想填表格？文本模式编辑没有直接写代码的感觉？试试code版robotframework吧, 基于unittest编写测试用例, 完全支持robotframework内置关键字和扩展库关键字, 可同时生成HTML格式测试报告和JUnit XML格式报告, 可直接集成到Jenkins中执行并查看结果。 
同时集成了将测试结果上传到云测试平台的脚本, 可获取云测试平台上的用例自动生成测试用例函数, 在编写测试用例脚本时, 按格式添加注释后, 也可自动生成测试用例上传到云测试平台, 避免了需要写多份用例及修改用例的麻烦。
后续将与大进军的框架融合, 以实现云测试平台多执行引擎的特性。

## 需要安装的模块
```
pip install -U parameterized unittest-xml-reporting html-testRunner requests selenium \
pymysql pymongo robotframework robotframework-seleniumlibrary==3.0.0b3 \
robotframework-requests robotframework-databaselibrary \
robotframework-ftplibrary robotframework-appiumlibrary \
robotframework-archivelibrary robotframework-difflibrary pyautogui rabird.winio \
robotframework-mongodbLibrary https://github.com/TronGeek/robotframework-QTLibrary/archive/master.zip
```

## 可选安装的模块
```
pip install -U robotframework-selenium2library \
robotframework-extendedselenium2library robotframework-httplibrary \
robotframework-faker robotframework-ncclient robotremoteserver
```

## 目录结构说明
```
├─Core          框架核心库
│  ├─Keywords   函数库
│  └─Runner     运行库
├─Library       自定义库
├─Resource      资源
│  ├─TestData   测试数据
│  │  ├─Files   普通文件
│  │  └─SQL     SQL文件
│  └─Variables  配置/变量
├─Results       测试结果
├─TestCase      测试用例
├─RunTestSuites.py  测试执行入口脚本, 在此脚本中修改需要测试的用例及调整测试执行顺序, 具体看注释
└─UploadReport.py   测试结果上传脚本, 上传到云测试平台, 可获取云测试平台上的用例自动生成测试用例函数, 具体看注释
```

## 用例注释格式说明
编写用例时增加注释可以对测试用例进行必要的描述, 同时在生成测试报告时会获取注释内容以便在测试报告中显示测试标题、操作步骤和预期结果。
```
import unittest

class TestSuite(unittest.TestCase):
    def test_case(self):
        """用例编号_用例标题
        操作步骤：
        1、
        2、
        3、
        ======
        预期结果：
        1、
        2、
        """
        pass
```
>Ps: 用例编号_用例标题必须写在第一行, 换行编写操作步骤和预期结果, 操作步骤与预期结果之间用======分隔开, 至少包含6个等号。
