"""
# coding:utf-8
Core infrastructure models: States, Role, ThirdParty.
"""
from datetime import datetime

from blogin.extension import db


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


class ThirdParty(db.Model):
    __tablename__ = 'third_party'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    user = db.relationship('User', back_populates='third_party', cascade='all')

    @staticmethod
    def init_tp():
        tp = ThirdParty(name='default')
        db.session.add(tp)
        tp = ThirdParty(name='github')
        db.session.add(tp)
        tp = ThirdParty(name='weibo')
        db.session.add(tp)
        tp = ThirdParty(name='qq')
        db.session.add(tp)
        db.session.commit()
