from handlers.common import BaseHandler, authenticated_async
from tornado import gen
from tornado.web import app_log as log
from handlers.common import AddLogs
from modules.testing import TestingModule
from settings import host_160, port_160, user_160, password_160, root_160
from git import Repo
import json
import os
import time
import uuid
import shutil


"""
工具相关接口
"""

class RunShellHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op=None):
        if op == 'list':
            sid = self.get_argument('id', None)
            if sid:
                data = dict(id=sid, shell='', type=[])
                file = os.path.join(self.settings.get('static_path'), 'files', 'shells', '{}.txt'.format(sid))
                if os.path.isfile(file):
                    with open(file, 'r', encoding='utf8') as fp:
                        lines = fp.readlines()
                        if len(lines) >= 3:
                            shell_type = lines[1].strip()
                            shell = ''
                            for i in range(2, len(lines)):
                                shell += lines[i]
                            data['shell'] = shell
                            if shell_type == 'web':
                                data['type'] = ['4']
                            elif shell_type == 'os':
                                data['type'] = ['7', '8', '9']
                            else:
                                data['type'] = ['5']
            else:
                data = list()
                data.append(dict(id=0, title='自定义SHELL'))
                try:
                    path = os.path.join(self.settings.get('static_path'), 'files', 'shells')
                    if os.path.exists(path):
                        for f in os.listdir(path):
                            file = f.split('.', 1)
                            if len(file) == 2:
                                file_path = os.path.join(self.settings.get('static_path'), 'files', 'shells', f)
                                if file_path.endswith('txt'):
                                    with open(file_path, 'r', encoding='utf8') as fp:
                                        lines = fp.readlines()
                                        if len(lines) >= 3:
                                            title = lines[0].strip()
                                            data.append(dict(id=file[0], title=title))
                except Exception as e:
                    log.error(e)
            msg = dict(status='SUCCESS', message='', data=data)
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)

    @authenticated_async
    @gen.coroutine
    def post(self, op=None):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        if op == 'run':
            data = yield self.get_request_body_to_json()
            message = list()
            success = list()
            for ip in data.get('ip'):
                msg = '服务器信息配置不对, 请在环境管理中检查配置是否正确!'
                server = (yield self.option_func.get_env_info(eid=data.get('eid'), ip=ip))[0]
                if server and server.details:
                    res, msg = yield self.thread_func.exec_remote_shell(
                        host=server.details[0].get('ip'), port=server.details[0].get('port'),
                        username=server.details[0].get('username'), password=server.details[0].get('password'),
                        shell=data.get('shell'))
                    if res:
                        success.append(res)
                if msg not in message:
                    message.append(msg)
            msg = dict(status='FAIL' if len(success) != len(data.get('ip')) else 'SUCCESS', message=', '.join(message), data='')
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)


class RunSQLHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op=None):
        if op == 'list':
            sid = self.get_argument('id', None)
            if sid:
                data = dict(id=sid, sql='', dbName='', type='')
                file = os.path.join(self.settings.get('static_path'), 'files', 'SQLs', '{}.txt'.format(sid))
                if os.path.isfile(file):
                    with open(file, 'r', encoding='utf8') as fp:
                        lines = fp.readlines()
                        if len(lines) >= 3:
                            db_name = lines[1].strip()
                            sql = ''
                            for i in range(2, len(lines)):
                                sql += lines[i]
                            data['sql'] = sql
                            data['type'] = '6'
                            data['dbName'] = db_name
            else:
                data = list()
                data.append(dict(id=0, title='自定义SQL'))
                try:
                    path = os.path.join(self.settings.get('static_path'), 'files', 'SQLs')
                    if os.path.exists(path):
                        for f in os.listdir(path):
                            file = f.split('.', 1)
                            if len(file) == 2:
                                file_path = os.path.join(self.settings.get('static_path'), 'files', 'SQLs', f)
                                if file_path.endswith('txt'):
                                    with open(file_path, 'r', encoding='utf8') as fp:
                                        lines = fp.readlines()
                                        if len(lines) >= 3:
                                            title = lines[0].strip()
                                            data.append(dict(id=file[0], title=title))
                except Exception as e:
                    log.error(e)
            msg = dict(status='SUCCESS', message='', data=data)
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)

    @authenticated_async
    @gen.coroutine
    def post(self, op=None):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        if op == 'run':
            data = yield self.get_request_body_to_json()
            server = (yield self.option_func.get_env_info(eid=data.get('eid'), ip=data.get('ip'), mark=data.get('db')))[0]
            if server and server.details:
                server = server.details[0]
                run_sql = TestingModule(engine='mysql', host=server.get('ip'), user=server.get('username'),
                                        password=server.get('password'), database=data.get('db'),
                                        sql=data.get('sql') or '', port=server.get('port'))
                res, msg = yield run_sql.run_some_sql()
                if res:
                    if isinstance(msg, list):
                        msg = [['{},'.format(t) for t in m] for m in msg]
                    msg = dict(status='SUCCESS', message=msg, data='')
                else:
                    msg = dict(status='FAIL', message=msg, data='')
            else:
                msg = dict(status='FAIL', message='服务器信息配置不对, 请在环境管理中检查配置是否正确!', data='')
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)


