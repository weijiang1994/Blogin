"""
# coding:utf-8
Miscellaneous models: Soul, Timeline, FriendLink, One, OneSentence, MessageBorder.
"""
from datetime import datetime

from blogin.extension import db
from blogin.models.core import States


class Soul(db.Model):
    __tablename__ = 'soul'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    hits = db.Column(db.String(300), nullable=False, default=1)


class Timeline(db.Model):
    __tablename__ = 'timeline'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    abandon = db.Column(db.INTEGER, default=0, comment='0 activate 1 abandon')


class FriendLink(db.Model):
    __tablename__ = 'friend_link'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False)
    link = db.Column(db.String(40), nullable=False)
    desc = db.Column(db.String(40), default='')
    timestamp = db.Column(db.DateTime, default=datetime.now)
    flag = db.Column(db.INTEGER, db.ForeignKey('states.id'))

    status = db.relationship(States, back_populates='flink')


class One(db.Model):
    __tablename__ = 'one'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    content = db.Column(db.String(512), nullable=False, default='')


class OneSentence(db.Model):
    __tablename__ = 'one_sentence'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    content = db.Column(db.String(512), default='', nullable=False)
    day = db.Column(db.DATE, default=datetime.today)


class MessageBorder(db.Model):
    __tablename__ = 'msg_border'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    parent_id = db.Column(db.INTEGER, default=0)
    body = db.Column(db.TEXT, nullable=False)
    timestamps = db.Column(db.DateTime, default=datetime.now)
    flag = db.Column(db.INTEGER, default=0, comment='is it not effect?')
    plain_text = db.Column(db.TEXT, nullable=False)
    msg_user = db.relationship('User', back_populates='msg_border')
