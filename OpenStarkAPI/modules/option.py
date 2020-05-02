from settings import pool
from tornado.log import app_log as log
from tornado import gen
from munch import munchify
import pymysql
import json


class OptionModule(object):
    """
    系统配置表相关操作
    """
    # 新增系统配置
    @gen.coroutine
    def add_option(self, o_type, name, value):
        if o_type in ['teams', 'cate']:
            options = yield self.get_options_list(o_type=o_type, name=name)
            option = []
            for op in options:
                if json.loads(op.value) == value:
                    option.append(op)
                    break
        else:
            option = yield self.get_option(o_type=o_type, name=name)
        if not option:
            sql = "INSERT INTO t_options (`type`, `name`, `value`) VALUE (%(type)s, %(name)s, %(value)s)"
            with (yield pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    try:
                        yield cursor.execute(sql, dict(type=o_type, name=name,
                                             value=json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else value))
                    except pymysql.Error as e:
                        yield conn.rollback()
                        log.error('添加系统配置失败#{}'.format(e))
                        flag, msg = False, '添加系统配置失败#{}'.format(e)
                    else:
                        yield conn.commit()
                        log.info('添加系统配置 {} 成功'.format(value))
                        flag, msg = cursor.lastrowid, '添加系统配置 {} 成功'.format(value)
        else:
            log.error('配置 {} 已存在'.format(value))
            flag, msg = False, '配置 {} 已存在'.format(value)
        return flag, msg

    # 删除系统配置
    @gen.coroutine
    def delete_option(self, o_type=None, name=None, value=None, oid=None, status=None):
        where = []
        param = dict()
        if o_type is not None:
            where.append("type=%(type)s")
            param['type'] = o_type
        if name is not None:
            where.append("name=%(name)s")
            param['name'] = name
        if value is not None:
            where.append("value=%(value)s")
            param['value'] = value
        if oid is not None:
            where.append("id=%(oid)s")
            param['oid'] = oid
        if status is not None:
            where.append("status=%(status)s")
            param['status'] = status
        if where:
            sql = "DELETE FROM t_options WHERE {}".format(' AND '.join(where))
            tx = yield pool.begin()
            try:
                yield tx.execute(sql, param)
            except pymysql.Error as e:
                yield tx.rollback()
                log.error('删除系统配置失败#{}'.format(e))
                flag, msg = False, '删除系统配置失败#{}'.format(e)
            else:
                yield tx.commit()
                log.info('删除系统配置成功')
                flag, msg = True, '删除系统配置成功'
        else:
            log.error('没有指定系统配置, 删除失败')
            flag, msg = False, '没有指定系统配置, 删除失败'
        return flag, msg

    # 编辑系统配置
    @gen.coroutine
    def edit_option(self, value=None, o_type=None, name=None, oid=None, status=None):
        where = []
        update = []
        param = dict()
        if value is not None:
            update.append("o.value=%(value)s")
            if isinstance(value, dict):
                param['value'] = json.dumps(value, ensure_ascii=False)
            else:
                param['value'] = value
        if o_type is not None:
            where.append("o.type=%(type)s")
            param['type'] = o_type
        if name is not None and oid is None:
            where.append("o.name=%(name)s")
            param['name'] = name
        if name is not None and oid is not None:
            update.append("o.name=%(name)s")
            param['name'] = name
        if oid is not None:
            where.append("o.id=%(oid)s")
            param['oid'] = oid
        if status is not None and value is None:
            update.append("o.status=%(status)s")
            param['status'] = status
        elif status is not None and value is not None:
            where.append("o.status=%(status)s")
            param['status'] = status
        option = yield self.get_option(o_type=o_type, name=name, oid=oid, status=status)
        if where and update and option:
            name = option.name
            o_type = option.type
            oid = option.id
            options = []
            if o_type == 'teams':
                option = yield self.get_options_list(o_type=o_type, name=name, status=status)
                for op in option:
                    if value and json.loads(op.value) == value:
                        options.append(op)
                        oid = op.id
            if (o_type == 'teams' and not options) or (o_type != 'teams' and option):
                sql = "UPDATE t_options o SET {} WHERE {}".format(','.join(update), ' AND '.join(where))
                tx = yield pool.begin()
                try:
                    yield tx.execute(sql, param)
                except pymysql.Error as e:
                    yield tx.rollback()
                    log.error('系统配置 {} 编辑失败#{}'.format(name, e))
                    flag, msg = False, '系统配置 {} 编辑失败#{}'.format(name, e)
                else:
                    yield tx.commit()
                    log.info('系统配置 {} 编辑成功'.format(name))
                    flag, msg = True, '系统配置 {} 编辑成功'.format(name)
            else:
                log.error('配置 {} 已存在'.format(value))
                flag, msg = oid, '配置 {} 已存在'.format(value)
        else:
            log.error('没有可编辑的系统配置')
            flag, msg = False, '没有可编辑的系统配置'
        return flag, msg

    # 获取系统配置
    @gen.coroutine
    def get_option(self, o_type=None, name=None, oid=None, status=None):
        where = []
        param = dict()
        if o_type is not None:
            where.append("o.type=%(type)s")
            param['type'] = o_type
        if name is not None and oid is None:
            where.append("o.name=%(name)s")
            param['name'] = name
        if oid is not None:
            where.append("o.id=%(oid)s")
            param['oid'] = oid
        if status is not None:
            where.append("o.status=%(status)s")
            param['status'] = status
        if where:
            try:
                sql = "SELECT * FROM t_options o WHERE {}".format(' AND '.join(where))
                cursor = yield pool.execute(sql, param)
                result = cursor.fetchone()
                cursor.close()
                return munchify(result)
            except pymysql.Error as e:
                log.error(e)
                return None
        else:
            log.error('参数不对, 获取系统配置失败')
            return None

    # 获取所有系统配置
    @gen.coroutine
    def get_options_list(self, o_type=None, name=None, status=None):
        where = []
        param = dict()
        if o_type is not None:
            where.append("o.type=%(type)s")
            param['type'] = o_type
        if name is not None:
            where.append("o.name=%(name)s")
            param['name'] = name
        if status is not None:
            where.append("o.status=%(status)s")
            param['status'] = status
        try:
            if where:
                sql = "SELECT * FROM t_options o WHERE {}".format(' AND '.join(where))
                cursor = yield pool.execute(sql, param)
            else:
                sql = "SELECT * FROM t_options"
                cursor = yield pool.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return munchify(result)
        except pymysql.Error as e:
            log.error(e)
            return []
