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

IP_QUERY = "http://ip-api.com/json/{}?lang=zh-CN&fields=status,message,country,region,regionName,city,lat,lon,query"


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

