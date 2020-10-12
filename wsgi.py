"""
# coding:utf-8
@Time    : 2020/10/12
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : wsgi
@Software: PyCharm
"""
from blogin import create_app
import os

print(os.getenv('DATABASE_PWD'))
app = create_app('production')
