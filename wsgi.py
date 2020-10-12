"""
# coding:utf-8
@Time    : 2020/10/12
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : wsgi
@Software: PyCharm
"""
from blogin import create_app

blogin = create_app('production')
