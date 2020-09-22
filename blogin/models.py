"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : models
@Software: PyCharm
"""
from datetime import datetime

from blogin.extension import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='user id', autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False, comment='user name')
    email = db.Column(db.String(40), unique=True, nullable=False, comment='user register email')
    password = db.Column(db.String(40), nullable=False, comment='user password')
    website = db.Column(db.String(128), comment='user owner website', default='""')
    avatar = db.Column(db.String(128), nullable=False, comment='user avatar')
    confirm = db.Column(db.INTEGER, nullable=False, default=0)
    role_id = db.Column(db.INTEGER, db.ForeignKey('role.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    role = db.relationship('Role', backref=db.backref('user', lazy='dynamic'))

    def __repr__(self):
        return 'username<%s> email<%s> website<%s>' % (self.username, self.email, self.website)


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='role id', autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True, comment='role name')
    permission = db.Column(db.String(50), nullable=False, unique=True)


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
    delete_flag = db.Column(db.INTEGER, nullable=False, default=0, comment='is delete? 0:no 1:yes')

    blog_types = db.relationship('BlogType', back_populates='blogs')

    def __repr__(self):
        return '<title> %s <introduce> %s <content> %s' % (self.title, self.introduce, self.content)


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
