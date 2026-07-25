"""
# coding:utf-8
Blog-related models.
"""
import os
from datetime import datetime, date

from flask import current_app

from blogin.extension import db, whooshee
from blogin.models.mixins import Mixin, TimeMixin
from blogin.utils import basedir, generate_thumbnail, create_path


class BlogType(db.Model, Mixin):
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


@whooshee.register_model('title', 'content', 'introduce')
class Blog(db.Model, Mixin):
    __tablename__ = 'blog'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='blog id', autoincrement=True)
    title = db.Column(db.String(200), nullable=False, comment='blog title', index=True)
    type_id = db.Column(db.INTEGER, db.ForeignKey('blog_type.id'))
    pre_img = db.Column(db.String(200), nullable=False, comment='blog preview image')
    introduce = db.Column(db.String(255), nullable=False, comment='blog introduce text', index=True)
    content = db.Column(db.TEXT, nullable=False, comment='blog content')
    is_private = db.Column(db.INTEGER, nullable=False, default=0, comment='is private? 0:no 1:yes')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    read_times = db.Column(db.INTEGER, default=0)
    delete_flag = db.Column(db.INTEGER, db.ForeignKey('states.id'))
    is_top = db.Column(db.INTEGER, default=0, comment='is it set top?')

    blog_types = db.relationship('BlogType', back_populates='blogs')
    comments = db.relationship('BlogComment', back_populates='blog', cascade='all')
    state = db.relationship('States', back_populates='blog')
    blog_history = db.relationship('BlogHistory', back_populates='blog', cascade='all')
    banner = db.relationship('BlogBanner', back_populates='blog', cascade='all')

    def __repr__(self):
        return '<title> %s <introduce> %s' % (self.title, self.introduce)


class BlogComment(db.Model, Mixin):
    __tablename__ = 'blog_comment'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    parent_id = db.Column(db.INTEGER)

    replied_id = db.Column(db.INTEGER, db.ForeignKey('blog_comment.id'))
    author_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    blog_id = db.Column(db.INTEGER, db.ForeignKey('blog.id'))
    delete_flag = db.Column(db.INTEGER, default=0, comment='this comment delete flag 0 no 1 yes')

    blog = db.relationship('Blog', back_populates='comments')
    author = db.relationship('User', back_populates='blog_comments')
    replies = db.relationship('BlogComment', back_populates='replied', cascade='all')
    replied = db.relationship('BlogComment', back_populates='replies', remote_side=[id])


class BlogHistory(db.Model):
    __tablename__ = 'blog_history'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    blog_id = db.Column(db.INTEGER, db.ForeignKey('blog.id'))
    save_path = db.Column(db.String(100), nullable=False)
    timestamps = db.Column(db.DateTime, default=datetime.now)

    blog = db.relationship('Blog', back_populates='blog_history')


class BlogBanner(db.Model, Mixin, TimeMixin):
    __tablename__ = 'blog_banner'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    blog_id = db.Column(db.INTEGER, db.ForeignKey('blog.id'))

    blog = db.relationship('Blog', back_populates='banner')


class PostContent(db.Model):
    __tablename__ = 'post_content'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    content = db.Column(db.VARCHAR(500), default='', comment='')
    post_id = db.Column(db.INTEGER)


class DraftBlog(db.Model):
    __tablename__ = 'draft'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False, comment='blog title')
    content = db.Column(db.Text, nullable=False)
    timestamps = db.Column(db.DateTime, default=datetime.now)
    brief = db.Column(db.String(512), default='', comment='blog brief introduce')
    tag = db.Column(db.INTEGER, default=1, comment='is is draft? 0: no 1: yes')


class Contribute(db.Model):
    __tablename__ = 'contribute'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='table id')
    date = db.Column(db.DATE, default=datetime.today, comment='contribute date')
    contribute_counts = db.Column(db.INTEGER, default=0)

    con_detail = db.relationship('ContributeDetail', back_populates='cont', cascade='all')


class ContributeDetail(db.Model):
    __tablename__ = 'contribute_detail'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    cont_id = db.Column(db.INTEGER, db.ForeignKey('contribute.id'))
    timestamps = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(256), default='', nullable=False)
    detail_link = db.Column(db.String(256), default='', nullable=False)

    cont = db.relationship('Contribute', back_populates='con_detail')


class Plan(db.Model):
    __tablename__ = 'plan'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='table id')
    title = db.Column(db.String(50), nullable=False)
    total = db.Column(db.INTEGER, nullable=False)
    done_count = db.Column(db.INTEGER, nullable=False, default=0)
    is_done = db.Column(db.INTEGER, default=0, nullable=False)
    timestamps = db.Column(db.DATE, default=datetime.today)
    done_time = db.Column(db.DATE)


class LoveMe(db.Model):
    __tablename__ = 'loveme'

    id = db.Column(db.INTEGER, primary_key=True, comment='primary key id')
    counts = db.Column(db.INTEGER, nullable=False, default=0)


class LoveInfo(db.Model):
    __tablename__ = 'love_info'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user = db.Column(db.String(200), default='')
    user_ip = db.Column(db.String(30), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)


def update_contribution():
    td = date.today()
    con = Contribute.query.filter_by(date=td).first()
    if con:
        con.contribute_counts += 1
