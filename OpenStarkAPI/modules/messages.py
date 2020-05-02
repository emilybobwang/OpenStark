from settings import pool
from tornado.log import app_log as log
from tornado import gen
from munch import munchify
import pymysql
import time
import json


class MessagesModule(object):
    """
    动态消息表相关操作
    """
    # 新增动态消息
    @gen.coroutine
    def add_message(self, user_id, m_type, content, status=1):
        sql = "INSERT INTO t_messages (`userId`, `type`, `content`, `status`) VALUE (%(userId)s, %(type)s, %(content)s, %(status)s)"
        with (yield pool.Connection()) as conn:
            with conn.cursor() as cursor:
                try:
                    yield cursor.execute(sql, dict(userId=user_id, type=m_type, content=json.dumps(
                        content, ensure_ascii=False), status=status))
                except pymysql.Error as e:
                    yield conn.rollback()
                    log.error('新增动态消息失败#{}'.format(e))
                    flag, msg = False, '新增动态消息失败#{}'.format(e)
                else:
                    yield conn.commit()
                    log.info('新增动态消息成功')
                    flag, msg = cursor.lastrowid, '新增动态消息成功'
        return flag, msg

    # 删除动态消息
    @gen.coroutine
    def delete_message(self, m_type=None, user_id=None, mid=None):
        where = []
        param = dict()
        if m_type is not None:
            where.append("type=%(type)s")
            param['type'] = m_type
        if user_id is not None:
            where.append("userId=%(userId)s")
            param['userId'] = user_id
        if mid is not None:
            where.append("id=%(mid)s")
            param['mid'] = mid
        if where:
            sql = "DELETE FROM t_messages WHERE {}".format(' AND '.join(where))
            tx = yield pool.begin()
            try:
                yield tx.execute(sql, param)
            except pymysql.Error as e:
                yield tx.rollback()
                log.error('删除动态消息失败#{}'.format(e))
                flag, msg = False, '删除动态消息失败#{}'.format(e)
            else:
                yield tx.commit()
                log.info('删除动态消息成功')
                flag, msg = True, '删除动态消息成功'
        else:
            log.error('没有指定动态消息, 删除失败')
            flag, msg = False, '没有指定动态消息, 删除失败'
        return flag, msg

    # 编辑动态消息
    @gen.coroutine
    def edit_message(self, m_type=None, user_id=None, mid=None, content=None, status=None):
        where = []
        update = ["m.updateTime=%(updateTime)s"]
        param = dict(updateTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        if m_type is not None:
            where.append("m.type=%(type)s")
            param['type'] = m_type
        if mid is not None:
            where.append("m.id=%(mid)s")
            param['mid'] = mid
        if user_id is not None:
            where.append("m.userId=%(userId)s")
            param['userId'] = user_id
        if status is not None and content is None:
            update.append("m.status=%(status)s")
            param['status'] = status
        elif content is not None and status is None:
            update.append("m.content=%(content)s")
            param['content'] = json.dumps(content, ensure_ascii=False)
        elif status is not None and content is not None:
            where.append("m.status=%(status)s")
            update.append("m.content=%(content)s")
            param['status'] = status
            param['content'] = json.dumps(content, ensure_ascii=False)
        message = yield self.get_message(m_type=m_type, user_id=user_id, mid=mid)
        if where and message:
            sql = "UPDATE t_messages m SET {} WHERE {}".format(', '.join(update), ' AND '.join(where))
            tx = yield pool.begin()
            try:
                yield tx.execute(sql, param)
            except pymysql.Error as e:
                yield tx.rollback()
                log.error('动态消息 #{} 编辑失败#{}'.format(message.id, e))
                flag, msg = False, '动态消息 #{} 编辑失败#{}'.format(message.id, e)
            else:
                yield tx.commit()
                log.info('动态消息 #{} 编辑成功'.format(message.id))
                flag, msg = True, '动态消息 #{} 编辑成功'.format(message.id)
        else:
            log.error('没有可编辑的动态消息')
            flag, msg = False, '没有可编辑的动态消息'
        return flag, msg

    # 获取动态消息
    @gen.coroutine
    def get_message(self, m_type=None, user_id=None, mid=None, status=None):
        where = []
        param = dict()
        if m_type is not None:
            where.append("m.type=%(type)s")
            param['type'] = m_type
        if user_id is not None:
            where.append("m.userId=%(userId)s")
            param['userId'] = user_id
        if mid is not None:
            where.append("m.id=%(mid)s")
            param['mid'] = mid
        if status is not None:
            where.append("m.status=%(status)s")
            param['status'] = status
        if where:
            try:
                sql = "SELECT m.*,u.username,u.realname,u.email,u.`profile`,u.role,u.`status` as userStatus,u.registerTime FROM t_messages m JOIN t_users u on u.id=m.userId WHERE {}".format(' AND '.join(where))
                cursor = yield pool.execute(sql, param)
                result = cursor.fetchone()
                cursor.close()
                return munchify(result)
            except pymysql.Error as e:
                log.error(e)
                return None
        else:
            log.error('参数不对, 获取动态消息失败')
            return None

    # 获取所有动态消息
    @gen.coroutine
    def get_messages_list(self, m_type=None, user_id=None, status=None, offset=0, limit=5):
        where = []
        param = dict(offset=offset, limit=limit)
        if m_type is not None:
            if isinstance(m_type, list):
                m_type = ', '.join(["'{}'".format(t) for t in m_type])
            else:
                m_type = "'{}'".format(m_type)
            where.append('m.type IN ({})'.format(m_type))
        if user_id is not None:
            where.append("m.userId=%(userId)s")
            param['userId'] = user_id
        if status is not None:
            if isinstance(status, list):
                status = ','.join([str(s) for s in status])
            where.append('m.status IN ({})'.format(status))
        try:
            if where:
                sql = "SELECT m.*,u.username,u.realname,u.email,u.`profile`,u.role,u.`status` as userStatus,u.registerTime FROM t_messages m JOIN t_users u on u.id=m.userId WHERE {} ORDER BY m.createTime DESC LIMIT %(offset)s,%(limit)s".format(' AND '.join(where))
                cursor = yield pool.execute(sql, param)
            else:
                sql = "SELECT m.*,u.username,u.realname,u.email,u.`profile`,u.role,u.`status` as userStatus,u.registerTime FROM t_messages m JOIN t_users u on u.id=m.userId ORDER BY m.createTime DESC LIMIT %(offset)s,%(limit)s"
                cursor = yield pool.execute(sql)
            result = cursor.fetchall()
            cursor = yield pool.execute('SELECT COUNT(*) count FROM t_messages')
            total = cursor.fetchone()
            cursor.close()
            return munchify(result), munchify(total).count
        except pymysql.Error as e:
            log.error(e)
            return [], 0