# 工具管理
class ToolsHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op=None):
        if op == 'list':
            AddLogs().add_logs(ip=self.request.remote_ip)
            name = self.get_argument('name', '')
            page = int(self.get_argument('page', 1))
            size = int(self.get_argument('size', 10))
            tools, total = yield self.project.get_projects_list(p_type='tool', page=page, limit=size, name=name or None)
            data = []
            no = 0
            for tool in tools:
                info = json.loads(tool.config) if tool.config else dict(description='', link='')
                no += 1
                data.append(dict(key=no+page*size-size, name=tool.name, tid=tool.id, status=tool.status,
                                 description=info.get('description'), link=info.get('link'), userId=info.get('userId')))
            msg = dict(status='SUCCESS', message='', data=dict(data=data, page=page, size=size, total=total))
        elif op == 'menu':
            tools, total = yield self.project.get_projects_list(p_type='tool', status=1)
            data = list()
            for tool in tools:
                info = json.loads(tool.config) if tool.config else dict(description='', link='')
                if tool.id in [34] or info.get('link').strip() == '':
                    continue
                data.append(dict(id=str(tool.id), title=tool.name, url=info.get('link').strip(),
                                 description=info.get('description').strip()))
            msg = dict(status='SUCCESS', message='', data=data)
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)

    @authenticated_async
    @gen.coroutine
    def post(self, op='edit'):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        data = yield self.get_request_body_to_json()
        if data.name.strip() == '':
            return self.write_json(msg=dict(status='FAIL', message='工具名称不能为空', data=''))
        if op == 'edit':
            if str(data.key).find('NEW_TEMP_ID') != -1 and data.tid == '':
                tid, msg = yield self.project.add_project(name=data.name.strip(), p_type='tool', status=data.status,
                                                          config=dict(description=data.description, link=data.link,
                                                                      userId=self.current_user.id))
                if tid:
                    msg = dict(status='SUCCESS', message='新增成功', data=dict(tid=tid))
                else:
                    msg = dict(status='FAIL', message=msg, data='')
            else:
                res, msg = yield self.project.edit_project(pid=data.tid, name=data.name.strip(), status=data.status,
                                                           config=dict(description=data.description, link=data.link,
                                                                       userId=data.userId))
                if res:
                    msg = dict(status='SUCCESS', message='编辑成功', data=dict(tid=data.tid))
                else:
                    msg = dict(status='FAIL', message=msg, data='')
        elif op == 'delete':
            res, msg = yield self.project.delete_project(pid=data.tid)
            if res:
                yield self.statistics.delete_statistics(project_id=data.tid)
                msg = dict(status='SUCCESS', message='删除成功', data='')
            else:
                msg = dict(status='FAIL', message=msg, data='')
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)


