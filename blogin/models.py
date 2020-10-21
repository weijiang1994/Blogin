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
from blogin.extension import db, whooshee
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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
    status = db.Column(db.INTEGER, db.ForeignKey('states.id'), default=1)

    roles = db.relationship('Role', back_populates='users')
    photo_comments = db.relationship('PhotoComment', back_populates='author', cascade='all')
    login_logs = db.relationship('LoginLog', back_populates='user', cascade='all')
    blog_comments = db.relationship('BlogComment', back_populates='author', cascade='all')
    likes = db.relationship('LikePhoto', back_populates='user', cascade='all')
    statuses = db.relationship('States', back_populates='user')

    receive_notify = db.relationship('Notification', back_populates='receive_user', cascade='all')

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


class LoginLog(db.Model):
    __tablename__ = 'login_log'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, comment='login record')
    timestamp = db.Column(db.DateTime, default=datetime.now)
    login_addr = db.Column(db.String(100), default='')
    real_addr = db.Column(db.String(100), default='')
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='login_logs')


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


@whooshee.register_model('title', 'content', 'introduce')
class Blog(db.Model):
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

    blog_types = db.relationship('BlogType', back_populates='blogs')
    comments = db.relationship('BlogComment', back_populates='blog', cascade='all')
    state = db.relationship('States', back_populates='blog')

    def __repr__(self):
        return '<title> %s <introduce> %s' % (self.title, self.introduce)


class BlogComment(db.Model):
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


class States(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    blog = db.relationship('Blog', back_populates='state')
    user = db.relationship('User', back_populates='statuses')
    flink = db.relationship('FriendLink', back_populates='status')

    @staticmethod
    def init_states():
        s1 = States(name='正常')
        s2 = States(name='禁用')
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()


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


tagging = db.Table('tagging',
                   db.Column('photo_id', db.INTEGER, db.ForeignKey('photo.id')),
                   db.Column('tag_id', db.INTEGER, db.ForeignKey('tag.id')))


@whooshee.register_model('title', 'description')
class Photo(db.Model):
    __tablename__ = 'photo'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, comment='photo id', autoincrement=True)
    title = db.Column(db.String(40), nullable=False, comment='photo title', default='""')
    description = db.Column(db.String(300), nullable=False, comment='photo description', default='""')
    save_path = db.Column(db.String(200), nullable=False, comment='photo save path')
    save_path_s = db.Column(db.String(200), nullable=False, comment='small size')
    create_time = db.Column(db.DateTime, default=datetime.now)
    level = db.Column(db.INTEGER, default=0)
    tags = db.relationship('Tag', secondary=tagging, back_populates='photos')
    comments = db.relationship('PhotoComment', back_populates='photo', cascade='all')
    likes = db.relationship('LikePhoto', back_populates='photo', cascade='all')


@whooshee.register_model('name')
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    photos = db.relationship('Photo', secondary=tagging, back_populates='tags')


class PhotoComment(db.Model):
    __tablename__ = 'photo_comment'

    id = db.Column(db.INTEGER, primary_key=True)
    body = db.Column(db.String(400))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

    parent_id = db.Column(db.INTEGER)
    replied_id = db.Column(db.INTEGER, db.ForeignKey('photo_comment.id'))
    author_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    photo_id = db.Column(db.INTEGER, db.ForeignKey('photo.id'))
    delete_flag = db.Column(db.INTEGER, default=0, comment='this comment delete flag 0 no 1 yes')

    photo = db.relationship('Photo', back_populates='comments')
    author = db.relationship('User', back_populates='photo_comments')
    replies = db.relationship('PhotoComment', back_populates='replied', cascade='all')
    replied = db.relationship('PhotoComment', back_populates='replies', remote_side=[id])


class LoveMe(db.Model):
    __tablename__ = 'loveme'

    id = db.Column(db.INTEGER, primary_key=True, comment='primary key id')
    counts = db.Column(db.INTEGER, nullable=False, default=0)


class LoveInfo(db.Model):
    __tablename__ = 'love_info'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user = db.Column(db.String(200), default='')
    user_ip = db.Column(db.String(30), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())


class LikePhoto(db.Model):
    __tablename__ = 'like_photo'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    img_id = db.Column(db.INTEGER, db.ForeignKey('photo.id'))
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    photo = db.relationship('Photo', back_populates='likes')
    user = db.relationship('User', back_populates='likes')


class VerifyCode(db.Model):
    __tablename__ = 'ver_code'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER)
    code = db.Column(db.INTEGER)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_retire = db.Column(db.BOOLEAN)


class Timeline(db.Model):
    __tablename__ = 'timeline'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    abandon = db.Column(db.INTEGER, default=0, comment='0 activate 1 abandon')


class VisitStatistics(db.Model):
    __tablename__ = 'visit_statistics'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    times = db.Column(db.INTEGER, default=1)


class CommentStatistics(db.Model):
    __tablename__ = 'comment_statistics'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    times = db.Column(db.INTEGER, default=1)


class LikeStatistics(db.Model):
    __tablename__ = 'like_statistics'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    times = db.Column(db.INTEGER, default=1)


class FriendLink(db.Model):
    __tablename__ = 'friend_link'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False)
    link = db.Column(db.String(40), nullable=False)
    desc = db.Column(db.String(40), default='')
    timestamp = db.Column(db.DateTime, default=datetime.now)
    flag = db.Column(db.INTEGER, db.ForeignKey('states.id'))

    status = db.relationship(States, back_populates='flink')


class Soul(db.Model):
    __tablename__ = 'soul'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    hits = db.Column(db.String(300), nullable=False, default=1)
