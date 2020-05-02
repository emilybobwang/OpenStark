from modules.setting import SettingModule
from modules.project import ProjectModule
from functions.common import CommonFunction, ThreadFunction, OptionsFunction
from settings import net_mail_to, net_mail_cc, static_path, host_160, port_160, user_160, password_160, root_160, jenkins_url, jenkins_user, jenkins_password, jenkins_jacoco
from tornado import gen
from tornado.log import app_log as log
from datetime import timedelta
from munch import munchify
import jenkins
import time
import json
import os
import re
import shutil


class JobsMonitor(object):
    def __init__(self):
        self.project = ProjectModule()
        self.setting = SettingModule()
        self.option_func = OptionsFunction()
        self.common_func = CommonFunction()
        self.thread_func = ThreadFunction()
        self.jenkins_server = jenkins.Jenkins(url=jenkins_url, username=jenkins_user, password=jenkins_password, timeout=5)

    # 监控任务状态
    @gen.coroutine
    def jobs_status(self):
        try:
            job_list, total = yield self.setting.get_settings_list(s_type=['job', 'jobG', 'jobA'], status=[0, 2], pj_status=1)
            for job in job_list:
                desc = json.loads(job.value)
                if (desc.get('buildEnv') or desc.get('dayBuild')) and job.status == 0 and int(time.time()) > int(job.createTime.timestamp()):
                    yield self.setting.edit_setting(sid=job.id, status=1)
                    continue
                job_name = desc.get('jobName') if job.type != 'job' else jenkins_jacoco
                if job_name and job.status == 2:
                    if job.type != 'job':
                        last_build_number = self.jenkins_server.get_job_info(job_name).get('lastBuild').get('number')
                        last_build = self.jenkins_server.get_build_info(job_name, last_build_number)
                        status = None if last_build.get('building') else 0
                    else:
                        status = None
                    if (job.type != 'job' and last_build.get('queueId') == desc.get('queueId')) or (job_name == jenkins_jacoco):
                        if (job.type != 'job' and status is None and desc['url'] == last_build.get('url')) or (job_name == jenkins_jacoco):
                            if desc.get('jacocoId'):
                                jacoco_job = self.jenkins_server.get_job_info(jenkins_jacoco)
                                first_build_number = jacoco_job.get('firstBuild').get('number')
                                last_build_number = jacoco_job.get('lastBuild').get('number')
                                for num in range(first_build_number, last_build_number + 1):
                                    try:
                                        jacoco = self.jenkins_server.get_build_info(jenkins_jacoco, num)
                                        if jacoco.get('queueId') != desc.get('jacocoId'):
                                            continue
                                        if not jacoco.get('building') and jacoco.get('result') == 'FAILURE':
                                            day_build_env = desc.get('buildEnv') or desc.get('dayBuild')
                                            apps = yield self.option_func.get_env_info(eid=day_build_env)
                                            stop_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 3600 * 24))
                                            parameters = [('ACTION', 'Monitoring'), ('STOPTIME', stop_time),
                                                          ('CLEAN', 'No'), ('JOB_ID', job.name)]
                                            for app in [a.get('details') for a in apps]:
                                                for ap in app:
                                                    if ap.get('title').lower().find('linux_app') != -1:
                                                        parameters.append(('ENV', ap.get('ip')))
                                            if len(parameters) > 4:
                                                version_file = os.path.join(static_path, 'diffAPP', job.name)
                                                if not os.path.isdir(version_file):
                                                    os.makedirs(version_file)
                                                version_file = os.path.join(version_file, 'jacoco_app_version.txt')
                                                if os.path.isfile(version_file): os.remove(version_file)
                                                for app in (desc.get('runApps') or []):
                                                    parameters.append(('APP', app))
                                                jacoco_id = self.jenkins_server.build_job(jenkins_jacoco, parameters=parameters)
                                                desc['jacocoId'] = jacoco_id
                                                yield self.setting.edit_setting(sid=job.id, value=desc)
                                    except Exception as e:
                                        log.error(e)
                                        continue
                            continue
                        desc['url'] = last_build.get('url')
                        cycle = desc.get('cycle')
                        if cycle == 'hour':
                            next_time = job.createTime + timedelta(hours=1)
                        elif cycle == 'day':
                            next_time = job.createTime + timedelta(days=1)
                        elif cycle == 'week':
                            next_time = job.createTime + timedelta(weeks=1)
                        elif cycle == 'mouth':
                            next_time = job.createTime + timedelta(days=30)
                        elif cycle == 'year':
                            next_time = job.createTime + timedelta(days=365)
                        else:
                            next_time = job.createTime
                            if status == 0: status = 3
                        if status in [0, 3] and desc.get('jacocoId'):
                            jacoco_job = self.jenkins_server.get_job_info(jenkins_jacoco)
                            first_build_number = jacoco_job.get('firstBuild').get('number')
                            last_build_number = jacoco_job.get('lastBuild').get('number')
                            for num in range(first_build_number, last_build_number + 1):
                                try:
                                    jacoco = self.jenkins_server.get_build_info(jenkins_jacoco, num)
                                    if jacoco.get('queueId') != desc.get('jacocoId'):
                                        continue
                                    self.jenkins_server.stop_build(jenkins_jacoco, num)
                                except Exception as e:
                                    log.error(e)
                                    continue
                                apps = yield self.option_func.get_env_info(eid=desc.get('buildEnv') or desc.get('dayBuild'))
                                desc['buildEnv'] = ''
                                parameters = [('ACTION', 'Reporting'), ('HIS_BUILD_ID', num),
                                              ('CLEAN', 'Yes'), ('JOB_ID', job.name)]
                                for app in [a.get('details') for a in apps]:
                                    for ap in app:
                                        if ap.get('title').lower().find('linux_app') != -1:
                                            parameters.append(('ENV', ap.get('ip')))
                                if len(parameters) > 4:
                                    for app in (desc.get('runApps') or []):
                                        parameters.append(('APP', app))
                                    self.jenkins_server.build_job(jenkins_jacoco, parameters=parameters)
                        yield self.setting.edit_setting(sid=job.id, value=desc, status=status,
                                                        create_time=next_time.strftime('%Y-%m-%d %H:%M:%S') if status in [0, 3] else None)
        except Exception as e:
            log.warning(e)

    # 执行定时任务
    @gen.coroutine
    def run_jobs(self):
        try:
            job_list, total = yield self.setting.get_settings_list(s_type=['jobG', 'jobA'], status=1, pj_status=1)
            for job in job_list:
                desc = json.loads(job.value)
                job_name = desc.get('jobName')
                day_build_env = desc.get('buildEnv') or desc.get('dayBuild')
                if not job_name or not day_build_env:
                    continue
                data = munchify(dict(env=day_build_env, type='api' if job.type == 'jobA' else 'gui', exec=job_name))
                yield self.option_func.get_hosts_info(data)
                yield self.option_func.get_mysql_jdbc(eid=day_build_env, data=data)
                yield self.option_func.get_cases_info(job, data)
                queue_id = self.jenkins_server.build_job(job_name, parameters=dict(JOB_ID=job.name))
                if queue_id:
                    apps = yield self.option_func.get_env_info(eid=day_build_env)
                    stop_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 3600 * 24))
                    parameters = [('ACTION', 'Monitoring'), ('STOPTIME', stop_time),
                                  ('CLEAN', 'Yes'), ('JOB_ID', job.name)]
                    for app in [a.get('details') for a in apps]:
                        for ap in app:
                            if ap.get('title').lower().find('linux_app') != -1:
                                parameters.append(('ENV', ap.get('ip')))
                    if len(parameters) > 4:
                        version_file = os.path.join(static_path, 'diffAPP', job.name)
                        if not os.path.isdir(version_file):
                            os.makedirs(version_file)
                        version_file = os.path.join(version_file, 'jacoco_app_version.txt')
                        if os.path.isfile(version_file): os.remove(version_file)
                        for app in (desc.get('runApps') or []):
                            parameters.append(('APP', app))
                        jacoco_id = self.jenkins_server.build_job(jenkins_jacoco, parameters=parameters)
                        desc['jacocoId'] = jacoco_id
                    desc['queueId'] = queue_id
                    desc['url'] = self.jenkins_server.get_job_info(job_name).get('url')
                    yield self.setting.edit_setting(sid=job.id, value=desc, status=2)
        except Exception as e:
            log.warning(e)

    # 申请关闭外网权限
    @gen.coroutine
    def close_network(self):
        try:
            now_date = time.strftime('%Y-%m-%d')
            now_time = time.strftime('%H:%M:%S')
            if now_time > '08:30:00':
                server, total = yield self.setting.get_settings_list(s_type='env', status=1)
                ips = list()
                for svr in server:
                    desc = json.loads(svr.value)
                    if (svr.createTime.strftime('%Y-%m-%d') < now_date or (
                            svr.createTime.strftime('%Y-%m-%d') == now_date and now_time > svr.createTime.strftime('%H:%M:%S'))
                    ) and desc.get('network') == 'yes' and desc.get('ip'):
                        ips.append(desc.get('ip').strip())
                if set(ips):
                    title = '测试环境申请关闭外网权限'
                    mail_content = '''
                    <p>Hi 你好！</p>
                    <p style="padding-left:30px;">测试人员已完成测试任务，申请关闭以下测试环境服务器外网权限。请帮忙处理一下，3ks~</p>
                    <p style="padding-left:30px;">1、服务器</p>
                    <p style="padding-left:60px;">{}</p>    
                                    '''.format('</br>'.join(set(ips)))
                    res, msg = yield self.common_func.send_email(
                        subject=title, content=mail_content, to=net_mail_to, cc=net_mail_cc)
                    if res:
                        log.info(msg)
                        for svr in server:
                            desc = json.loads(svr.value)
                            if (svr.createTime.strftime('%Y-%m-%d') < now_date or (
                                svr.createTime.strftime('%Y-%m-%d') == now_date and now_time > svr.createTime.strftime('%H:%M:%S'))
                            ) and desc.get('network') == 'yes' and desc.get('ip'):
                                desc['network'] = 'no'
                                yield self.setting.edit_setting(sid=svr.id, value=desc)
                    else:
                        log.warn(msg)
        except Exception as e:
            log.error(e)

    # 同步准生产数据库表
    @gen.coroutine
    def sync_db_tables(self):
        dumps = dict()
        db_path = os.path.join(static_path, 'syncDB', 'lasTables')
        if not os.path.isdir(db_path):
            os.makedirs(db_path)
        flag_file = os.path.join(db_path, 'TAG')
        old_date = ''
        if os.path.isfile(flag_file):
            with open(flag_file, 'r') as fp:
                old_date = fp.read()
        now_date = time.strftime('%Y%m%d')
        if old_date != now_date:
            env_list, total = yield self.project.get_projects_list(
                p_type='env', status=1, search='准生产')
            for env in env_list:
                details, total = yield self.setting.get_settings_list(
                    s_type='env', name=env.name)
                for detail in details:
                    desc = json.loads(detail.value)
                    if desc.get('type') != 'APPLICATION' and desc.get('title').upper().find('MYSQL') == -1:
                        continue
                    dumps[detail.id] = dict(ip=desc.get('ip').strip(), port=desc.get('port').strip(), user=desc.get('user').strip(),
                                            password=desc.get('password').strip(), dbs=desc.get('description').split(','))
                break
            with open(flag_file, 'w') as fp:
                fp.write(time.strftime('%Y%m%d'))
            for key in dumps:
                for db in dumps[key]['dbs']:
                    tmp_path = os.path.join(db_path, '{}_tmp.txt'.format(db))
                    shell_dump = '''cd {}
                    /opt/lampp/bin/mysqldump -h{} -P{} -u{} -p{} -d {} > {}'''.format(
                        root_160, dumps[key]['ip'], dumps[key]['port'], dumps[key]['user'], dumps[key]['password'],
                        db, 'lasTables/{}_tmp.txt'.format(db)
                    )
                    res, msg = yield self.thread_func.exec_remote_shell(
                        shell=shell_dump, host=host_160, port=port_160, username=user_160, password=password_160)
                    if res and os.path.isfile(tmp_path):
                        with open(tmp_path, 'r', encoding='utf8') as fp:
                            lines = fp.readlines()
                        tables = list()
                        for line in lines:
                            if line.find('DROP TABLE IF EXISTS') == -1:
                                continue
                            table = re.findall(r'`(\w+)`;', line)
                            table and tables.append('{}\n'.format(table[0]))
                        with open(os.path.join(db_path, '{}.txt'.format(db)), 'w') as fp:
                            fp.writelines(tables)
                        os.remove(tmp_path)
                    else:
                        log.info(msg)
        old_time = time.time() - 30 * 24 * 3600
        old_path = os.path.join(static_path, 'syncDB', time.strftime('%Y%m%d', time.gmtime(old_time)))
        if os.path.isdir(old_path):
            shutil.rmtree(old_path)

def jobs_status():
    job = JobsMonitor()
    job.jobs_status()

def run_jobs():
    job = JobsMonitor()
    job.run_jobs()

def close_network():
    job = JobsMonitor()
    job.close_network()

def sync_db_tables():
    job = JobsMonitor()
    job.sync_db_tables()
