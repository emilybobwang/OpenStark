from settings import pool
from munch import munchify
from tornado import gen
from tornado.log import app_log as log
import pymysql
import json
import time


class ProjectModule(object):
    """
    项目表相关操作
    """
    # 添加项目
    @gen.coroutine
    def add_project(self, name, p_type, value=None, status=None, create_time=None):
        pj = yield self.get_project(name=name, p_type=p_type)
        if not pj:
            sql = "INSERT INTO t_projects (`name`, `type`, `value`, `status`, `createTime`) VALUE (%(name)s, %(type)s, %(value)s, %(status)s, %(createTime)s)"
            with (yield pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    try:
                        yield cursor.execute(sql, dict(name=name, type=p_type, status=status or 1,
                                                       value=json.dumps(value, ensure_ascii=False) if value else '{}',
                                                       createTime=create_time or time.strftime('%Y-%m-%d %H:%M:%S')))
                    except pymysql.Error as e:
                        yield conn.rollback()
                        log.error('添加项目失败#{}'.format(e))
                        flag, msg = False, '添加项目失败#{}'.format(e)
                    else:
                        yield conn.commit()
                        log.info('添加项目成功')
                        flag, msg = cursor.lastrowid, '添加项目成功'
            return flag, msg
        else:
            log.error('项目 {} 已存在'.format(name))
            return False, '项目 {} 已存在'.format(name)

    # 删除项目
    @gen.coroutine
    def delete_project(self, name=None, p_type=None, pid=None, status=None):
        pj = yield self.get_project(name=name, pid=pid, p_type=p_type)
        if pj:
            sql = "DELETE FROM t_projects"
            where = []
            param = dict()
            if name is not None:
                where.append("name=%(name)s")
                param['name'] = name
            if p_type is not None:
                where.append("type=%(type)s")
                param['type'] = p_type
            if pid is not None:
                if isinstance(pid, list):
                    pid = ','.join([str(p) for p in pid])
                where.append("id IN ({})".format(pid))
            if status is not None:
                where.append("status=%(status)s")
                param['status'] = status
            if where:
                sql += ' WHERE {}'.format(' AND '.join(where))
                tx = yield pool.begin()
                try:
                    yield tx.execute(sql, param)
                except Exception as e:
                    yield tx.rollback()
                    log.error('删除项目 {} 失败#{}'.format(pj.name, e))
                    flag, msg = False, '删除项目 {} 失败#{}'.format(pj.name, e)
                else:
                    yield tx.commit()
                    log.info('删除项目 {} 成功'.format(pj.name))
                    flag, msg = True, '删除项目 {} 成功'.format(pj.name)
            else:
                flag, msg = False, '请指定删除项目条件, 不能删除所有项目'
        else:
            log.error('没有指定删除的项目')
            flag, msg = False, '没有指定删除的项目'
        return flag, msg

    # 编辑项目
    @gen.coroutine
    def edit_project(self, pid, p_type=None, name=None, value=None, status=None, create_time=None):
        update = []
        param = dict(pid=pid)
        if name is not None:
            update.append("p.name=%(name)s")
            param['name'] = name
        if value is not None:
            update.append("p.value=%(value)s")
            param['value'] = json.dumps(value, ensure_ascii=False)
        if status is not None:
            update.append("p.status=%(status)s")
            param['status'] = status
        if create_time is not None:
            update.append("p.createTime=%(createTime)s")
            param['createTime'] = create_time
        pj = yield self.get_project(pid=pid, p_type=p_type)
        if update and pj:
            sql = 'UPDATE t_projects p SET {} WHERE p.id=%(pid)s'.format(', '.join(update))
            tx = yield pool.begin()
            try:
                yield tx.execute(sql, param)
            except pymysql.Error as e:
                log.error('项目 {} 编辑失败#{}'.format(pj.name, e))
                yield tx.rollback()
                flag, msg = False, '项目 {} 编辑失败#{}'.format(pj.name, e)
            else:
                yield tx.commit()
                log.info('项目 {} 编辑成功'.format(pj.name))
                flag, msg = True, '项目 {} 编辑成功'.format(pj.name)
            return flag, msg
        else:
            log.error('所编辑项目不存在')
            return False, '所编辑项目不存在'

    # 获取项目
    @gen.coroutine
    def get_project(self, name=None, pid=None, p_type=None, status=None):
        where = []
        param = dict()
        if status is not None:
            where.append("p.status=%(status)s")
            param['status'] = status
        if name is not None:
            where.append("p.name=%(name)s")
            param['name'] = name
        if p_type is not None:
            where.append("p.type=%(type)s")
            param['type'] = p_type
        if pid is not None:
            if isinstance(pid, list):
                pid = ','.join([str(p) for p in pid])
            where.append("p.id IN ({})".format(pid))
        sql = 'SELECT * FROM t_projects p'
        if where:
            try:
                sql += ' WHERE {}'.format(' AND '.join(where))
                cursor = yield pool.execute(sql, param)
                result = cursor.fetchone()
                cursor.close()
                return munchify(result)
            except pymysql.Error as e:
                log.error(e)
                return None
        else:
            log.error('参数不对, 获取项目失败')
            return None

    # 获取项目列表
    @gen.coroutine
    def get_projects_list(self, page=1, limit=None, p_type=None, name=None,
                          status=None, search=None, start_time=None, end_time=None):
        sql = 'SELECT * FROM t_projects p'
        where = []
        param = dict()
        if p_type is not None:
            where.append("p.type=%(type)s")
            param['type'] = p_type
        if name is not None:
            where.append("p.name like %(name)s")
            param['name'] = '%{}%'.format(name)
        if status is not None:
            if isinstance(status, list):
                status = ','.join([str(s) for s in status])
            where.append("p.status IN ({})".format(status))
        if search is not None:
            where.append('(p.name LIKE %(search)s OR p.value LIKE %(search)s)')
            param['search'] = '%{}%'.format(search)
        if start_time is not None and end_time is not None:
            where.append('(p.createTime BETWEEN %(startTime)s AND %(endTime)s)')
            param['startTime'] = start_time
            param['endTime'] = end_time
        if where:
            sql += ' WHERE {}'.format(' AND '.join(where))
        sql += ' ORDER BY p.id DESC'
        if limit is not None:
            offset = (page - 1) * limit
            sql += ' LIMIT {},{}'.format(offset, limit)
        try:
            cursor = yield pool.execute(sql, param)
            result = cursor.fetchall()
            sql = 'SELECT COUNT(*) count FROM t_projects p'
            if where:
                sql += ' WHERE {}'.format(' AND '.join(where))
            cursor = yield pool.execute(sql, param)
            total = cursor.fetchone()
            cursor.close()
            return munchify(result), munchify(total).count
        except pymysql.Error as e:
            log.error(e)
            return [], 0
