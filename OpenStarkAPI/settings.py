from tornado.log import app_log as log
from tornado.web import gen
import os
import tormysql
import pymysql


# 数据库配置
db_host = '172.20.20.160'
db_port = 3306
db_name = 'OpenStark'
db_name_other = 'xiaoniu_work_timp'
db_user = 'test'
db_password = 'test1234'
db_charset = 'utf8'
db_pool_size = 150
db_pool_recycle = 3600
db_timeout = 60

# 应用配置
static_path = os.path.join(os.path.dirname(__file__), 'static')
cookie_secret = 'SQYMzDHiShGCl1gx/e4g5HHS7Be1UkPpk7eJxklvKmE='
websocket_ping_timeout = 5
xsrf_cookie = True
debug = True

cycle_time = 10    # 定时任务监控周期(秒)
log_url = ''    # 日志上报接口地址
auto_login_url = 'http://172.20.20.160:8580/xiaoniu_web_tm/IPManager/ip_info/query'  # 自动登录用户查询接口地址
net_mail_to = ['pengpeng@xiaoniu66.com']   # 开通外网邮件申请接收人
net_mail_cc = ['pengpeng@xiaoniu66.com']    # 开通外网邮件申请抄送人
online_mail_to = ['pengpeng@xiaoniu66.com']   # 线上问题汇报邮件接收人
report_mail_cc = ['pengpeng@xiaoniu66.com']    # 测试报告邮件抄送人
host_160 = '172.20.20.160'
port_160 = '22'
user_160 = 'root'
password_160 = 'test123456'
root_160 = '/data/project/automation/OpenStark/OpenStarkAPI/static/syncDB'
jenkins_url = 'http://172.20.20.160:8091'
jenkins_user = 'admin'
jenkins_password = 'admin123456'
jenkins_jacoco = 'INNER_JACOCO测试覆盖率监控'
jenkins_docker = 'INNER_DOCKER_STATUS_MONITOR'

# 创建数据库连接池
pool = tormysql.helpers.ConnectionPool(
    max_connections=db_pool_size,
    idle_seconds=db_pool_recycle,
    wait_connection_timeout=db_timeout,
    host=db_host,
    port=db_port,
    user=db_user,
    passwd=db_password,
    db=db_name,
    charset=db_charset,
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)


# 初始化数据库
@gen.coroutine
def init_db():
    sql_file = os.path.join(os.path.dirname(__file__), 'OpenStark.sql')
    if os.path.isfile(sql_file):
        with open(sql_file, 'rb') as fp:
            sql_scripts = fp.read().decode('utf8')
        tx = yield pool.begin()
        log.info('初始化数据库SQL:\n{}'.format(sql_scripts))
        try:
            for sql in sql_scripts.split(';'):
                if sql:
                    yield tx.execute(sql)
        except pymysql.Error as e:
            yield tx.rollback()
            log.error('初始化数据库失败#{}'.format(e))
        else:
            yield tx.commit()
            log.info('初始化数据库成功')
