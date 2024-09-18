"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@File    : extension
@Software: PyCharm
"""
import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_share import Share
from flask_avatars import Avatars
from flask_mail import Mail
from flask_whooshee import Whooshee
from flask_oauthlib.client import OAuth
from flask_apscheduler import APScheduler
import redis
from flask_caching import Cache
from flask_babel import Babel
from flask_jwt_extended import JWTManager

jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
ckeditor = CKEditor()
login_manager = LoginManager()
share = Share()
avatar = Avatars()
mail = Mail()
whooshee = Whooshee()
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
rd = redis.Redis(connection_pool=pool)
oauth = OAuth()
aps = APScheduler()
cache = Cache()
babel = Babel()


@login_manager.user_loader
def load_user(user_id):
    from blogin.models import User
    user = User.query.filter_by(id=user_id).first()
    return user


login_manager.login_view = 'auth_bp.login'
login_manager.login_message = u'请先登陆!'
login_manager.login_message_category = 'danger'