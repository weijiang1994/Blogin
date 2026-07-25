"""
# coding:utf-8
Photo gallery models.
"""
import os
from datetime import datetime
from urllib.parse import urljoin

from flask import current_app
from werkzeug.utils import secure_filename

from blogin.extension import db, whooshee
from blogin.models.mixins import Mixin
from blogin.utils import config_ini, basedir, generate_thumbnail, create_path


tagging = db.Table('tagging',
                   db.Column('photo_id', db.INTEGER, db.ForeignKey('photo.id')),
                   db.Column('tag_id', db.INTEGER, db.ForeignKey('tag.id')))


@whooshee.register_model('name')
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    photos = db.relationship('Photo', secondary=tagging, back_populates='tags')


@whooshee.register_model('title', 'description')
class Photo(db.Model, Mixin):
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

    def url(self, small=False):
        """
        获取图片的url

        :param small: 是否获取缩略图
        :return:
        """
        base_url = config_ini.get('server', 'host')
        if small:
            return urljoin(base_url, self.save_path_s)
        return urljoin(base_url, self.save_path)

    def update_tags(self, tags):
        """
        更新图片的标签

        :param tags: list
        :return:
        """
        self.tags = []
        for tag in tags:
            t = Tag.query.filter_by(name=tag).first()
            if t is None:
                t = Tag(name=tag)
            self.tags.append(t)
        self.save()

    def save_photo(self, file, user_id):
        """
        保存图片

        :param user_id: 用户ID
        :param file: FileStorage 上传的文件
        :return:
        """
        img_file = str(user_id) + '_' + secure_filename(file.filename)
        folder = str(datetime.now()).split(' ')[0]
        create_path(basedir + '/uploads/gallery/' + folder)
        file.save(basedir + '/uploads/gallery/' + folder + '/' + img_file)

        if os.path.getsize(basedir + '/uploads/gallery/' + folder + '/' + img_file) > \
                current_app.config.get('PHOTO_NEED_RESIZE'):
            small_img = generate_thumbnail(basedir + '/uploads/gallery/' + folder + '/' + img_file)
            small_img.save(basedir + '/uploads/gallery/' + folder + '/' + 'small' + img_file)
            small_path = '/gallery/' + folder + '/' + 'small' + img_file
        else:
            small_path = '/gallery/' + folder + '/' + img_file

        img_path = '/gallery/' + folder + '/' + img_file
        self.save_path = img_path
        self.save_path_s = small_path
        self.save()


class PhotoComment(db.Model, Mixin):
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


class LikePhoto(db.Model):
    __tablename__ = 'like_photo'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    img_id = db.Column(db.INTEGER, db.ForeignKey('photo.id'))
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    photo = db.relationship('Photo', back_populates='likes')
    user = db.relationship('User', back_populates='likes')
