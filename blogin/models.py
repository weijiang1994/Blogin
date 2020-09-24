"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : models
@Software: PyCharm
"""
from datetime import datetime
from flask_avatars import Identicon
from blogin.extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
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

    roles = db.relationship('Role', back_populates='users')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_avatar()
        self.set_role()

    def __repr__(self):
        return 'username<%s> email<%s> website<%s>' % (self.username, self.email, self.website)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def generate_avatar(self):
        icon = Identicon()
        files = icon.generate(self.username)
        self.avatar = '/accounts/avatar/' + files[2]
        db.session.commit()

    def set_role(self):
        if self.roles is None:
            if self.email == '804022023@qq.com' or self.email == 'weijiang1994_1@qq.com':
                self.roles = Role.query.filter_by(name='ADMIN').first()
            else:
                self.roles = Role.query.filter_by(name='USER').first()
            db.session.commit()


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='role id', autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True, comment='role name')
    permission = db.Column(db.String(50), nullable=False, unique=True)

    users = db.relationship('User', back_populates='roles')

    @staticmethod
    def init_role():
        admin = Role(name='ADMIN', permission='ANY')
        db.session.add(admin)
        usr = Role(name='USER', permission='SOME')
        db.session.add(usr)
        db.session.commit()


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='blog id', autoincrement=True)
    title = db.Column(db.String(300), nullable=False, comment='blog title')
    type_id = db.Column(db.INTEGER, db.ForeignKey('blog_type.id'))
    pre_img = db.Column(db.String(200), nullable=False, comment='blog preview image')
    introduce = db.Column(db.String(300), nullable=False, comment='blog introduce text')
    content = db.Column(db.TEXT, nullable=False, comment='blog content')
    is_private = db.Column(db.INTEGER, nullable=False, default=0, comment='is private? 0:no 1:yes')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    read_times = db.Column(db.INTEGER, default=0)
    delete_flag = db.Column(db.INTEGER, nullable=False, default=0, comment='is delete? 0:no 1:yes')

    blog_types = db.relationship('BlogType', back_populates='blogs')

    def __repr__(self):
        return '<title> %s <introduce> %s' % (self.title, self.introduce)


class BlogType(db.Model):
    __tablename__ = 'blog_type'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='blog type id', autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False, comment='blog type name')
    counts = db.Column(db.INTEGER, nullable=False, default=0, comment='this type blog counts')
    description = db.Column(db.String(300), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    blogs = db.relationship('Blog', back_populates='blog_types')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<name> %s <description> %s' % (self.name, self.description)


class Photo(db.Model):
    __tablename__ = 'photo'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='photo id', autoincrement=True)
    title = db.Column(db.String(40), nullable=False, comment='photo title', default='""')
    description = db.Column(db.String(300), nullable=False, comment='photo description', default='""')
    save_path = db.Column(db.String(200), nullable=False, comment='photo save path')
    create_time = db.Column(db.DateTime, default=datetime.now)


class LoveMe(db.Model):
    __tablename__ ='loveme'

    id = db.Column(db.INTEGER, primary_key=True, comment='primary key id')
    counts = db.Column(db.INTEGER, nullable=False, default=0)


class LoveInfo(db.Model):
    __tablename__ = 'love_info'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user = db.Column(db.String(200), default='')
    user_ip = db.Column(db.String(30), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
