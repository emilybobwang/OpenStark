from tornado import gen
from tornado.log import app_log as log
from munch import munchify
from settings import pool
import pymysql
import json
import time


class SettingModule(object):
    """
    设置表相关操作
    """
    # 添加配置项
    @gen.coroutine
    def add_setting(self, s_type, name, value, pid=None, project=None,
                    status=1, sort=1, create_time=None):
        if project is not None:
            pid = "SELECT p.id FROM t_projects p WHERE p.`name`='{}' and p.type='project'".format(project)
        if create_time is not None:
            time_param = ', `createTime`'
            time_value = ', %(createTime)s'
        else:
            time_param = ''
            time_value = ''
        sql = """INSERT INTO t_settings (`projectId`, `type`, `name`, `value`, `status`, `sort`{})
        VALUE (({}), %(s_type)s, %(name)s, %(value)s, %(status)s, %(sort)s{})""".format(time_param, pid, time_value)
        if pid:
            with (yield pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    try:
                        yield cursor.execute(sql, dict(s_type=s_type, name=name, status=status, createTime=create_time,
                                                       value=json.dumps(value, ensure_ascii=False), sort=sort))
                    except pymysql.Error as e:
                        yield conn.rollback()
                        log.error('新增 {} 设置项 {} 失败#{}'.format(s_type, name, e))
                        flag, msg = False, '新增 {} 设置项 {} 失败#{}'.format(s_type, name, e)
                    else:
                        yield conn.commit()
                        log.info('新增 {} 设置项 {} 成功'.format(s_type, name))
                        flag, msg = cursor.lastrowid, '新增 {} 设置项 {} 成功'.format(s_type, name)
        else:
            flag = False
            msg = '新增 {} 设置项 {} 失败#pid不能为空'.format(s_type, name)
        return flag, msg

    # 删除配置项
    @gen.coroutine
    def delete_setting(self, sid):
        setting = yield self.get_settings_by_id(sid=sid)
        if isinstance(sid, list):
            sid = ','.join([str(s) for s in sid])
        if setting and sid:
            sql = 'DELETE FROM t_settings WHERE id in ({})'.format(sid)
            tx = yield pool.begin()
            try:
                yield tx.execute(sql)
            except pymysql.Error as e:
                yield tx.rollback()
                log.error('删除 {} 设置项 {} 失败#{}'.format(setting[0].type, [x.name for x in setting], e))
                flag, msg = False, '删除 {} 设置项 {} 失败#{}'.format(setting[0].type, [x.name for x in setting], e)
            else:
                yield tx.commit()
                log.info('删除 {} 设置项 {} 成功'.format(setting[0].type, [x.name for x in setting]))
                flag, msg = True, '删除 {} 设置项 {} 成功'.format(setting[0].type, [x.name for x in setting])
        else:
            flag, msg = False, '不存在指定的设置项'
        return flag, msg

    # 按类型批量删除配置项
    @gen.coroutine
    def delete_settings_by_type(self, s_type, name=None, status=None):
        setting = yield self.get_settings_list(s_type=s_type, status=status, name=name)
        if setting:
            where = []
            param = dict(s_type=s_type)
            if status is not None:
                where.append('status=%(status)s')
                param['status'] = status
            elif name is not None:
                where.append('name=%(name)s')
                param['name'] = name
            sql = 'DELETE FROM t_settings WHERE type=%(s_type)s'
            if where:
                sql += ' AND {}'.format(' AND '.join(where))
            tx = yield pool.begin()
            try:
                yield tx.execute(sql, param)
            except pymysql.Error as e:
                yield tx.rollback()
                log.error('批量删除设置项 {} 失败#{}'.format(s_type, e))
                flag, msg = False, '批量删除设置项 {} 失败#{}'.format(s_type, e)
            else:
                yield tx.commit()
                log.info('批量删除设置项 {} 成功'.format(s_type))
                flag, msg = True, '批量删除设置项 {} 成功'.format(s_type)
        else:
            flag, msg = False, '不存在指定的设置项'
        return flag, msg

    # 编辑配置项
    @gen.coroutine
    def edit_setting(self, sid, status=None, name=None, pid=None, project=None, value=None, sort=None, create_time=None):
        if project is not None:
            pid = "SELECT p.id FROM t_projects p WHERE p.`name`='{}' and p.type='project'".format(project)
        update = []
        param = dict(sid=sid)
        if status is not None:
            update.append('s.status=%(status)s')
            param['status'] = status
        if name is not None:
            update.append("s.name=%(name)s")
            param['name'] = name
        if value is not None:
            update.append("s.value=%(value)s")
            param['value'] = json.dumps(value, ensure_ascii=False)
        if pid is not None:
            update.append("s.projectId=(%(pid)s)")
            param['pid'] = pid
        if sort is not None:
            update.append('s.sort=%(sort)s')
            param['sort'] = sort
        if create_time is not None:
            update.append('s.createTime=%(createTime)s')
            param['createTime'] = create_time
        setting = yield self.get_settings_by_id(sid=sid)
        if update and setting:
            sql = 'UPDATE t_settings s SET {} WHERE id=%(sid)s'.format(', '.join(update))
            tx = yield pool.begin()
            try:
                yield tx.execute(sql, param)
            except pymysql.Error as e:
                yield tx.rollback()
                log.error('更新 {} 配置项 {} 失败#{}'.format(setting[0].type, [x.name for x in setting], e))
                flag, msg = False, '更新 {} 配置项 {} 失败#{}'.format(setting[0].type, [x.name for x in setting], e)
            else:
                yield tx.commit()
                log.info('更新 {} 配置项 {} 成功'.format(setting[0].type, [x.name for x in setting]))
                flag, msg = True, '更新 {} 配置项 {} 成功'.format(setting[0].type, [x.name for x in setting])
            return flag, msg
        else:
            log.error('没有指定编辑的配置项')
            return False, '没有指定编辑的配置项'

    # 通过条件获取配置项
    @gen.coroutine
    def get_setting(self, pid=None, name=None, s_type=None, project=None,
                    status=None, pj_status=None, team_id=None, create_time=None):
        sql = """
            SELECT s.id, s.projectId project_id, s.type, s.name, s.value, s.status, p.name project_name, p.teamId team_id, s.sort, s.createTime, o.value team
            FROM t_settings s JOIN t_projects p ON s.projectId=p.id LEFT JOIN t_options o ON o.id=p.teamId
            """
        where = []
        param = dict()
        if pid is not None:
            if isinstance(pid, list):
                pid = ','.join([str(p) for p in pid])
            where.append('s.projectId IN ({})'.format(pid))
        if project is not None:
            where.append("p.type='project' AND p.name=%(project)s")
            param['project'] = project
        if name is not None:
            where.append("s.name=%(name)s")
            param['name'] = name
        if create_time is not None:
            where.append('s.createTime LIKE %(createTime)s')
            param['createTime'] = '%{}%'.format(create_time)
        if s_type is not None:
            if isinstance(s_type, list):
                s_type = ', '.join(["'{}'".format(t) for t in s_type])
            else:
                s_type = "'{}'".format(s_type)
            where.append('s.type IN ({})'.format(s_type))
        if status is not None:
            if isinstance(status, list):
                status = ','.join([str(s) for s in status])
            where.append('s.status IN ({})'.format(status))
        if team_id is not None:
            if isinstance(team_id, list):
                team_id = ','.join([str(t) for t in team_id])
            where.append('p.teamId IN ({})'.format(team_id))
        if pj_status is not None:
            where.append('p.status=%(pj_status)s')
            param['pj_status'] = pj_status
        if where:
            sql += ' WHERE {}'.format(' AND '.join(where))
        try:
            cursor = yield pool.execute(sql, param)
            result = cursor.fetchone()
            cursor.close()
            return munchify(result)
        except pymysql.Error as e:
            log.error(e)
            return None

    # 通过条件获取配置项列表
    @gen.coroutine
    def get_settings_list(self, pid=None, name=None, s_type=None, order_by=list(), project=None, sort=None,
                          status=None, pj_status=None, page=1, limit=None, search=None, team_id=None):
        sql = """
            SELECT s.id, s.projectId project_id, s.type, s.name, s.value, s.status, p.name project_name, p.teamId team_id, s.sort, s.createTime, o.value team
            FROM t_settings s JOIN t_projects p ON s.projectId=p.id LEFT JOIN t_options o ON o.id=p.teamId
            """
        sql_count = 'SELECT COUNT(*) count FROM t_settings s JOIN t_projects p ON s.projectId=p.id LEFT JOIN t_options o ON o.id=p.teamId'
        where = []
        param = dict()
        if pid is not None:
            if isinstance(pid, list):
                pid = ','.join([str(p) for p in pid])
            where.append('s.projectId IN ({})'.format(pid))
        if project is not None:
            where.append("p.type='project' AND p.name=%(project)s")
            param['project'] = project
        if name is not None:
            where.append("s.name=%(name)s")
            param['name'] = name
        if s_type is not None:
            if isinstance(s_type, list):
                s_type = ', '.join(["'{}'".format(t) for t in s_type])
            else:
                s_type = "'{}'".format(s_type)
            where.append('s.type IN ({})'.format(s_type))
        if status is not None:
            if isinstance(status, list):
                status = ','.join([str(s) for s in status])
            where.append('s.status IN ({})'.format(status))
        if sort is not None:
            if isinstance(sort, list):
                sort = ','.join([str(s) for s in sort])
            where.append('s.sort IN ({})'.format(sort))
        if team_id is not None:
            if isinstance(team_id, list):
                team_id = ','.join([str(t) for t in team_id])
            where.append('p.teamId IN ({})'.format(team_id))
        if pj_status is not None:
            where.append('p.status=%(pj_status)s')
            param['pj_status'] = pj_status
        if search is not None:
            where.append('(s.name LIKE %(search)s OR s.value LIKE %(search)s)')
            param['search'] = '%{}%'.format(search)
        if where:
            sql += ' WHERE {}'.format(' AND '.join(where))
            sql_count += ' WHERE {}'.format(' AND '.join(where))
        if order_by:
            sql += ' ORDER BY {}'.format(','.join(order_by))
        if limit is not None:
            offset = (page - 1) * limit
            sql += ' LIMIT {},{}'.format(offset, limit)
        try:
            cursor = yield pool.execute(sql, param)
            result = cursor.fetchall()
            cursor = yield pool.execute(sql_count, param)
            total = cursor.fetchone()
            cursor.close()
            return munchify(result), munchify(total).count
        except pymysql.Error as e:
            log.error(e)
            return [], 0

    # 通过id获取配置项
    @gen.coroutine
    def get_settings_by_id(self, sid, order_by=list()):
        if isinstance(sid, list):
            sid = ','.join([str(s) for s in sid])
        if sid:
            sql = """
                SELECT s.id, s.projectId project_id, s.type, s.name, s.value, s.status, p.name project_name, p.teamId team_id, s.sort, s.createTime, o.value team
                FROM t_settings s JOIN t_projects p ON s.projectId=p.id LEFT JOIN t_options o ON o.id=p.teamId WHERE s.id IN ({})
                """.format(sid)
            if order_by:
                sql += ' ORDER BY {}'.format(','.join(order_by))
            try:
                cursor = yield pool.execute(sql)
                result = cursor.fetchall()
                cursor.close()
                return munchify(result)
            except pymysql.Error as e:
                log.error(e)
                return []
        else:
            return []
