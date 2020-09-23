"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : setting
@Software: PyCharm
"""
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Operators:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'


class BaseConfig:

    # Paginate configure
    BLOGIN_BLOG_PER_PAGE = 10
    BLOGIN_COMMENT_PER_PAGE = 10
    BLOGIN_PHOTO_PER_PAGE = 12
    SECRET_KEY = os.getenv('SECRET_KEY')

    # CKEditor configure
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_HEIGHT = 500
    # CKEDITOR_CODE_THEME = 'docco'
    CKEDITOR_CODE_THEME = 'monokai'
    CKEDITOR_FILE_UPLOADER = 'be_blog_bp.upload'

    BLOGIN_UPLOAD_PATH = os.path.join(basedir, 'uploads')

    # SQL configure
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Mail configure
    BLOGIN_EMAIL_PRE = '[Blogin.] '
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Blogin Admin', MAIL_USERNAME)


class DevelopmentConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1994124@127.0.0.1/blog?charset=utf8'
    REDIS_URL = "redis://localhost"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
