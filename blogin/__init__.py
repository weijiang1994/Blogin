"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : __init__.py
@Software: PyCharm
"""
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from blogin.extension import db, bootstrap, moment, ckeditor, migrate
from blogin.setting import basedir
import os
from blogin.blueprint.front.blog_bp import blog_bp
from blogin.blueprint.backend.blog_bp import be_blog_bp
from blogin.setting import config
from blogin.models import *


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('blogin')
    app.config.from_object(config[config_name])
    register_extension(app)
    register_blueprint(app)
    error_execute(app)
    shell_handler(app)

    return app


def shell_handler(app: Flask):
    @app.shell_context_processor
    def shell():
        return dict(db=db, User=User, Role=Role, BlogType=BlogType, Blog=Blog)


def error_execute(app: Flask):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('error/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('error/400.html', description=e.description), 500


def register_extension(app: Flask):
    migrate.init_app(app, db)
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)


def register_blueprint(app: Flask):
    app.register_blueprint(blog_bp)
    app.register_blueprint(be_blog_bp)