# 同步数据库
class SyncDB(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op=None):
        AddLogs().add_logs(ip=self.request.remote_ip)
        if op == 'db':
            key = self.get_argument('key', None)
            date = self.get_argument('date', None)
            if date and key:
                detail_list, total = yield self.setting.get_settings_list(
                    s_type='env', name=key, status=1)
                dbs = list()
                for detail in detail_list:
                    desc = json.loads(detail.value)
                    if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                        continue
                    db_path = os.path.join(self.settings.get('static_path'), 'syncDB', date, desc.get('ip').strip())
                    if not os.path.isdir(db_path):
                        continue
                    sql_list = os.listdir(db_path)
                    for sql in sql_list:
                        if sql.find('backup') == -1:
                            continue
                        sql = sql.split('_', maxsplit=1)
                        if len(sql) > 1:
                            db = dict(id=sql[0], key=sql[0], title=sql[0], description=sql[0])
                            db not in dbs and dbs.append(db)
                msg = dict(status='SUCCESS', message='获取数据库成功', data=dict(dbList=dbs))
            elif key:
                detail_list, total = yield self.setting.get_settings_list(
                    s_type='env', name=key, status=1)
                db = list()
                for detail in detail_list:
                    desc = json.loads(detail.value)
                    if desc.get('type') == 'APPLICATION' and desc.get('title').upper().find('MYSQL') != -1:
                        for d in desc.get('description').split(','):
                            db.append(dict(id=d, key=d, title=d, description=d))
                msg = dict(status='SUCCESS', message='获取数据库成功', data=dict(dbList=db))
            else:
                msg = dict(status='FAIL', message='环境ID不能为空', data='')
        elif op == 'table':
            key = self.get_argument('key', None)
            if key:
                db_path = os.path.join(self.settings.get('static_path'), 'syncDB', 'lasTables')
                table = list()
                if os.path.isdir(db_path):
                    last_table_path = os.path.join(db_path, '{}.txt'.format(key))
                    if os.path.isfile(last_table_path):
                        with open(last_table_path, 'r', encoding='utf8') as fp:
                            for line in fp.readlines():
                                table.append(dict(id=line, key=line, title=line, description=line))
                msg = dict(status='SUCCESS', message='获取数据表成功', data=dict(tableList=table))
            else:
                msg = dict(status='FAIL', message='数据库ID不能为空', data='')
        elif op == 'init':
            db = self.get_argument('db', '')
            tb_list = list()
            init_path = os.path.join(self.settings.get('static_path'), 'syncDB', 'initSQL')
            db_file = os.path.join(init_path, '{}.txt'.format(db))
            if os.path.isfile(db_file):
                with open(db_file, 'r', encoding='utf8') as fp:
                    for f in fp.readlines():
                        tb_list.append(f.strip())
            msg = dict(status='SUCCESS', message='获取初始化数据表成功',
                       data=dict(initTable=tb_list))
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)

    @authenticated_async
    @gen.coroutine
    def post(self, op=None):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        if op == 'do':
            data = yield self.get_request_body_to_json()
            source_list, total = yield self.setting.get_settings_list(
                s_type='env', name=data.source.server.key, status=1)
            target_list, total = yield self.setting.get_settings_list(
                s_type='env', name=data.target.server.key, status=1)
            source_db_host = dict()
            target_db_host = dict()
            source_db = [db.key.strip() for db in data.source.dbs]
            if not source_db:
                for source in source_list:
                    desc = json.loads(source.value)
                    if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                        continue
                    for db in desc.get('description').split(','):
                        source_db.append(db)
            for source in source_list:
                desc = json.loads(source.value)
                if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                    continue
                for db in source_db:
                    if desc.get('description').find(db) == -1:
                        continue
                    if source.id not in source_db_host.keys():
                        source_db_host[source.id] = dict(
                            ip=desc.get('ip').strip(), port=desc.get('port').strip(), tables=[tb.key.strip() for tb in data.source.tables],
                            user=desc.get('user').strip(), password=desc.get('password').strip(), dbs=[db])
                    else:
                        source_db_host[source.id]['dbs'].append(db)
            for target in target_list:
                desc = json.loads(target.value)
                if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                    continue
                for db in source_db_host:
                    for key in source_db_host[db]['dbs']:
                        if desc.get('description').find(key) == -1:
                            continue
                        if target.id not in target_db_host.keys():
                            target_db_host[target.id] = dict(
                                ip=desc.get('ip').strip(), port=desc.get('port').strip(),
                                tables=source_db_host[db]['tables'], source=db, dbs=[key],
                                user=desc.get('user').strip(), password=desc.get('password').strip())
                        else:
                            target_db_host[target.id]['dbs'].append(key)
            db_path = os.path.join(self.settings.get('static_path'), 'syncDB', 'lasTables')
            init_path = os.path.join(self.settings.get('static_path'), 'syncDB', 'initSQL')
            init_data_path = os.path.join(self.settings.get('static_path'), 'syncDB', time.strftime('%Y%m%d'), 'data')
            if not os.path.isdir(db_path):
                os.makedirs(db_path)
            if not os.path.isdir(init_data_path):
                os.makedirs(init_data_path)
            init_sql = list()
            init_data_sql = dict()
            if os.path.isdir(init_path):
                for file in os.listdir(init_path):
                    file = file.split('.', maxsplit=1)
                    if len(file) > 1 and file[1] == 'txt':
                        init_data_sql[file[0]] = []
                        continue
                    file = file[0].split('_', maxsplit=1) if len(file) > 1 and file[1] == 'sql' else None
                    file = file[1] if file and len(file) > 1 else None
                    file and init_sql.append(file)
                for key in init_data_sql:
                    with open(os.path.join(init_path, '{}.txt'.format(key)), 'r', encoding='utf8') as fp:
                        init_data_sql[key] = [tb.strip() for tb in fp.readlines()]
            success_db = list()
            total_db = list()
            for key in target_db_host:
                for db in target_db_host[key]['dbs']:
                    total_db.append(db)
                    tables = target_db_host[key]['tables']
                    if os.path.isdir(db_path) and not tables:
                        last_table_path = os.path.join(db_path, '{}.txt'.format(db))
                        if os.path.isfile(last_table_path):
                            with open(last_table_path, 'r', encoding='utf8') as fp:
                                tables = fp.readlines()
                    tables = ' '.join([tb.strip() for tb in tables])
                    dump_path = os.path.join(self.settings.get('static_path'), 'syncDB', time.strftime('%Y%m%d'), target_db_host[key]['ip'])
                    if not os.path.isdir(dump_path):
                        os.makedirs(dump_path)
                    if tables.strip() and os.path.isdir(dump_path):
                        sql_file = '{}/{}.sql'.format(time.strftime('%Y%m%d'), db)
                        init_sql_file = '{}/data/{}.sql'.format(time.strftime('%Y%m%d'), db)
                        init_data = '''cd {}
                        /opt/lampp/bin/mysqldump -h{} -P{} -u{} -p{} --insert-ignore {} {} > {}'''.format(
                                root_160, source_db_host[target_db_host[key]['source']]['ip'], source_db_host[target_db_host[key]['source']]['port'],
                                source_db_host[target_db_host[key]['source']]['user'], source_db_host[target_db_host[key]['source']]['password'],
                                db, ' '.join(init_data_sql[db]), init_sql_file
                            ) if db in init_data_sql.keys() and init_data_sql[db] else ''
                        shell_dump = '''cd {}
                        /opt/lampp/bin/mysqldump -h{} -P{} -u{} -p{} -d {} {} > {}
                        {}'''.format(
                            root_160, source_db_host[target_db_host[key]['source']]['ip'], source_db_host[target_db_host[key]['source']]['port'],
                            source_db_host[target_db_host[key]['source']]['user'], source_db_host[target_db_host[key]['source']]['password'],
                            db, tables, sql_file, init_data
                        )
                        shell_backup = '''cd {}
                        /opt/lampp/bin/mysqldump -h{} -P{} -u{} -p{} -d {} > {}
                        {}'''.format(
                            root_160, target_db_host[key]['ip'], target_db_host[key]['port'], target_db_host[key]['user'],
                            target_db_host[key]['password'], db,
                            '{}/{}/{}_backup.sql'.format(time.strftime('%Y%m%d'), target_db_host[key]['ip'], db),
                            init_data
                        )
                        init_data = '/opt/lampp/bin/mysql -h{} -P{} -u{} -p{} -f {} < {}'.format(
                            target_db_host[key]['ip'], target_db_host[key]['port'], target_db_host[key]['user'],
                            target_db_host[key]['password'], db, 'initSQL/init_{}.sql'.format(db)
                        ) if db in init_sql else ''
                        import_data = '/opt/lampp/bin/mysql -h{} -P{} -u{} -p{} -f {} < {}'.format(
                            target_db_host[key]['ip'], target_db_host[key]['port'], target_db_host[key]['user'],
                            target_db_host[key]['password'], db, init_sql_file
                        ) if db in init_data_sql.keys() and init_data_sql[db] else ''
                        shell_import = '''cd {}
                        /opt/lampp/bin/mysql -h{} -P{} -u{} -p{} -f {} < {}
                        {}
                        {}'''.format(
                            root_160, target_db_host[key]['ip'], target_db_host[key]['port'], target_db_host[key]['user'],
                            target_db_host[key]['password'], db, sql_file, init_data, import_data
                        )
                        res, msg = yield self.thread_func.exec_remote_shell(
                            shell=shell_backup, host=host_160, port=port_160, username=user_160, password=password_160)
                        if res and not os.path.isfile(os.path.join(self.settings.get('static_path'), 'syncDB', sql_file)):
                            res, msg = yield self.thread_func.exec_remote_shell(
                                shell=shell_dump, host=host_160, port=port_160, username=user_160, password=password_160)
                        if res and os.path.isfile(os.path.join(self.settings.get('static_path'), 'syncDB', sql_file)):
                            res, msg = yield self.thread_func.exec_remote_shell(
                                shell=shell_import, host=host_160, port=port_160, username=user_160, password=password_160)
                            if res:
                                success_db.append(db)
                            else:
                                log.error(msg)
                        else:
                            log.error(msg)
            msg = dict(status='SUCCESS' if (len(success_db) == len(total_db) and len(success_db) > 0) else 'FAIL', message='同步成功的库: {}, 同步失败的库: {}'.format(
                ', '.join(success_db), ', '.join(list(set(total_db).difference(set(success_db))))), data='')
        elif op == 'recover':
            data = yield self.get_request_body_to_json()
            target_list, total = yield self.setting.get_settings_list(
                s_type='env', name=data.reTarget.server.key, status=1)
            dbs = list()
            for detail in target_list:
                desc = json.loads(detail.value)
                if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                    continue
                db_path = os.path.join(self.settings.get('static_path'), 'syncDB', data.date, desc.get('ip').strip())
                if not os.path.isdir(db_path):
                    continue
                sql_list = os.listdir(db_path)
                for sql in sql_list:
                    if sql.find('backup') == -1:
                        continue
                    sql = sql.split('_', maxsplit=1)
                    len(sql) > 1 and sql[0] not in dbs and dbs.append(sql[0])
            if dbs:
                database = [db.key for db in data.reTarget.dbs]
                for db in database:
                    if db not in dbs:
                        database.remove(db)
                database = database or dbs
                target_db_host = dict()
                success_db = list()
                for target in target_list:
                    desc = json.loads(target.value)
                    if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                        continue
                    for db in database:
                        if desc.get('description').find(db) != -1:
                            if target.id not in target_db_host.keys():
                                target_db_host[target.id] = dict(
                                    ip=desc.get('ip').strip(), port=desc.get('port').strip(), dbs=[db],
                                    user=desc.get('user').strip(), password=desc.get('password').strip())
                            else:
                                target_db_host[target.id]['dbs'].append(db)
                init_path = os.path.join(self.settings.get('static_path'), 'syncDB', 'initSQL')
                init_data_path = os.path.join(
                    self.settings.get('static_path'), 'syncDB', time.strftime('%Y%m%d'), 'data')
                if not os.path.isdir(init_data_path):
                    os.makedirs(init_data_path)
                init_sql = list()
                init_data_sql = dict()
                if os.path.isdir(init_path):
                    for file in os.listdir(init_path):
                        file = file.split('.', maxsplit=1)
                        if len(file) > 1 and file[1] == 'txt':
                            init_data_sql[file[0]] = []
                            continue
                        file = file[0].split('_', maxsplit=1) if len(file) > 1 and file[1] == 'sql' else None
                        file = file[1] if file and len(file) > 1 else None
                        file and init_sql.append(file)
                for key in target_db_host:
                    for db in target_db_host[key]['dbs']:
                        init_sql_file = '{}/data/{}.sql'.format(time.strftime('%Y%m%d'), db)
                        init_data = '/opt/lampp/bin/mysql -h{} -P{} -u{} -p{} -f {} < {}'.format(
                            target_db_host[key]['ip'], target_db_host[key]['port'], target_db_host[key]['user'],
                            target_db_host[key]['password'], db, 'initSQL/init_{}.sql'.format(db)
                        ) if db in init_sql else ''
                        import_data = '/opt/lampp/bin/mysql -h{} -P{} -u{} -p{} -f {} < {}'.format(
                            target_db_host[key]['ip'], target_db_host[key]['port'], target_db_host[key]['user'],
                            target_db_host[key]['password'], db, init_sql_file
                        ) if db in init_data_sql.keys() and init_data_sql[db] else ''
                        shell_import = '''cd {}
                        /opt/lampp/bin/mysql -h{} -P{} -u{} -p{} -f {} < {}
                        {}
                        {}'''.format(
                            root_160, target_db_host[key]['ip'], target_db_host[key]['port'], target_db_host[key]['user'],
                            target_db_host[key]['password'], db, '{}/{}/{}_backup.sql'.format(
                                data.date, target_db_host[key]['ip'], db), init_data, import_data
                        )
                        res, msg = yield self.thread_func.exec_remote_shell(
                            shell=shell_import, host=host_160, port=port_160, username=user_160, password=password_160)
                        if res:
                            success_db.append(db)
                        else:
                            log.error(msg)
                msg = dict(status='SUCCESS', message='还原成功的库: {}'.format(', '.join(success_db)), data='')
            else:
                msg = dict(status='FAIL', message='所选日期没有备份', data='')
        elif op == 'init':
            data = yield self.get_request_body_to_json()
            init_path = os.path.join(self.settings.get('static_path'), 'syncDB', 'initSQL')
            db_file = os.path.join(init_path, '{}.txt'.format(data.db))
            if not os.path.isdir(init_path):
                os.makedirs(init_path)
            with open(db_file, 'a', encoding='utf8') as fp:
                fp.writelines(['{}\n'.format(data.table)])
            msg = dict(status='SUCCESS', message='初始化数据表添加成功!', data='')
        elif op == 'delInit':
            data = yield self.get_request_body_to_json()
            init_path = os.path.join(self.settings.get('static_path'), 'syncDB', 'initSQL')
            db_file = os.path.join(init_path, '{}.txt'.format(data.db))
            if os.path.isfile(db_file):
                tables = list()
                with open(db_file, 'r', encoding='utf8') as fp:
                    for t in fp.readlines():
                        if data.table.strip() != t.strip():
                            tables.append(t)
                with open(db_file, 'w', encoding='utf8') as fp:
                    fp.writelines(tables)
            msg = dict(status='SUCCESS', message='初始化数据表删除成功!', data='')
        elif op == 'diff':
            data = yield self.get_request_body_to_json()
            if data.left.server.key == data.right.server.key:
                return self.write_json(dict(status='FAIL', message='数据库与参考数据库不能相同!', data=''))
            left_list, total = yield self.setting.get_settings_list(
                s_type='env', name=data.left.server.key, status=1)
            right_list, total = yield self.setting.get_settings_list(
                s_type='env', name=data.right.server.key, status=1)
            left_db_host = dict()
            right_db_host = dict()
            left_db = [db.key.strip() for db in data.left.dbs]
            object_type = data.objecType if 'ALL' not in data.objecType and len(data.objecType) != 7 else ['ALL']
            if not left_db:
                for left in left_list:
                    desc = json.loads(left.value)
                    if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                        continue
                    for db in desc.get('description').split(','):
                        left_db.append(db)
            for left in left_list:
                desc = json.loads(left.value)
                if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                    continue
                for db in left_db:
                    if desc.get('description').find(db) == -1:
                        continue
                    if left.id not in left_db_host.keys():
                        left_db_host[left.id] = dict(
                            ip=desc.get('ip').strip(), port=desc.get('port').strip(), tables=[tb.key.strip() for tb in data.left.tables],
                            user=desc.get('user').strip(), password=desc.get('password').strip(), dbs=[db])
                    else:
                        left_db_host[left.id]['dbs'].append(db)
            for right in right_list:
                desc = json.loads(right.value)
                if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                    continue
                for db in left_db_host:
                    for key in left_db_host[db]['dbs']:
                        if desc.get('description').find(key) == -1:
                            continue
                        if right.id not in right_db_host.keys():
                            right_db_host[right.id] = dict(
                                ip=desc.get('ip').strip(), port=desc.get('port').strip(),
                                tables=left_db_host[db]['tables'], left=db, dbs=[key],
                                user=desc.get('user').strip(), password=desc.get('password').strip())
                        else:
                            right_db_host[right.id]['dbs'].append(key)
            sql_path = os.path.join(self.settings.get('static_path'), 'diffDB', data.left.server.key, time.strftime('%Y%m%d%H%M%S'))
            if not os.path.isdir(sql_path):
                os.makedirs(sql_path)
            commands = list()
            for key in right_db_host:
                left_ip = left_db_host[right_db_host[key]['left']]['ip']
                left_port = left_db_host[right_db_host[key]['left']]['port']
                left_user = left_db_host[right_db_host[key]['left']]['user']
                left_pass = left_db_host[right_db_host[key]['left']]['password']
                right_ip = right_db_host[key]['ip']
                right_port = right_db_host[key]['port']
                right_user = right_db_host[key]['user']
                right_pass = right_db_host[key]['password']
                sql_file_path = os.path.join(sql_path, '{}_{}.sql'.format(left_ip, left_port))
                args = '--server1={0}:{1}@{2}:{3} --server2={4}:{5}@{6}:{7} --skip-table-options --force --difftype=sql --output={8}'.format(
                    left_user, left_pass, left_ip, left_port, right_user, right_pass, right_ip, right_port, sql_file_path
                )
                args_db = list()
                for db in left_db:
                    has_tb = False
                    for tb in (data.left.dbs and left_db_host[right_db_host[key]['left']]['tables']):
                        args_db.append('{0}.{1}:{0}.{1}'.format(db, tb))
                        has_tb = True
                    if has_tb:
                        continue
                    elif db in right_db_host[key]['dbs'] and db in left_db_host[right_db_host[key]['left']]['dbs']:
                        args_db.append('{0}:{0}'.format(db))
                for obj in object_type:
                    cmd = '{0} --objectype={1} {2}'.format(args, obj, ' '.join(args_db))
                    commands.append(cmd)
            result = list()
            for cmd in commands:
                res, output = yield self.thread_func.exec_shell(shell='mysqldiff {}'.format(cmd))
                if res: result.append(res)
            data = list()
            if os.path.isdir(sql_path):
                for file in os.listdir(sql_path):
                    with open(os.path.join(sql_path, file), 'r', encoding='utf8') as fp:
                        data.extend(fp.readlines())
            if len(data) > 0:
                msg = dict(status='SUCCESS', message='对比数据库差异成功, 请执行右边的SQL同步差异!', data=dict(
                    path=sql_path, content=' '.join(data)))
            elif len(result) == len(commands):
                msg = dict(status='SUCCESS', message='所对比数据库无差异!', data=dict(
                    path=sql_path, content=' '.join(data)))
            else:
                msg = dict(status='FAIL', message='对比数据库差异出现异常!', data=dict(
                    path=sql_path, content=' '.join(data)))
        elif op == 'execSQL':
            data = yield self.get_request_body_to_json()
            if os.path.isdir(data.path):
                env = data.get('path', '').split(os.sep)[-2]
                left_list, total = yield self.setting.get_settings_list(
                    s_type='env', name=env, status=1)
                left_db_host = dict()
                for left in left_list:
                    desc = json.loads(left.value)
                    if desc.get('type') != 'APPLICATION' or desc.get('title').upper().find('MYSQL') == -1:
                        continue
                    if '{}_{}'.format(desc.get('ip').strip(), desc.get('port').strip()) not in left_db_host.keys():
                        left_db_host['{}_{}'.format(desc.get('ip').strip(), desc.get('port').strip())] = dict(
                            ip=desc.get('ip').strip(), port=desc.get('port').strip(),
                            user=desc.get('user').strip(), password=desc.get('password').strip(),
                            dbs=[db for db in desc.get('description').split(',')])
                msg = dict(status='FAIL', message='差异SQL文件不存在!', data='')
                for file in os.listdir(data.path):
                    with open(os.path.join(data.path, file), 'r', encoding='utf8') as fp:
                        sql_content = fp.read()
                    run_sql = TestingModule(engine='mysql', host=left_db_host[file[:-4]].get('ip'), user=left_db_host[file[:-4]].get('user'),
                                            password=left_db_host[file[:-4]].get('password'), database=left_db_host[file[:-4]].get('dbs')[0],
                                            sql=sql_content, port=left_db_host[file[:-4]].get('port'))
                    res, msg = yield run_sql.run_some_sql()
                    if res:
                        msg = dict(status='SUCCESS', message='差异SQL同步成功!', data='')
                    else:
                        msg = dict(status='FAIL', message='差异SQL同步失败, 可能的原因: {}'.format(msg), data='')
            else:
                msg = dict(status='FAIL', message='差异SQL文件不存在!', data='')
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)


