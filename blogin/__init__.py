"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@File    : __init__.py
@Software: PyCharm
"""
import atexit
import platform
import logging
from logging.handlers import RotatingFileHandler
import os

from flask_cors import CORS
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from blogin.commands import register_cmd
from blogin.extension import db, bootstrap, moment, ckeditor, migrate, login_manager, share, avatar, mail, whooshee, \
    oauth, aps, cache, babel, jwt
from blogin.monitor import start_monitor_thread
from blogin.setting import basedir
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
from blogin.blueprint.front.msg_border import msg_border_bp
from blogin.setting import config
from blogin.models import User, Role, BlogType, Blog
from blogin.utils import split_space, super_split, conv_list, is_empty, config_ini, BOOTSTRAP_SUFFIX, read_config
from blogin import task
from blogin.api import register_restful_api


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'production')
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

    @babel.localeselector
    def get_language():
        from flask import request
        cookie = request.cookies.get('local-language') or 'zh'
        if cookie in ['zh', 'en']:
            return cookie

        return request.accept_languages.best_match(app.config.get('BABEL_DEFAULT_LOCALE'))

    @app.context_processor
    def inject_stage_and_region():
        light_theme = read_config().get('base', 'light_theme')
        dark_theme = read_config().get('base', 'dark_theme')
        return dict(light=light_theme + BOOTSTRAP_SUFFIX, dark=dark_theme + BOOTSTRAP_SUFFIX)

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
    babel.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    CORS(app)
    if config_ini.getboolean('base', 'scheduler'):
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
        except Exception:
            app.logger.debug('Scheduler already running, skipping init.')

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
        except Exception:
            app.logger.debug('Scheduler already running, skipping init.')

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except Exception:
                pass

        atexit.register(_unlock_file)


# 注册蓝图
def register_blueprint(app: Flask):
    register_restful_api(app)
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
    app.register_blueprint(msg_border_bp)


def register_log(app: Flask):
    app.logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(basedir + '/logs/blogin.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    if not app.debug:
        app.logger.addHandler(file_handler)
