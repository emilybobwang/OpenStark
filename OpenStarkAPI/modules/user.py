import time
from settings import pool
from functions.common import CommonFunction
from tornado.log import app_log as log
from tornado import gen
from munch import munchify
import pymysql
import json


class UserModule(object):
    """
    用户表相关操作
    """
    def __init__(self):
        self.common_func = CommonFunction()

    # 获取用户信息
    @gen.coroutine
    def get_user_info(self, email_or_username=None, uid=None, status=None):
        where = []
        params = dict()
        if uid is not None:
            where.append("u.id=%(uid)s")
            params['uid'] = uid
        if email_or_username is not None:
            where.append("(u.email=%(user)s OR u.username=%(user)s)")
            params['user'] = email_or_username
        if status is not None:
            where.append("u.status=%(status)s")
            params['status'] = status
        sql = "SELECT u.*, (SELECT COUNT(IF(m.`type` IN ('notice', 'message') AND m.`status` NOT IN (0, 2), m.`type`, NULL)) + COUNT(IF(m.`type` IN ('todo') AND m.`status` NOT IN (0, 5), m.`type`, NULL)) FROM t_messages m WHERE m.type <> 'active' AND m.userId=u.id AND m.`status` <> 0) as unreadCount FROM t_users u"
        if where:
            sql += ' WHERE {}'.format(' AND '.join(where))
        try:
            cursor = yield pool.execute(sql, params)
            result = cursor.fetchone()
            cursor.close()
            return munchify(result)
        except pymysql.Error as e:
            log.error(e)
            return None

    # 通过user_id获取用户信息
    @gen.coroutine
    def get_users_info_by_id(self, uid, status=None):
        if isinstance(uid, list):
            uid = ','.join([str(u) for u in uid])
        sql = 'SELECT * FROM t_users u WHERE u.id in ({})'.format(uid)
        param = dict()
        if status is not None:
            sql += ' AND status=%(status)s'
            param['status'] = status
        sql += ' ORDER BY u.role'
        try:
            cursor = yield pool.execute(sql, param)
            result = cursor.fetchall()
            cursor.close()
            return munchify(result)
        except pymysql.Error as e:
            log.error(e)
            return []

    # 获取用户列表
    @gen.coroutine
    def get_users_list(self, page=1, limit=None, status=None, name=None):
        sql = 'SELECT * FROM t_users u'
        sql_count = 'SELECT COUNT(*) count FROM t_users u'
        where = []
        params = dict()
        if name is not None:
            where.append("(u.realname like %(name)s OR u.username like %(name)s OR u.email like %(name)s OR u.profile like %(name)s)")
            params['name'] = '%{}%'.format(name)
        if status is not None:
            where.append("u.status=%(status)s")
            params['status'] = status
        if where:
            where = ' WHERE {}'.format(' AND '.join(where))
            sql += where
            sql_count += where
        sql += ' ORDER BY u.role'
        if limit is not None:
            offset = (page - 1) * limit
            sql += ' LIMIT {},{}'.format(offset, limit)
        try:
            cursor = yield pool.execute(sql, params)
            result = cursor.fetchall()
            cursor = yield pool.execute(sql_count, params)
            total = cursor.fetchone()
            cursor.close()
            return munchify(result), munchify(total).count
        except pymysql.Error as e:
            log.error(e)
            return [], 0

    # 注册用户
    @gen.coroutine
    def register_user(self, email, password, username=None, real_name=None, profile=None, role=1, status=1):
        register_time = time.strftime('%Y-%m-%d %H:%M:%S')
        password = self.common_func.encode_password(password)
        try:
            cursor = yield pool.execute('SELECT COUNT(*) count FROM t_users')
            total = munchify(cursor.fetchone())
            if total.count == 0:
                role = 0
                status = 2
        except pymysql.Error as e:
            log.error(e)
        username = username or '{}_{}'.format(email.split('@')[0], str(int(time.time()*1000)))
        sql = """
        INSERT INTO t_users (username, email, password, realname, profile, registerTime, lastLoginTime, role, status)
        VALUE(%(username)s, %(email)s, %(password)s, %(realname)s, %(profile)s, %(registerTime)s, %(lastLoginTime)s, %(role)s, %(status)s)
        """
        user = yield self.get_user_info(email_or_username=email)
        if not user:
            with (yield pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    try:
                        yield cursor.execute(sql, dict(
                            username=username, email=email, password=password, realname=real_name or '',
                            registerTime=register_time, lastLoginTime=register_time, profile=json.dumps(
                                profile, ensure_ascii=False) or '',
                            role=role, status=status))
                    except pymysql.Error as e:
                        yield conn.rollback()
                        log.error('注册用户 {} 失败#{}'.format(email, e))
                        flag, msg = False, '注册用户 {} 失败#{}'.format(email, e)
                    else:
                        yield conn.commit()
                        log.info('注册用户 {} 成功'.format(email))
                        flag, msg = munchify(dict(id=cursor.lastrowid, status=status, role=role)), '注册用户成功!'
        else:
            log.error('该邮箱已注册!')
            flag, msg = False, '该邮箱已注册!'
        return flag, msg

    # 编辑用户
    @gen.coroutine
    def edit_user(self, email=None, uid=None, password=None, username=None, real_name=None, last_login_time=None,
                  role=None, status=None, profile=None):
        user = yield self.get_user_info(email_or_username=None if uid else email, uid=uid)
        if user:
            update = []
            param = dict(email=email if email else user.email)
            if password is not None:
                update.append("password=%(password)s")
                param['password'] = self.common_func.encode_password(password)
            if username is not None:
                sql = "SELECT id, username FROM t_users u WHERE u.email != %(email)s AND u.username = %(username)s"
                param['username'] = username
                try:
                    cursor = yield pool.execute(sql, param)
                    user_info = cursor.fetchone()
                    if (user_info and uid and uid != user_info['id']) or (user_info and uid is None):
                        log.error('用户名 {} 已存在'.format(username))
                        return False, '用户名 {} 已存在'.format(username)
                    else:
                        update.append("username=%(username)s")
                except pymysql.Error as e:
                    log.error(e)
                    return False, '编辑用户失败#{}'.format(e)
            if email is not None and uid is not None:
                is_exist_user = yield self.get_user_info(email)
                if is_exist_user and is_exist_user.id != uid:
                    log.error('该邮箱 {} 已注册'.format(email))
                    return False, '该邮箱 {} 已注册'.format(email)
                else:
                    update.append("email=%(email)s")
            if real_name is not None:
                update.append("realname=%(realname)s")
                param['realname'] = real_name
            if last_login_time is not None:
                update.append("lastLoginTime=%(lastLoginTime)s")
                param['lastLoginTime'] = last_login_time
            if role is not None:
                update.append('role=%(role)s')
                param['role'] = role
            if profile is not None:
                update.append('profile=%(profile)s')
                param['profile'] = json.dumps(profile, ensure_ascii=False)
            if status is not None:
                update.append('status=%(status)s')
                param['status'] = status
            if update:
                if uid is not None:
                    param['uid'] = uid
                    sql = "UPDATE t_users SET {} WHERE id=%(uid)s".format(', '.join(update))
                else:
                    sql = "UPDATE t_users SET {} WHERE email=%(email)s".format(', '.join(update))
                tx = yield pool.begin()
                try:
                    yield tx.execute(sql, param)
                except pymysql.Error as e:
                    yield tx.rollback()
                    log.error('编辑用户失败#{}'.format(e))
                    flag, msg = False, '用户 {} 资料修改失败'.format(user.email)
                else:
                    yield tx.commit()
                    log.info('用户 {} 资料修改成功'.format(user.email))
                    flag, msg = True, '用户 {} 资料修改成功'.format(user.email)
                return flag, msg
            else:
                log.error('没有可更新的项')
                return False, '没有可更新的项'
        else:
            log.error('用户 {} 不存在!'.format(email))
            return False, '用户 {} 不存在!'.format(email)

    # 删除用户信息
    @gen.coroutine
    def delete_user(self, uid=None, username_or_email=None, status=None):
        user = yield self.get_user_info(uid=uid, email_or_username=username_or_email, status=status)
        if user:
            where = []
            params = dict()
            if uid is not None:
                where.append("id=%(uid)s")
                params['uid'] = uid
            if username_or_email is not None:
                where.append("(email=%(user)s OR username=%(user)s)")
                params['user'] = username_or_email
            if status is not None:
                where.append("status=%(status)s")
                params['status'] = status
            sql = 'DELETE FROM t_users'
            if where:
                sql += ' WHERE {}'.format(' AND '.join(where))
            tx = yield pool.begin()
            try:
                yield tx.execute(sql, params)
            except pymysql.Error as e:
                yield tx.rollback()
                log.error('删除用户失败#{}'.format(e))
                flag, msg = False, '删除用户失败'
            else:
                yield tx.commit()
                log.info('删除用户成功')
                flag, msg = True, '删除用户成功'
            return flag, msg
        else:
            log.error('用户不存在!')
            return False, '用户不存在!'
