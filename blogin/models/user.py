"""
# coding:utf-8
User-related models: User, LoginLog, Notification, VerifyCode.
"""
from datetime import datetime
from urllib.parse import urljoin

from flask_avatars import Identicon
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from blogin.extension import db
from blogin.models.mixins import Mixin
from blogin.models.core import Role
from blogin.utils import config_ini


class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    type = db.Column(db.INTEGER, default=0, comment='notification type 0 blog 1 photo')
    target_id = db.Column(db.INTEGER)
    target_name = db.Column(db.String(200))
    send_user = db.Column(db.String(40))
    receive_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    msg = db.Column(db.String(400))
    read = db.Column(db.INTEGER, default=0, comment='is readed? 0 no 1 yes')
    timestamp = db.Column(db.DateTime, default=datetime.now)

    receive_user = db.relationship('User', back_populates='receive_notify')


class User(db.Model, UserMixin, Mixin):
    __tablename__ = 'user'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='user id', autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False, comment='user name')
    email = db.Column(db.String(40), unique=True, nullable=False, comment='user register email')
    password = db.Column(db.String(128), nullable=False, comment='user password')
    website = db.Column(db.String(128), comment='user owner website', default='')
    avatar = db.Column(db.String(128), nullable=False, comment='user avatar')
    confirm = db.Column(db.INTEGER, nullable=False, default=0)
    role_id = db.Column(db.INTEGER, db.ForeignKey('role.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    slogan = db.Column(db.String(200), default='')
    recent_login = db.Column(db.DateTime, default=datetime.now)
    received_email_tag = db.Column(db.INTEGER, default=1, comment='receive email notify')
    status = db.Column(db.INTEGER, db.ForeignKey('states.id'), default=1)
    reg_way = db.Column(db.INTEGER, db.ForeignKey('third_party.id'), default=1)

    roles = db.relationship('Role', back_populates='users')
    photo_comments = db.relationship('PhotoComment', back_populates='author', cascade='all')
    login_logs = db.relationship('LoginLog', back_populates='user', cascade='all')
    blog_comments = db.relationship('BlogComment', back_populates='author', cascade='all')
    likes = db.relationship('LikePhoto', back_populates='user', cascade='all')
    statuses = db.relationship('States', back_populates='user')
    third_party = db.relationship('ThirdParty', back_populates='user')

    receive_notify = db.relationship('Notification', back_populates='receive_user', cascade='all')
    msg_border = db.relationship('MessageBorder', back_populates='msg_user', cascade='all')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self._generate_avatar()
        self._set_default_role()

    def __repr__(self):
        return 'username<%s> email<%s> website<%s>' % (self.username, self.email, self.website)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def _generate_avatar(self):
        """Generate avatar file and set the avatar path (does not commit)."""
        icon = Identicon()
        files = icon.generate(self.username)
        self.avatar = '/accounts/avatar/' + files[2]

    def generate_avatar(self):
        """Regenerate avatar and persist the change."""
        self._generate_avatar()
        db.session.commit()

    def _set_default_role(self):
        """Assign the default USER role (does not commit)."""
        self.roles = Role.query.filter_by(name='USER').first()

    def set_role(self):
        """Assign default USER role and persist."""
        self._set_default_role()
        db.session.commit()

    def set_admin(self):
        self.roles = Role.query.filter_by(name='ADMIN').first()
        db.session.commit()

    def url_for_avatar(self):
        return urljoin(config_ini.get('server', 'host'), self.avatar)

    def info(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'website': self.website,
            'avatar': self.url_for_avatar(),
            'slogan': self.slogan,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'recent_login': self.recent_login.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'role': self.roles.name
        }


class LoginLog(db.Model):
    __tablename__ = 'login_log'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='login record')
    timestamp = db.Column(db.DateTime, default=datetime.now)
    login_addr = db.Column(db.String(100), default='')
    real_addr = db.Column(db.String(100), default='')
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='login_logs')


class VerifyCode(db.Model):
    __tablename__ = 'ver_code'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    code = db.Column(db.INTEGER)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_retire = db.Column(db.BOOLEAN)
