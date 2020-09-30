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
from urllib.parse import urlparse, urljoin
import base64
import requests
from flask import current_app, request, redirect, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from blogin import db

IP_QUERY = "http://ip-api.com/json/{}?lang=zh-CN&fields=status,message,country,region,regionName,city,lat,lon,query"
OCR_URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/'
OCR_TOKEN = '24.487f3dbf8ba5259be2f7b321741f02cf.2592000.1604024498.282335-22776145'
OCR_HEADERS = {'content-type': 'application/x-www-form-urlencoded'}
OCR_CATEGORY = {'文字识别': 'accurate_basic'}


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
    if ip == '127.0.0.1':
        return '本地IP'
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
        user.confirm = 1
    else:
        user.set_password(new_password)
    db.session.commit()

    return True


def generate_ver_code():
    import random
    return random.randint(134299, 873242)


def split_space(string):
    return str(string).split()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog_bp.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allow_img_file(filename):
    suffix = filename.split('.')[0]
    if suffix not in ['jpg', 'png', 'jpeg']:
        return False
    return True


class OCR:
    def __init__(self, filename, category='accurate_basic'):
        self.filename = filename
        self.category = category
        self.url = None
        self.img = None
        self.set_url()
        self.set_img()

    def set_url(self):
        self.url = OCR_URL + OCR_CATEGORY.get(self.category) + "?access_token=" + OCR_TOKEN

    def set_img(self):
        with open(self.filename, 'rb') as f:
            self.img = base64.b64encode(f.read())

    def ocr(self):
        response = requests.post(self.url, data={"image": self.img}, headers=OCR_HEADERS)
        return response.json()
