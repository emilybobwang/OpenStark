import json
from Crypto.Hash import MD5
from urllib.parse import quote_plus


"""
签名方法函数格式:
def 方法名(接口请求内容接收变量"body", 项目自定义参数接收变量"params", 项目相关加密方法接收变量"encrypt"):
    方法过程
"""


# 比搜益加签POST方法
def bsy_md5_sign_post(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    if encrypt is None:
        return ''
    sign = ''
    cid = ''
    for param in params:
        if param['name'] == 'sign':
            sign = param['value']
        if param['name'] == 'cid':
            cid = param['value']
    h = MD5.new()
    h.update(b'%s%s%s' % (cid.encode('utf8', errors='ignore'), sign.encode('utf8', errors='ignore'), encrypt['function'](
        json.dumps(body['content'], ensure_ascii=False), encrypt['key'], encrypt['iv'], encrypt['mode']).encode('utf8', errors='ignore')))
    return h.hexdigest()


# 比搜益加签GET方法
def bsy_md5_sign_get(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    if encrypt is None:
        return ''
    sign = ''
    cid = ''
    for param in params:
        if param['name'] == 'sign':
            sign = param['value']
        if param['name'] == 'cid':
            cid = param['value']
    h = MD5.new()
    h.update(b'%s%s%s' % (cid.encode('utf8', errors='ignore'), sign.encode('utf8', errors='ignore'), quote_plus(encrypt['function'](
        json.dumps(body['content'], ensure_ascii=False), encrypt['key'], encrypt['iv'], encrypt['mode'])).encode('utf8', errors='ignore')))
    return h.hexdigest()


# 网贷天眼加签方法
def wdty_md5_sign(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    body_list = body['data'].split('&')
    body = ''
    for row in sorted(body_list):
        body += '{}&'.format(row)
    body = body[:-1]
    h = MD5.new()
    h.update(b'%s' % body.encode('utf8', errors='ignore'))
    return h.hexdigest()


# 希财网加签方法
def xc_md5_sign(body, params, encrypt):
    timestamp = ''
    client_secret = ''
    for param in params:
        if param['name'] == 'timestamp':
            timestamp = param['value']
        if param['name'] == 'client_secret':
            client_secret = param['value']
    t = MD5.new()
    t.update(b'%s' % timestamp.encode('utf8', errors='ignore'))
    h = MD5.new()
    h.update(b'%s%s' % (t.hexdigest().encode('utf8', errors='ignore'), client_secret.encode('utf8', errors='ignore')))
    return h.hexdigest()


# 返利网加签方法
def flw_md5_sign(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    shop_no = ''
    shop_key = ''
    for param in params:
        if param['name'] == 'shop_no':
            shop_no = param['value']
        if param['name'] == 'shop_key':
            shop_key = param['value']
    code = 'begin_date={}&end_date={}&code={}{}'.format(body['begin_date'], body['end_date'], shop_no, shop_key)
    t = MD5.new()
    t.update(b'%s' % code.encode('utf8', errors='ignore'))
    return t.hexdigest()


# 投呗加签方法
def tb_md5_sign(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    org_secret = ''
    for param in params:
        if param['name'] == 'org_secret':
            org_secret = param['value']
    body.pop('sign')
    s = org_secret
    for k in sorted(body):
        s += '%s%s' % (k, body[k])
    s += org_secret
    t = MD5.new()
    t.update(b'%s' % s.encode('utf8', errors='ignore'))
    return t.hexdigest().upper()


# 互金明镜加签方法
def hj_md5_sign(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    key = ''
    for param in params:
        if param['name'] == 'key':
            key = param['value']
    body.pop('sign')
    s = '{"version":"%s","optype":"%s","timestamp":"%s","merchant":"%s"}%s' % (
        body['version'], body['optype'], body['timestamp'], body['merchant'], key)
    t = MD5.new()
    t.update(b'%s' % s.encode('utf8', errors='ignore'))
    return t.hexdigest().lower()


# 响巢看看加签方法
def kk_md5_sign(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    merchantKey = ''
    for param in params:
        if param['name'] == 'merchantKey':
            merchantKey = param['value']
    body.pop('sign')
    s = ''
    for k in sorted(body):
        s += '%s%s' % (k, body[k])
    s += merchantKey
    t = MD5.new()
    t.update(b'%s' % s.encode('utf8', errors='ignore'))
    return t.hexdigest()


# 响巢看看加签方法, 着陆页跳转
def kk_zly_md5_sign(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    signKey = ''
    for param in params:
        if param['name'] == 'signKey':
            signKey = param['value']
    body.pop('sign')
    s = 'xluserid=%s&time=%s' % (body['xluserid'], body['time'])
    s += signKey
    t = MD5.new()
    t.update(b'%s' % s.encode('utf8', errors='ignore'))
    return t.hexdigest()


# 生菜网接口加签
def scw_md5_sign(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    if encrypt is None:
        return ''
    secretKey = ''
    for param in params:
        if param['name'] == 'secretKey':
            secretKey = param['value']
    if 'userpwd' in body.keys():
        body['userpwd'] = encrypt['function'](body['userpwd'], encrypt['key'], encrypt['iv'], encrypt['mode'])
    body.pop('sign')
    s = ''
    for k in sorted(body):
        s += '%s%s' % (k, body[k])
    s += secretKey
    t = MD5.new()
    t.update(b'%s' % s.encode('utf8', errors='ignore'))
    return t.hexdigest()


# 通用加签方式一, 格式: p1v1p2p2p3v3signKey
def public_md5_sign_one(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    signKey = ''
    for param in params:
        if param['name'] == 'signKey':
            signKey = param['value']
    body.pop('sign')
    s = ''
    for k in sorted(body):
        s += '%s%s' % (k, body[k])
    s += signKey
    t = MD5.new()
    t.update(b'%s' % s.encode('utf8', errors='ignore'))
    return t.hexdigest()


# 通用加签方式二, 格式: signKeyp1v1p2p2p3v3
def public_md5_sign_two(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    signKey = ''
    for param in params:
        if param['name'] == 'signKey':
            signKey = param['value']
    body.pop('sign')
    s = signKey
    for k in sorted(body):
        s += '%s%s' % (k, body[k])
    t = MD5.new()
    t.update(b'%s' % s.encode('utf8', errors='ignore'))
    return t.hexdigest()


# 通用加签方式三, 格式: signKeyp1v1p2p2p3v3signKey
def public_md5_sign_three(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    signKey = ''
    for param in params:
        if param['name'] == 'signKey':
            signKey = param['value']
    body.pop('sign')
    s = signKey
    for k in sorted(body):
        s += '%s%s' % (k, body[k])
    s += signKey
    t = MD5.new()
    t.update(b'%s' % s.encode('utf8', errors='ignore'))
    return t.hexdigest()


# 互金协会加签
def hjxh_md5_sign(body, params, encrypt):
    if not isinstance(body, dict):
        return ''
    s = ''
    for param in params:
        if param['type'] == 'String':
            s += '{}{}'.format(param['name'], param['value'])
    s += 'name{}idNumber{}'.format(body['name'], body['idNumber'])
    t = MD5.new()
    t.update(b'%s' % s.encode('utf8', errors='ignore'))
    return t.hexdigest()


# 存管加签
def cg_md5_sign(body, params, encrypt):
    if not isinstance(body, dict):
        return body
    rft_key = ''
    rft_secret = ''
    for param in params:
        if param['name'] == 'rft_key':
            rft_key = param['value']
        if param['name'] == 'rft_secret':
            rft_secret = param['value']
    try:
        body = body['data'] if isinstance(body['data'], dict) else json.loads(body['data'])
    except Exception as e:
        pass
    body.pop('sign')
    serial = cg_body_sort(body)
    key = '{}{}'.format(rft_key, rft_secret)
    t = MD5.new()
    t.update(b'%s' % key.encode('utf8', errors='ignore'))
    signValue = '{}{}'.format(serial, t.hexdigest())
    t = MD5.new()
    t.update(b'%s' % signValue.encode('utf8', errors='ignore'))
    return t.hexdigest()


# 存管参数序列化
def cg_body_sort(body):
    if isinstance(body, str):
        return body
    elif isinstance(body, dict):
        param = ''
        for line in sorted(body, key=lambda x:x.keys() if isinstance(x, dict) else x):
            param += '{}={}&'.format(line, cg_body_sort(body[line]))
        return param[:-1]
    elif isinstance(body, list):
        param = ''
        for line in sorted(body, key=lambda x:x.keys() if isinstance(x, dict) else x):
            param += '{}&'.format(cg_body_sort(line))
        return param[:-1]
    else:
        return body