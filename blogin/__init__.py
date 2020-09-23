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
import click
from blogin.extension import db, bootstrap, moment, ckeditor, migrate, login_manager, share
from blogin.setting import basedir
import os
from blogin.blueprint.front.blog_bp import blog_bp
from blogin.blueprint.backend.blog_bp import be_blog_bp
from blogin.blueprint.backend.photo_bp import be_photo_bp
from blogin.setting import config
from blogin.models import *


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('blogin')
    app.config.from_object(config[config_name])
    register_extension(app)
    register_blueprint(app)
    register_cmd(app)
    error_execute(app)
    shell_handler(app)

    return app


def shell_handler(app: Flask):
    @app.shell_context_processor
    def shell():
        return dict(db=db, User=User, Role=Role, BlogType=BlogType, Blog=Blog)


# 错误请求页面处理
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


# 注册flask拓展
def register_extension(app: Flask):
    migrate.init_app(app, db)
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    share.init_app(app)


# 注册蓝图
def register_blueprint(app: Flask):
    app.register_blueprint(blog_bp)
    app.register_blueprint(be_blog_bp)
    app.register_blueprint(be_photo_bp)


def register_cmd(app: Flask):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Drop database and create a new database')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def init():
        """Initialized Blogin"""
        click.echo('Initializing the database...')
        db.drop_all()
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()

        click.echo('Done.')

    @app.cli.command()
    def admin():
        try:
            db.drop_all()
            db.create_all()
            Role.init_role()
            ad = Role.query.filter_by(name='ADMIN').first()
            username = input('请输入超级管理员用户名:')
            email = input('请输入超级管理员邮箱:')
            pwd = input('请输入超级管理员密码:')
            confirm = input('请确认密码:')
            if pwd != confirm:
                click.echo('两次密码不一致')
                click.echo('退出当前操作')
                return
            super_user = User(username=username, email=email, password=pwd, confirm=1,
                              avatar='/static/img/admin/admin.jpg',
                              role_id=ad.id)
            db.session.add(super_user)
            db.session.commit()
            click.echo('超级管理员创建成功!')
            click.echo('程序退出...')
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            click.echo('操作出现异常,退出...')
