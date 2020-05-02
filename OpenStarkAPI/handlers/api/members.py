from handlers.common import BaseHandler, authenticated_async
from tornado import gen
from handlers.common import AddLogs
import json


"""
团队管理相关接口
"""


# 团队管理
class DepartmentsEdit(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self):
        AddLogs().add_logs(ip=self.request.remote_ip)
        op = self.get_argument('type', '')
        groups = []
        members = dict(data=[])
        if op == 'groups':
            groups = yield self.__get_group()
        elif op == 'members':
            callback = self.get_argument('callback', None)
            members = yield self.__get_members(status=2 if callback else None)
            if callback:
                return self.write_json('{}({})'.format(callback, members['data']))
        elif op == 'teams':
            teams = yield self.option.get_options_list(o_type='teams', name='team')
            departments = yield self.option.get_options_list(o_type='teams', name='department')
            teams_list = []
            for team in teams:
                department = '火星部门'
                for d in departments:
                    if d.id == json.loads(team.value)['up']:
                        department = json.loads(d.value)['name']
                teams_list.append(dict(tid=team.id, name='{} ({})'.format(json.loads(team.value)['name'], department)))
            return self.write_json(dict(status='SUCCESS', message='', data=teams_list))
        else:
            groups = yield self.__get_group()
            members = yield self.__get_members()
        self.write_json(dict(status='SUCCESS', message='', data=dict(groups=groups, members=members)))

    @authenticated_async
    @gen.coroutine
    def post(self, op='edit'):
        AddLogs().add_logs(ip=self.request.remote_ip, op_type='active')
        data = yield self.get_request_body_to_json()
        if data.type == 'groups':
            if op == 'edit':
                msg = yield self.__save_group(data.data)
            elif op == 'delete':
                msg = yield self.__delete_group(data.data)
            else:
                msg = dict(status='FAIL', message='操作类型错误', data='')
        elif data.type == 'members':
            if op == 'edit':
                msg = yield self.__save_members(data.data)
            elif op == 'delete':
                msg = yield self.__delete_members(data.data)
            else:
                msg = dict(status='FAIL', message='操作类型错误', data='')
        elif data.type == 'reset':
            user = data.data
            email = user.email or ''
            res, msg = yield self.user.edit_user(uid=user.uid, password=email.split('@')[0]+'123456')
            if res:
                msg = dict(status='SUCCESS', message='密码重置成功!', data='')
            else:
                msg = dict(status='FAIL', message=msg, data='')
        else:
            msg = dict(status='FAIL', message='操作类型错误', data='')
        self.write_json(msg=msg)

    @gen.coroutine
    def __get_members(self, status=None):
        page = int(self.get_argument('page', 1))
        size = int(self.get_argument('size', 10))
        name = self.get_argument('name', '')
        users, total = yield self.user.get_users_list(page=page, limit=size or None, name=name or None, status=status)
        members = []
        no = 0
        for u in users:
            no += 1
            profile = json.loads(u.profile)
            label = []
            for d in profile['department']:
                res = yield self.option.get_option(oid=d)
                if res:
                    label.append(json.loads(res.value)['name'])
                else:
                    break
            members.append(dict(key=no+page*size-size, uid=u.id, username=u.username, name=u.realname, email=u.email, role=u.role,
                                status=u.status, workerId=profile['workerId'] if 'workerId' in profile.keys() else '',
                                position=profile['position'], department=dict(value=profile['department'],
                                                                              label=' / '.join(label))))
        return dict(data=members, page=page, size=size, total=total)

    @gen.coroutine
    def __save_members(self, data):
        if str(data.key).find('NEW_TEMP_ID') != -1 and data.uid == '':
            email = data.email.strip() or ''
            name = data.name.strip() or ''
            username = data.username.strip() or ''
            department = data.department or []
            if name == '':
                msg = dict(status='FAIL', message='请填写姓名!', data='')
            elif not department:
                msg = dict(status='FAIL', message='请选择部门!', data='')
            elif not self.common_func.check_string(username, 'username'):
                msg = dict(status='FAIL', message='用户名格式不对, 请检查!', data='')
            elif not self.common_func.check_string(email, 'email'):
                msg = dict(status='FAIL', message='邮箱格式不对, 请检查!', data='')
            else:
                res, msg = yield self.user.register_user(
                    email=email, password=email.split('@')[0]+'123456', real_name=name,
                    profile=dict(department=department, workerId=data.workerId.strip(),
                                 avatar='https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
                                 position=data.position.strip()), username=username, role=data.role or None, status=data.status or None)
                if res:
                    label = []
                    for d in department:
                        res = yield self.option.get_option(oid=d)
                        if res:
                            label.append(json.loads(res.value)['name'])
                        else:
                            break
                    msg = dict(status='SUCCESS', message='新增用户成功!', data=dict(uid=res.id, label=' / '.join(label)))
                else:
                    msg = dict(status='FAIL', message=msg, data='')
        else:
            email = data.email.strip() or ''
            name = data.name.strip() or ''
            username = data.username.strip() or ''
            department = data.department or []
            if name == '':
                msg = dict(status='FAIL', message='请填写姓名!', data='')
            elif not department:
                msg = dict(status='FAIL', message='请选择部门!', data='')
            elif not self.common_func.check_string(username, 'username'):
                msg = dict(status='FAIL', message='用户名格式不对, 请检查!', data='')
            elif not self.common_func.check_string(email, 'email'):
                msg = dict(status='FAIL', message='邮箱格式不对, 请检查!', data='')
            else:
                user = yield self.user.get_user_info(uid=data.uid)
                if user:
                    profile = json.loads(user.profile)
                    profile['department'] = department
                    profile['workerId'] = data.workerId.strip()
                    profile['position'] = data.position.strip()
                    res, msg = yield self.user.edit_user(email=email, uid=data.uid, username=username, real_name=name, role=data.role or None,
                                                         status=data.status or None, profile=profile)
                    if res:
                        label = []
                        for d in department:
                            res = yield self.option.get_option(oid=d)
                            if res:
                                label.append(json.loads(res.value)['name'])
                            else:
                                break
                        msg = dict(status='SUCCESS', message='编辑用户成功!', data=dict(label=' / '.join(label)))
                    else:
                        msg = dict(status='FAIL', message=msg, data='')
                else:
                    msg = dict(status='FAIL', message='所编辑用户不存在!', data='')
        return msg

    @gen.coroutine
    def __delete_members(self, data):
        user = yield self.user.get_user_info(uid=data.uid)
        if user:
            if user.role == 0:
                return dict(status='FAIL', message='不能删除管理员账户!', data='')
            res, msg = yield self.user.delete_user(uid=data.uid)
            if res:
                yield self.msg.delete_message(user_id=data.uid)
                msg = dict(status='SUCCESS', message='删除用户成功', data='')
            else:
                msg = dict(status='FAIL', message=msg, data='')
        else:
            msg = dict(status='FAIL', message='用户不存在!', data='')
        return msg

    @gen.coroutine
    def __get_group(self):
        teams = yield self.option.get_options_list(o_type='teams', status=1)
        groups = []
        company = dict()
        department = dict()
        for team in teams:
            if team.name == 'company':
                company[team.id] = json.loads(team.value)['name']
            if team.name == 'department':
                department[team.id] = json.loads(team.value)
        department_id = set()
        company_id = set()
        no = 0
        for t in teams:
            if t.name == 'team':
                team = json.loads(t.value)
                no += 1
                groups.append(dict(key=no, company=company[department[team['up']]['up']],
                                   cid=department[team['up']]['up'], tid=t.id, did=team['up'],
                                   department=department[team['up']]['name'], team=team['name']))
                company_id.add(department[team['up']]['up'])
                department_id.add(team['up'])
        for d in department_id:
            department.pop(d)
        for dep in department:
            no += 1
            groups.append(dict(key=no, company=company[department[dep]['up']], cid=department[dep]['up'],
                               department=department[dep]['name'], did=dep, team='', tid=0))
            company_id.add(department[dep]['up'])
        for c in company_id:
            company.pop(c)
        for com in company:
            no += 1
            groups.append(dict(key=no, company=company[com], cid=com, department='', did=0, team='', tid=0))
        return groups

    @gen.coroutine
    def __save_group(self, data):
        if str(data.key).find('NEW_TEMP_ID') != -1:
            cid, msg = yield self.option.add_option(o_type='teams', name='company', value=dict(name=data.company.strip()))
            if cid:
                did, msg = yield self.option.add_option(o_type='teams', name='department',
                                                        value=dict(name=data.department.strip(), up=cid))
                if did:
                    tid = ''
                    if data.team.strip() != '':
                        tid, msg = yield self.option.add_option(o_type='teams', name='team',
                                                                value=dict(name=data.team.strip(), up=did))
                        if not tid:
                            return dict(status='FAIL', message=msg, data='')
                    return dict(status='SUCCESS', message='新增团队成功', data=dict(cid=cid, did=did, tid=tid))
                else:
                    return dict(status='FAIL', message=msg, data='')
            else:
                company = yield self.option.get_options_list(o_type='teams', name='company')
                cid = False
                for com in company:
                    if json.loads(com.value)['name'] == data.company.strip():
                        cid = com.id
                        if com.status != 1:
                            yield self.option.edit_option(oid=com.id, status=1)
                            break
                if cid:
                    did, msg = yield self.option.add_option(o_type='teams', name='department',
                                                            value=dict(name=data.department.strip(), up=cid))
                    if did:
                        tid = ''
                        if data.team.strip() != '':
                            tid, msg = yield self.option.add_option(o_type='teams', name='team',
                                                                    value=dict(name=data.team.strip(), up=did))
                            if not tid:
                                return dict(status='FAIL', message=msg, data='')
                        return dict(status='SUCCESS', message='新增团队成功', data=dict(cid=cid, did=did, tid=tid))
                    else:
                        dep = yield self.option.get_options_list(o_type='teams', name='department')
                        did = False
                        for d in dep:
                            if json.loads(d.value)['name'] == data.department.strip():
                                did = d.id
                                if d.status != 1:
                                    yield self.option.edit_option(oid=d.id, status=1)
                                    break
                        if did:
                            if data.team.strip() != '':
                                tid, msg = yield self.option.add_option(o_type='teams', name='team',
                                                                        value=dict(name=data.team.strip(), up=did))
                                if tid:
                                    return dict(status='SUCCESS', message='新增团队成功',
                                                data=dict(cid=cid, did=did, tid=tid))
                                else:
                                    return dict(status='FAIL', message=msg, data='')
                            else:
                                return dict(status='FAIL', message='新增的部门已存在', data='')
                        else:
                            return dict(status='FAIL', message='部门名称应该存在, 但是没找到!', data='')
                else:
                    return dict(status='FAIL', message='公司名称应该存在, 但是没找到!', data='')
        else:
            cid, msg = yield self.option.edit_option(oid=data.cid, value=dict(name=data.company.strip()))
            if cid:
                if data.did != 0 and data.department.strip() != '':
                    did, msg = yield self.option.edit_option(oid=data.did, value=dict(name=data.department.strip(),
                                                             up=cid if not isinstance(cid, bool) else data.cid))
                elif data.did == 0 and data.department.strip() != '':
                    did, msg = yield self.option.add_option(o_type='teams', name='department',
                                                            value=dict(name=data.department.strip(),
                                                                       up=cid if not isinstance(cid, bool) else data.cid))
                else:
                    did = False
                    msg = '部门信息不能为空'
                if did:
                    if data.tid != 0 and data.team.strip() != '':
                        tid, msg = yield self.option.edit_option(oid=data.tid, value=dict(name=data.team.strip(),
                                                                 up=did if not isinstance(did, bool) else data.did))
                    elif data.tid == 0 and data.team.strip() != '':
                        tid, msg = yield self.option.add_option(o_type='teams', name='team',
                                                                value=dict(name=data.team.strip(),
                                                                           up=did if not isinstance(did, bool) else data.did))
                    else:
                        tid = did
                    if tid:
                        return dict(status='SUCCESS', message='编辑团队成功', data='')
                    else:
                        return dict(status='FAIL', message=msg, data='')
                else:
                    return dict(status='FAIL', message=msg, data='')
            else:
                return dict(status='FAIL', message=msg, data='')

    @gen.coroutine
    def __delete_group(self, data):
        if data.tid != 0:
            res, msg = yield self.option.delete_option(oid=data.tid)
        elif data.tid == 0 and data.did != 0:
            res, msg = yield self.option.delete_option(oid=data.did)
        elif data.did == 0 and data.cid != 0:
            res, msg = yield self.option.delete_option(oid=data.cid)
        else:
            return dict(status='FAIL', message='删除失败', data='')
        if res:
            return dict(status='SUCCESS', message='删除团队成功', data='')
        else:
            return dict(status='FAIL', message=msg, data='')
