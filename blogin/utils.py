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


def get_current_time():
    """
    get the current time with yy-mm-dd hh:mm:ss format
    :return: the current time
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)