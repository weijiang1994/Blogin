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
from blogin.setting import basedir
import os
from blogin.blueprint.front import blog_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    prefix = 'sqlite:////'
    app = Flask('blogin')
    app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(basedir, 'data-dev.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extension(app)
    register_blueprint(app)

    return app


def register_extension(app: Flask):
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)


def register_blueprint(app: Flask):
    app.register_blueprint(blog_bp)
