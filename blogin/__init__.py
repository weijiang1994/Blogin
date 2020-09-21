"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : __init__.py
@Software: PyCharm
"""
from flask import Flask
from blogin.extension import db, bootstrap, moment, ckeditor


def create_app():
    app = Flask()
    register_extension(app)
    return app


def register_extension(app: Flask):
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)

