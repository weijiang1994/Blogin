"""
# coding:utf-8
@Time    : 2020/10/12
@Author  : jiangwei
@File    : wsgi
@Software: PyCharm
"""
from blogin import create_app

app = create_app('production')
