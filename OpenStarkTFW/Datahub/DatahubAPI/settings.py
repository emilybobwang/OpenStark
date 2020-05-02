from tornado.log import app_log as log
from tornado.web import gen
import os
import tormysql
import pymysql


# 数据库配置
db_host = '172.20.20.160'
db_port = 3306
db_name = 'Datahub'
db_user = 'test'
db_password = 'test1234'
db_charset = 'utf8'
db_pool_size = 150
db_pool_recycle = 3600
db_timeout = 5

# 应用配置
static_path = os.path.join(os.path.dirname(__file__), 'static')
cookie_secret = 'SQYMzDHiShGCl1gx/e4g5HHS7Be1UkPpk7eJxklvKmE='
websocket_ping_timeout = 5
xsrf_cookie = True
debug = True

cycle_time = 10    # 定时任务监控周期(秒)
log_url = ''    # 日志上报接口地址

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
