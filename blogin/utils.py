"""
# coding:utf-8
@Time    : 2020/9/23
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : utils
@Software: PyCharm
"""
import datetime
import os

import json
import requests
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from blogin import db

IP_QUERY = "http://ip-api.com/json/{}?lang=zh-CN&fields=status,message,country,region,regionName,city,lat,lon,query"


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


def get_current_time():
    """
    get the current time with yy-mm-dd hh:mm:ss format
    :return: the current time
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_ip_real_add(ip):
    response = requests.get(IP_QUERY.format(ip))
    response = response.text
    response = json.loads(response)
    if response['status'] == 'fail':
        return '定位失败'
    return response['country'], response['city']


def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    print(s.dumps(data))
    return s.dumps(data)


def validate_token(user, token, operation, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False
    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == Operations.CONFIRM:
        user.confirm=1
    else:
        user.set_password(new_password)
    db.session.commit()

    return True


def generate_ver_code():
    import random
    return random.randint(134299, 873242)


def split_space(string):
    return str(string).split()
