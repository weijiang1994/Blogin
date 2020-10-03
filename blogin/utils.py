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
import jieba
import wordcloud as wc

from blogin.extension import db
from blogin.setting import basedir
from imageio import imread

IP_QUERY = "http://ip-api.com/json/{}?lang=zh-CN&fields=status,message,country,region,regionName,city,lat,lon,query"
OCR_URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/'
OCR_TOKEN = '24.487f3dbf8ba5259be2f7b321741f02cf.2592000.1604024498.282335-22776145'
OCR_HEADERS = {'content-type': 'application/x-www-form-urlencoded'}
OCR_CATEGORY = {'文字识别': 'accurate_basic', '身份证识别': 'idcard', '银行卡识别': 'bankcard',
                '驾驶证识别': 'driving_license', '车牌识别': 'license_plate'}
BANK_CARD_TYPE = {0: '不能识别', 1: '借记卡', 2: '信用卡'}
LANGUAGE = {'中文': 'zh-CN', '英文': 'en', '日语': 'ja', '法语': 'fr', '俄语': 'ru'}
IP_REG = '((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))'


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


def allow_txt_file(filename):
    suffix = filename.split('.')[0]
    if suffix != 'txt':
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
        res = response.json()
        nums = res.get("words_result_num")
        texts = ''
        for text in res.get('words_result'):
            texts += text.get('words') + '\n'
        return nums, texts

    def ocr_idcard(self):
        response = requests.post(self.url, data={"id_card_side": "front", "image": self.img}, headers=OCR_HEADERS)
        res = response.json()
        nums = res.get('words_result_num')
        texts = ''
        results = res.get('words_result')
        texts += '姓名:' + results.get('姓名').get('words') + '\n'
        texts += '民族:' + results.get('民族').get('words') + '\n'
        texts += '住址:' + results.get('住址').get('words') + '\n'
        texts += '出生:' + results.get('出生').get('words') + '\n'
        texts += '公民身份号码:' + results.get('公民身份号码').get('words') + '\n'
        texts += '性别:' + results.get('性别').get('words') + '\n'
        return nums, texts

    def ocr_bankcard(self):
        response = requests.post(self.url, data={"image": self.img}, headers=OCR_HEADERS)
        res = response.json()
        card_num = res.get('result').get('bank_card_number')
        validate_date = res.get('result').get('valid_date')
        card_type = BANK_CARD_TYPE.get(res.get('result').get('bank_card_type'))
        bank_name = res.get('result').get('bank_name')
        return 4, '卡号: ' + card_num + '\n' + '有效日期: ' + validate_date + \
               '\n' + '卡种: ' + card_type + '\n' + '所属行: ' + bank_name

    def ocr_drive_card(self):
        response = requests.post(self.url, data={"image": self.img}, headers=OCR_HEADERS)
        res = response.json()
        nums = res.get('words_result_num')
        results = res.get('words_result')
        number = results.get('证号').get('words')
        validate_date = results.get('有效期限').get('words')
        car_type = results.get('准驾车型').get('words')
        # start_date = results.get('有效起始日期').get('words')
        addr = results.get('住址').get('words')
        name = results.get('姓名').get('words')
        country = results.get('国籍').get('words')
        birth = results.get('出生日期').get('words')
        gender = results.get('性别').get('words')
        get_time = results.get('初次领证日期').get('words')

        return nums, '证号: ' + number + '\n' + '有效期限: ' + validate_date + '\n' + '准驾车型: ' + car_type + '\n' + \
               '住址: ' + addr + '\n' + '姓名: ' + name + '\n' + \
               '国籍: ' + country + '\n' + '出生日期: ' + birth + '\n' + '性别: ' + gender + '\n' + '初次领证日期: ' \
               + get_time

    def ocr_license_plate(self):
        response = requests.post(self.url, data={"image": self.img}, headers=OCR_HEADERS)
        res = response.json()
        color = res.get('words_result').get('color')
        number = res.get('words_result').get('number')

        return 0, '车牌颜色: ' + color + '\n' + '车牌号码: ' + number


class IPQuery:
    def __init__(self, ip, lang='zh-CN'):
        self.ip = ip
        self.lang = LANGUAGE.get(lang)
        self.url = "http://ip-api.com/json/{}?lang={}&fields=status,continent,continentCode,isp,zip,message,timezone," \
                   "country,region,regionName,city,lat,lon,query"

    def query(self):
        if self.ip == '127.0.0.1':
            return '本地IP'
        response = requests.get(self.url.format(self.ip, self.lang))
        response = response.text
        response = json.loads(response)
        if response['status'] == 'fail':
            return '查询失败'
        return [response['country'], response['regionName'], response['city'], response['continent'],
                response['continentCode'], response['isp'], response['timezone'], response['lat'], response['lon']]


class WordCloud:
    def __init__(self, txt=None, img=None):
        self.txt = txt
        self.img = img
        self.words = None

    def cut(self):
        self.words = jieba.cut(self.txt)
        self.words = ' '.join(self.words)

    def generate(self):
        try:
            mask = imread(self.img)
            self.cut()
            w = wc.WordCloud(font_path="simkai.ttf", mask=mask, width=1000, height=700, background_color="white",
                             max_words=20)
            w.generate(self.words)
            w.to_file(basedir + '/uploads/wordcloud/word-cloud.jpg')
            return basedir + '/uploads/wordcloud/word-cloud.jpg'
        except:
            import traceback
            traceback.format_exc()
            return False
