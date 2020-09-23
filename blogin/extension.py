"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : extension
@Software: PyCharm
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_share import Share

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
ckeditor = CKEditor()
login_manager = LoginManager()
share = Share()


@login_manager.user_loader
def load_user(user_id):
    from blogin.models import User
    user = User.query.filter_by(id=user_id)
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message = u'请先登陆后在进行操作'
login_manager.login_message_category = 'info'
