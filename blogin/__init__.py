"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : __init__.py
@Software: PyCharm
"""
import atexit
import platform
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
import click
from blogin.extension import db, bootstrap, moment, ckeditor, migrate, login_manager, share, avatar, mail, whooshee, \
    oauth, aps
from blogin.monitor import start_monitor_thread
from blogin.setting import basedir
import os
from blogin.blueprint.front.blog import blog_bp
from blogin.blueprint.backend.blog_bp import be_blog_bp
from blogin.blueprint.backend.photo_bp import be_photo_bp
from blogin.blueprint.backend.account_manage_bp import user_m_bp
from blogin.blueprint.backend.other_bp import other_bp
from blogin.blueprint.backend.index_bp import index_bp_be
from blogin.blueprint.front.auth import auth_bp
from blogin.blueprint.front.accounts import accounts_bp
from blogin.blueprint.front.gallery import gallery_bp
from blogin.blueprint.front.tool import tool_bp
from blogin.blueprint.front.soul import soul_bp
from blogin.blueprint.front.api import api_bp
from blogin.blueprint.front.oauth import oauth_bp
from blogin.blueprint.front.rss import rss_bp
from blogin.setting import config
from blogin.models import *
from blogin.utils import split_space, super_split, conv_list, is_empty
from blogin import task
import logging


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('blogin')
    app.jinja_env.filters['split'] = split_space
    app.jinja_env.filters['ssplit'] = super_split
    app.jinja_env.filters['slist'] = conv_list
    app.jinja_env.filters['isempty'] = is_empty
    app.config.from_object(config[config_name])
    app.config['SCHEDULER_API_ENABLED'] = True
    register_extension(app)
    register_blueprint(app)
    register_cmd(app)
    error_execute(app)
    shell_handler(app)
    register_log(app)

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
    db.app = app
    bootstrap.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    share.init_app(app)
    avatar.init_app(app)
    mail.init_app(app)
    mail.app = app
    whooshee.init_app(app)
    oauth.init_app(app)
    scheduler_init(app)


def scheduler_init(app):
    """
    保证系统只启动一次定时任务
    :param app: 当前flask实例
    :return: None
    """
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open(basedir + '/scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            aps.init_app(app)
            aps.start()
            app.logger.debug('Scheduler Started,---------------')
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)
    else:
        msvcrt = __import__('msvcrt')
        f = open(basedir + 'scheduler.lock', 'wb')
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            aps.init_app(app)
            aps.start()
            app.logger.debug('Scheduler Started,----------------')
        except:
            pass

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

        atexit.register(_unlock_file)


# 注册蓝图
def register_blueprint(app: Flask):
    app.register_blueprint(blog_bp)
    app.register_blueprint(be_blog_bp)
    app.register_blueprint(be_photo_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(tool_bp)
    app.register_blueprint(user_m_bp)
    app.register_blueprint(other_bp)
    app.register_blueprint(index_bp_be)
    app.register_blueprint(soul_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(rss_bp)


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
            States.init_states()
            ThirdParty.init_tp()
            username = input('请输入超级管理员用户名:')
            email = input('请输入超级管理员邮箱:')
            pwd = input('请输入超级管理员密码:')
            confirm = input('请确认密码:')
            if pwd != confirm:
                click.echo('两次密码不一致')
                click.echo('退出当前操作')
                return

            super_user = User(username=username, email=email, password=pwd, confirm=1,
                              avatar='/static/img/admin/admin.jpg')
            super_user.set_password(pwd)
            db.session.add(super_user)
            db.session.commit()
            click.echo('超级管理员创建成功!')
            click.echo('应用初始化成功!')
            click.echo('程序退出...')
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            click.echo('操作出现异常,退出...')

    @app.cli.command()
    def addtp():
        print('添加第三方登录方式')
        third_party_name = input('请输入第三方登录方式:')
        tp = ThirdParty(name=third_party_name)
        db.session.add(tp)
        db.session.commit()
        print('添加成功')

    @app.cli.command()
    def archive():
        blogs = Blog.query.filter_by(delete_flag=1).order_by(Blog.create_time.desc()).all()
        archives = {}
        for blog in blogs:
            current_year = blog.create_time.year
            current_month = blog.create_time.month
            # 如果当前年份不存在,那么当前月份也不存在
            if not archives.get(current_year):
                # 记录当前年份以及当前月份
                archives[current_year] = {current_month: []}
                archives.get(current_year).get(current_month).append([blog.id, blog.title,
                                                                      str(blog.create_time).split(' ')[0][5:]])
            else:
                # 如果当前年份存在,月份不存在,则更新一条数据到当前年份中
                if not archives.get(current_year).get(current_month):
                    archives.get(current_year).update({current_month: []})
                    archives.get(current_year).get(current_month).append([blog.id, blog.title,
                                                                          str(blog.create_time).split(' ')[0][5:]])
                else:
                    # 年月都存在则直接将数据拼接到后面
                    archives.get(current_year).get(current_month).append([blog.id, blog.title,
                                                                          str(blog.create_time).split(' ')[0][5:]])


def register_log(app: Flask):
    app.logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(basedir + '/logs/blogin.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    if not app.debug:
        app.logger.addHandler(file_handler)