# 应用包差异对比
class PackageDiff(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op=None):
        AddLogs().add_logs(ip=self.request.remote_ip)
        if op == 'version':
            app = self.get_argument('app', '')
            version_path = os.path.join(self.settings.get('static_path'), 'diffAPP', '{}_version.txt'.format(app))
            ret_msg = dict(status='SUCCESS', message='', data=[])
            if os.path.isfile(version_path):
                with open(version_path, 'r', encoding='utf8') as fp:
                    versions = fp.readlines()
                    ret_msg = dict(status='SUCCESS', message='',
                                   data=[dict(key=str(uuid.uuid1()), id=v.split(',')[1], title=v.split(',')[0], description=v) for v in sorted(versions, reverse=True)])
        elif op == 'content':
            file = self.get_argument('file', '')
            diff_file = os.path.join(self.settings.get('static_path'), 'diffAPP', file)
            if os.path.isfile(diff_file):
                with open(diff_file, 'r', encoding='utf8') as fp:
                    content = fp.read()
            else:
                content = ''
            ret_msg = dict(status='SUCCESS' if content else 'FAIL',
                           message='获取差异内容成功!' if content else '差异内容文件不存在!', data=content)
        else:
            ret_msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(ret_msg)

    @authenticated_async
    @gen.coroutine
    def post(self, op='app'):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        data = yield self.get_request_body_to_json()
        if op == 'deploy':
            if not data:
                data = dict(ip=self.get_argument('ip', None), app=self.get_arguments('app'))
            if isinstance(data.get('app', []), list) and data.get('ip'):
                apps = list()
                for app in data.get('app', []):
                    if app.upper().find('APP') >= 0 and len(app.split(':', maxsplit=1)) == 2:
                        apps.append(app)
                if apps:
                    data['app'] = apps
                    self.__get_version(data)
                log.info(apps)
                return self.write_json(dict(status='SUCCESS', message='应用版本信息登记成功!', data=''))
            else:
                return self.write_json(dict(status='FAIL', message='请求参数格式不对!', data=''))
        elif op == 'app':
            diff_res = list()
            left_version = None
            right_version = None
            if data.appLeft.server.key != data.appRight.server.key:
                left_list, total = yield self.setting.get_settings_list(
                    s_type='env', name=data.appLeft.server.key, status=1)
                right_list, total = yield self.setting.get_settings_list(
                    s_type='env', name=data.appRight.server.key, status=1)
                left_app_host = dict()
                right_app_host = dict()
                for left in left_list:
                    desc = json.loads(left.value)
                    if desc.get('type') != 'OS' or desc.get('title', '').split('_')[0].upper() != 'LINUX':
                        continue
                    if desc.get('title', '').upper().find('APP') >= 0:
                        left_app_host = dict(
                            ip=desc.get('ip').strip(), port=desc.get('port').strip(), key=left.name,
                            user=desc.get('user').strip(), password=desc.get('password').strip())
                        break
                for right in right_list:
                    desc = json.loads(right.value)
                    if desc.get('type') != 'OS' or desc.get('title', '').split('_')[0].upper() != 'LINUX':
                        continue
                    if desc.get('title', '').upper().find('APP') >= 0:
                        right_app_host = dict(
                            ip=desc.get('ip').strip(), port=desc.get('port').strip(), key=right.name,
                            user=desc.get('user').strip(), password=desc.get('password').strip())
                        break
                left_local_path = os.path.join(self.settings.get('static_path'), 'diffAPP', left_app_host.get('key'))
                right_local_path = os.path.join(self.settings.get('static_path'), 'diffAPP', right_app_host.get('key'))
                git_path = os.path.join(left_local_path, '{}-{}'.format(data.appLeft.dbs.key, time.strftime('%H%M%S')))
                left_commit_id, app_name, left_version = yield self.__get_app_file(
                    left_app_host, data.appLeft.dbs.key, left_local_path, git_path)
                right_commit_id, app_name, right_version = yield self.__get_app_file(
                    right_app_host, data.appLeft.dbs.key, right_local_path, git_path)
                if left_commit_id and right_commit_id:
                    repo_base = Repo(git_path)
                    diff_content = repo_base.git.diff(left_commit_id, right_commit_id)
                    file = None
                    content = list()
                    file_path = os.path.join(left_local_path, right_app_host.get('key'))
                    if not os.path.isdir(file_path):
                        os.makedirs(file_path)
                    else:
                        shutil.rmtree(file_path)
                        os.makedirs(file_path)
                    for line in diff_content.splitlines():
                        if line.startswith('diff --git'):
                            if file and content:
                                with open(os.path.join(file_path, '{}.diff'.format(file.replace('/', '.'))), 'w', encoding='utf8', errors='ignore') as fp:
                                    fp.writelines(content)
                            file = line.split()[2][2:]
                            diff_res.append(dict(key=file.replace('/', '.'), title=file, file=os.path.join(
                                left_app_host.get('key'), right_app_host.get('key'), '{}.diff'.format(file.replace('/', '.'))
                            )))
                            content = list()
                        content.append('{}\n'.format(line))
                    if file and content:
                        with open(os.path.join(file_path, '{}.diff'.format(file.replace('/', '.'))), 'w', encoding='utf8', errors='ignore') as fp:
                            fp.writelines(content)
                    repo_base.close()
                if os.path.isdir(git_path):
                    shutil.rmtree(git_path)
            else:
                local_path = os.path.join(
                    self.settings.get('static_path'), 'diffAPP', data.appLeft.dbs.get('key'))
                left_commit_id = data.appLeft.tables.get('key', '').strip()
                right_commit_id = data.appRight.tables.get('key', '').strip()
                if os.path.isdir(local_path) and left_commit_id and right_commit_id:
                    repo_base = Repo(local_path)
                    diff_content = repo_base.git.diff(left_commit_id, right_commit_id)
                    file = None
                    content = list()
                    file_path = os.path.join(
                        self.settings.get('static_path'), 'diffAPP', '{}_{}'.format(left_commit_id, right_commit_id))
                    if not os.path.isdir(file_path):
                        os.makedirs(file_path)
                    else:
                        shutil.rmtree(file_path)
                        os.makedirs(file_path)
                    for line in diff_content.splitlines():
                        if line.startswith('diff --git'):
                            if file and content:
                                with open(os.path.join(file_path, '{}.diff'.format(file.replace('/', '.'))), 'w', encoding='utf8', errors='ignore') as fp:
                                    fp.writelines(content)
                            file = line.split()[2][2:]
                            diff_res.append(dict(key=file.replace('/', '.'), title=file, file=os.path.join(
                                '{}_{}'.format(left_commit_id, right_commit_id), '{}.diff'.format(file.replace('/', '.')))))
                            content = list()
                        content.append('{}\n'.format(line))
                    if file and content:
                        with open(os.path.join(file_path, '{}.diff'.format(file.replace('/', '.'))), 'w', encoding='utf8', errors='ignore') as fp:
                            fp.writelines(content)
                    repo_base.close()
            msg = dict(status='SUCCESS' if left_commit_id and right_commit_id else 'FAIL',
                       message='对比应用包差异成功!' if diff_res else '所对比的应用包无差异!' if left_commit_id and right_commit_id else '获取需要对比的文件失败!',
                       data=dict(leftVersion=left_version, rightVersion=right_version, diffRes=diff_res))
        elif op == 'jacoco':
            data = yield self.get_request_body_to_json()
            msg = ''
            if data and data.get('left') != 'allVersions' and data.get('app'):
                left_commit_id = data.get('left', '').strip()
                if left_commit_id == 'earliest': left_commit_id = None
                app = data.get('app', '').strip()
                local_path = os.path.join(
                    self.settings.get('static_path'), 'diffAPP')
                git_path = os.path.join(local_path, app)
                right_commit_id = None
                if os.path.isdir(git_path):
                    try:
                        repo_base = Repo(git_path)
                    except Exception as e:
                        log.error(e)
                        repo_base = Repo.init(git_path)
                    adds = repo_base.index.add('*')
                    if adds:
                        right_commit_id = repo_base.index.commit('jacoco lastest')
                    repo_base.close()
                    if (not left_commit_id or not right_commit_id) and os.path.isfile(os.path.join(local_path, '{}_version.txt'.format(app))):
                        with open(os.path.join(local_path, '{}_version.txt'.format(app)), 'r', encoding='utf8') as fp:
                            content = fp.readlines()
                        if content:
                            content = sorted(content, reverse=True)
                            if not left_commit_id: left_commit_id = content[-1].split(',')[1].strip()
                            if not right_commit_id: right_commit_id = content[0].split(',')[1].strip()
                if left_commit_id and right_commit_id and left_commit_id != right_commit_id and app:
                    repo_base = Repo(git_path)
                    diff_content = repo_base.git.diff(left_commit_id, right_commit_id)
                    repo_base.close()
                    file = None
                    content = list()
                    file_path = os.path.join(local_path, data.get('jobId', ''), 'jacoco_{}_{}.txt'.format(app, right_commit_id))
                    for line in diff_content.splitlines():
                        if line.startswith('diff --git'):
                            if file and file.endswith('.java'):
                                content.append('{}.class\n'.format(file[:-5]))
                            file = line.split()[2][2:]
                    if file and file.endswith('.java'):
                        content.append('{}.class\n'.format(file[:-5]))
                    if content:
                        with open(file_path, 'w', encoding='utf8', errors='ignore') as fp:
                            fp.writelines(content)
                        msg = '{}{}jacoco_{}_{}.txt'.format(data.get('jobId', ''), os.sep, app, right_commit_id)
            return self.finish(msg)
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg)

    @gen.coroutine
    def __get_app_file(self, app_host, app, local_path, git_path):
        app = app.split(':', maxsplit=1)
        version = app[1] if len(app) > 1 else None
        app_name = app[0][9:]
        if app_name == 'user':
            app_name = 'uaccount'
        elif app_name == 'msg':
            app_name = 'message'
        elif app_name == 'account':
            app_name = 'myaccount'
        elif app_name == 'thirdplat':
            app_name = 'partner'
        elif app_name == 'bizlog':
            app_name = 'biz-log'
        elif app_name == 'paymentmonitor':
            app_name = 'payment-monitor'
        elif app_name == 'canal':
            app_name = 'cannal'
        elif app_name == 'ifcert':
            app_name = 'ifcert-gateway'
        if version:
            copy_shell = '''if [ ! -x "/databak" ]; then mkdir /databak; fi
    cd /databak
    dok=$(docker ps -a|grep {app}|grep {version})
    if [ "$dok" == "" ];then echo -e "\033[31m Error: app version is not exist!\033[0m";exit 1; fi
    if [ ! -x {app_name} ]; then mkdir {app_name}; fi
    rm -rf /databak/{app_name}/*
    rm -rf /databak/{app}
    docker cp {app}:/data/{app} ./
    if [ ! -x {app} ];then echo -e "\033[31m Error: docker cp fail!\033[0m";exit 1;fi
    cp {app}/lib/xnol-{app_name}-app-*.jar {app_name}/
    rm -rf /databak/{app}
    mv /databak/{app_name}/xnol-{app_name}-app-*.jar /databak/{app_name}/xnol-{app_name}-app-{version}.jar || echo -e "\033[31m Error: jar file copy fail!\033[0m";exit 1
            '''.format(**dict(app=app[0], app_name=app_name, version=version))
            remote_file = 'xnol-{}-app-{}.jar'.format(app_name, version)
        else:
            copy_shell = '''if [ ! -x "/databak" ]; then mkdir /databak; fi
    cd /databak
    if [ ! -x {app_name} ]; then mkdir {app_name}; fi
    rm -rf /databak/{app_name}/*
    rm -rf /databak/{app}
    docker cp {app}:/data/{app} ./
    if [ ! -x {app} ];then echo -e "\033[31m Error: docker cp fail!\033[0m";exit 1;fi
    cp {app}/lib/xnol-{app_name}-app-*.jar {app_name}/
    rm -rf /databak/{app}
    ls /databak/{app_name}/xnol-{app_name}-app-*.jar
    mv /databak/{app_name}/xnol-{app_name}-app-*.jar /databak/{app_name}/xnol-{app_name}-app-lastest.jar || echo -e "\033[31m Error: jar file copy fail!\033[0m";exit 1
            '''.format(**dict(app=app[0], app_name=app_name))
            remote_file = 'xnol-{}-app-lastest.jar'.format(app_name)
        try:
            res, msg = yield self.thread_func.exec_remote_shell(
                host=app_host.get('ip'), port=app_host.get('port'),
                username=app_host.get('user'), password=app_host.get('password'), shell=copy_shell)
            commit_id = False
            if res and msg.find('Error') < 0:
                if not version:
                    version = msg.split('-')
                    version = version[5][:-4] if len(version) > 5 else None
                app_file = 'xnol-{}-app-{}.jar'.format(app_name, version or 'lastest')
                if not os.path.isdir(local_path):
                    os.makedirs(local_path)
                local_path = os.path.join(local_path, app_file)
                remote_path = '/databak/{}/{}'.format(app_name, remote_file)
                res, msg = yield self.thread_func.exec_sftp(
                    host=app_host.get('ip'), port=app_host.get('port'), username=app_host.get('user'),
                    password=app_host.get('password'), do='get', local_path=local_path, remote_path=remote_path)
                if not os.path.isdir(git_path):
                    Repo.init(git_path)
                jd = os.path.join(self.settings.get('static_path'), 'files', 'jd-core-java-1.2.jar')
                if os.path.isfile(jd) and res:
                    res, msg = yield self.thread_func.exec_shell(shell='java -jar "{}" "{}" "{}"'.format(jd, local_path, git_path))
                    repo_base = Repo(git_path)
                    adds = repo_base.index.add('*')
                    if adds and (res or msg.find('Decompiled') >= 0):
                        commit_id = repo_base.index.commit(version or 'lastest')
                    repo_base.close()
                else:
                    return False, app[0], version
            if os.path.isfile(local_path):
                os.remove(local_path)
            return commit_id, app[0], version
        except Exception as e:
            log.error(e)
            if os.path.isfile(local_path):
                os.remove(local_path)
            return False, app[0], version

    @gen.coroutine
    def __get_version(self, data):
        app_host = dict()
        if data.get('ip'):
            servers, total = yield self.setting.get_settings_list(s_type='env', status=1, search=data.get('ip'))
            for host in servers:
                desc = json.loads(host.value)
                if desc.get('type') != 'OS' or desc.get('title', '').split('_')[0].upper() != 'LINUX':
                    continue
                if desc.get('title', '').upper().find('APP') >= 0:
                    app_host = dict(
                        ip=desc.get('ip').strip(), port=desc.get('port').strip(), key=host.name,
                        user=desc.get('user').strip(), password=desc.get('password').strip())
                    break
        if app_host:
            for app in data.get('app', []):
                local_path = os.path.join(self.settings.get('static_path'), 'diffAPP')
                git_path = os.path.join(local_path, app.split(':', maxsplit=1)[0])
                commit_id, app_name, version = yield self.__get_app_file(app_host, app, local_path, git_path)
                if commit_id and version:
                    version_path = os.path.join(local_path, '{}_version.txt'.format(app_name))
                    if os.path.isfile(version_path):
                        with open(version_path, 'r', encoding='utf8') as fp:
                            version_list = fp.readlines()
                    else:
                        version_list = list()
                    is_new = True
                    for i in range(len(version_list)):
                        if version_list[i].split(',')[0] == version:
                            version_list[i] = '{},{}\n'.format(version, commit_id)
                            is_new = False
                            break
                    if is_new:
                        version_list.append('{},{}\n'.format(version, commit_id))
                    with open(version_path, 'w', encoding='utf8') as fp:
                        fp.writelines(version_list)
