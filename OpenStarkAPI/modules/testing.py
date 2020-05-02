from tornado import gen
from tornado.log import app_log as log
import tormysql
import pymysql


class TestingModule(object):
    """
    动态连接数据库查询
    """
    def __init__(self, engine, host, user, password, database, sql, port=3306, charset='utf8'):
        self.engine = engine
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.sql = sql.splitlines()
        self._conn()

    # 建立数据库连接
    def _conn(self):
        if self.engine == 'mysql':
            conn = tormysql.helpers.ConnectionPool(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.password,
                db=self.database,
                charset=self.charset,
                cursorclass = pymysql.cursors.DictCursor,
            )
            self.pool = conn
        else:
            self.pool = None

    # 获取所有查询结果
    @gen.coroutine
    def get_all_result(self):
        try:
            cursor = yield self.pool.execute('\n'.join(self.sql))
            result = cursor.fetchall()
            cursor.close()
            yield self.pool.close()
            return result
        except Exception as e:
            log.error(e)
            return []

    # 获取查询结果的第一条
    @gen.coroutine
    def get_one_result(self):
        try:
            cursor = yield self.pool.execute('\n'.join(self.sql))
            result = cursor.fetchone()
            cursor.close()
            yield self.pool.close()
            return result
        except Exception as e:
            log.error(e)
            return None

    # 执行多条混合语句
    @gen.coroutine
    def run_some_sql(self):
        with (yield self.pool.Connection()) as conn:
            with conn.cursor() as cursor:
                results = list()
                res, msg = False, ''
                sql = []
                total = 0
                for s in self.sql:
                    total += 1
                    if not s.strip().endswith(';') and total != len(self.sql):
                        sql.append(s)
                        continue
                    sql.append(s)
                    sql_str = '\n'.join(sql)
                    if not sql_str.strip():
                        continue
                    log.info('RUN SQL: {}'.format(sql_str))
                    try:
                        yield cursor.execute(sql_str)
                        result = cursor.fetchall()
                        result and results.append(result)
                    except pymysql.Error as e:
                        yield conn.rollback()
                        log.error('执行多条混合语句失败#{}'.format(e))
                        res, msg =  False, '执行多条混合语句失败#{}'.format(e)
                        break
                    else:
                        yield conn.commit()
                        log.info('执行多条混合语句成功')
                        res, msg = True, '执行多条混合语句成功(无返回结果集)'
                    sql = []
                return res, results or msg
