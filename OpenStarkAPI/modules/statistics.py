from settings import pool
from tornado.log import app_log as log
from tornado import gen
from munch import munchify
import pymysql
import json


class StatisticsModule(object):
    """
    统计表相关操作
    """
    # 新增统计信息
    @gen.coroutine
    def add_statistics(self, s_type, name, value=None, user_id=0, project_id=0, status=1):
        if value is None:
            value = dict()
        sql = """INSERT INTO t_statistics (`userId`, `projectId`, `type`, `name`, `value`, `status`) 
        VALUE (%(userId)s, %(projectId)s, %(type)s, %(name)s, %(value)s, %(status)s)
        """
        with (yield pool.Connection()) as conn:
            with conn.cursor() as cursor:
                try:
                    yield cursor.execute(sql, dict(userId=user_id, projectId=project_id, name=name, status=status,
                                                   type=s_type, value=json.dumps(value, ensure_ascii=False)))
                except pymysql.Error as e:
                    yield conn.rollback()
                    log.error('新增统计信息失败#{}'.format(e))
                    flag, msg = False, '新增统计信息失败#{}'.format(e)
                else:
                    yield conn.commit()
                    log.info('新增统计信息成功')
                    flag, msg = cursor.lastrowid, '新增统计信息成功'
        return flag, msg

    # 删除统计信息
    @gen.coroutine
    def delete_statistics(self, s_type=None, user_id=None, project_id=None, name=None, sid=None):
        where = []
        param = dict()
        if s_type is not None:
            where.append("type=%(type)s")
            param['type'] = s_type
        if project_id is not None:
            where.append("projectId=%(projectId)s")
            param['projectId'] = project_id
        if user_id is not None:
            where.append("userId=%(userId)s")
            param['userId'] = user_id
        if name is not None:
            where.append("name=%(name)s")
            param['name'] = name
        if sid is not None:
            where.append("id=%(sid)s")
            param['sid'] = sid
        if where:
            sql = "DELETE FROM t_statistics WHERE {}".format(' AND '.join(where))
            tx = yield pool.begin()
            try:
                yield tx.execute(sql, param)
            except pymysql.Error as e:
                yield tx.rollback()
                log.error('删除统计信息失败#{}'.format(e))
                flag, msg = False, '删除统计信息失败#{}'.format(e)
            else:
                yield tx.commit()
                log.info('删除统计信息成功')
                flag, msg = True, '删除统计信息成功'
        else:
            log.error('没有指定统计信息, 删除失败')
            flag, msg = False, '没有指定统计信息, 删除失败'
        return flag, msg

    # 编辑统计信息
    @gen.coroutine
    def edit_statistics(self, status, s_type=None, user_id=None, project_id=None, name=None, sid=None):
        where = []
        param = dict(status=status)
        if s_type is not None:
            where.append("s.type=%(type)s")
            param['type'] = s_type
        if sid is not None:
            where.append("s.id=%(sid)s")
            param['sid'] = sid
        if user_id is not None:
            where.append("s.userId=%(userId)s")
            param['userId'] = user_id
        if project_id is not None:
            where.append("s.projectId=%(projectId)s")
            param['projectId'] = project_id
        if name is not None:
            where.append("s.name=%(name)s")
            param['name'] = name
        statistics = yield self.get_statistics(s_type=s_type, user_id=user_id, project_id=project_id,
                                               sid=sid, name=None, status=status)
        if where and statistics:
            sql = "UPDATE t_statistics s SET status=%(status)s WHERE {}".format(' AND '.join(where))
            tx = yield pool.begin()
            try:
                yield tx.execute(sql, param)
            except pymysql.Error as e:
                yield tx.rollback()
                log.error('统计信息 {} 编辑失败#{}'.format(statistics.name, e))
                flag, msg = False, '统计信息 {} 编辑失败#{}'.format(statistics.name, e)
            else:
                yield tx.commit()
                log.info('统计信息 {} 编辑成功'.format(statistics.name))
                flag, msg = True, '统计信息 {} 编辑成功'.format(statistics.name)
        else:
            log.error('没有可编辑的统计信息')
            flag, msg = False, '没有可编辑的统计信息'
        return flag, msg

    # 获取统计信息
    @gen.coroutine
    def get_statistics(self, s_type=None, user_id=None, project_id=None, name=None, sid=None, status=None):
        where = []
        param = dict()
        if s_type is not None:
            where.append("s.type=%(type)s")
            param['type'] = s_type
        if user_id is not None:
            where.append("s.userId=%(userId)s")
            param['userId'] = user_id
        if sid is not None:
            where.append("s.id=%(sid)s")
            param['sid'] = sid
        if project_id is not None:
            where.append("s.projectId=%(projectId)s")
            param['projectId'] = project_id
        if name is not None:
            where.append("s.name=%(name)s")
            param['name'] = name
        if status is not None:
            where.append("s.status=%(status)s")
            param['status'] = status
        if where:
            try:
                sql = "SELECT * FROM t_statistics s WHERE {}".format(' AND '.join(where))
                cursor = yield pool.execute(sql, param)
                result = cursor.fetchone()
                cursor.close()
                return munchify(result)
            except pymysql.Error as e:
                log.error(e)
                return None
        else:
            log.error('参数不对, 获取统计信息失败')
            return None

    # 获取所有统计信息
    @gen.coroutine
    def get_statistics_list(self, s_type=None, user_id=None, project_id=None, name=None, status=None, search=None,
                            page=1, limit=None, group_by=list(), start_time=None, end_time=None, order_by=list()):
        where = []
        param = dict()
        sql = '''SELECT p.name projectName, s.projectId, s.name, s.id, p.config, s.value 
        FROM t_statistics s JOIN t_projects p ON p.id=s.projectId'''
        if s_type is not None:
            where.append("s.type=%(type)s")
            param['type'] = s_type
        if user_id is not None:
            where.append("s.userId=%(userId)s")
            param['userId'] = user_id
        if project_id is not None:
            where.append("s.projectId=%(projectId)s")
            param['projectId'] = project_id
        if name is not None:
            where.append("s.name=%(name)s")
            param['name'] = name
        if status is not None:
            where.append("s.status=%(status)s")
            param['status'] = status
        if search is not None:
            where.append('(p.name LIKE %(search)s OR p.config LIKE %(search)s)')
            param['search'] = '%{}%'.format(search)
        if start_time and end_time:
            where.append("s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59'".format(start_time, end_time))
        if where:
            sql += " WHERE {}".format(' AND '.join(where))
        if group_by:
            sql += ' GROUP BY {}'.format(','.join(group_by))
        count_sql = "SELECT COUNT(*) count FROM ({}) as tmp".format(sql)
        if order_by:
            sql += ' ORDER BY {}'.format(','.join(order_by))
        if limit is not None:
            offset = (page - 1) * limit
            sql += ' LIMIT {},{}'.format(offset, limit)
        try:
            cursor = yield pool.execute(sql, param)
            result = cursor.fetchall()
            cursor = yield pool.execute(count_sql, param)
            total = cursor.fetchone()
            cursor.close()
            return munchify(result), munchify(total).count
        except pymysql.Error as e:
            log.error(e)
            return [], 0

    # 数据统计
    @gen.coroutine
    def statistics(self, s_type=None, p_type=None, user_id=None, project_id=None, name=None, fields=list(),
                   status=None, group_by=list(), start_time=None, end_time=None, order_by=list(), join='LEFT'):
        where = []
        param = dict()
        if s_type is not None:
            where.append("s.type=%(s_type)s")
            param['s_type'] = s_type
        if p_type is not None:
            where.append("p.type=%(p_type)s")
            param['p_type'] = p_type
        if user_id is not None:
            where.append("s.userId=%(userId)s")
            param['userId'] = user_id
        if project_id is not None:
            where.append("s.projectId=%(projectId)s")
            param['projectId'] = project_id
        if name is not None:
            where.append("s.name=%(name)s")
            param['name'] = name
        if status is not None:
            where.append("s.status=%(status)s")
            where.append("p.status=%(status)s")
            param['status'] = status
        if start_time and end_time:
            where.append("s.createTime BETWEEN '{} 00:00:00' AND '{} 23:59:59'".format(start_time, end_time))
        if where:
            if fields:
                sql = "SELECT {} FROM t_statistics s {} JOIN t_projects p ON p.id=s.projectId LEFT JOIN t_users u on u.id=s.userId WHERE {}".format(', '.join(fields), join, ' AND '.join(where))
            else:
                sql = "SELECT p.id pid, p.`name` projectName,s.id sid, s.type,s.`name`, s.createTime, u.id uid, u.realname, count(s.id) count FROM t_statistics s {} JOIN t_projects p ON p.id=s.projectId LEFT JOIN t_users u on u.id=s.userId WHERE {}".format(join, ' AND '.join(where))
            if group_by:
                sql += ' GROUP BY {}'.format(','.join(group_by))
            if order_by:
                sql += ' ORDER BY {}'.format(','.join(order_by))
            try:
                cursor = yield pool.execute(sql, param)
                result = cursor.fetchall()
                cursor.close()
                return munchify(result)
            except pymysql.Error as e:
                log.error(e)
                return []
        else:
            log.error('参数不对, 数据统计失败')
            return []

    # 自定义数据统计
    @gen.coroutine
    def custom_statistics(self, sql=''):
        if sql:
            try:
                cursor = yield pool.execute(sql)
                result = cursor.fetchall()
                cursor.close()
                return munchify(result)
            except pymysql.Error as e:
                log.error(e)
                return []
        else:
            log.error('参数不对, 数据统计失败')
            return []
