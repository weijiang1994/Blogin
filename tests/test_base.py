"""
# coding:utf-8
@Time    : 2020/12/30
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : test_base.py
@Desc    : test_front_blog
@Software: PyCharm
"""
import os

os.environ['GITHUB_CLIENT_ID'] = 'test'
os.environ['GITHUB_CLIENT_SECRET'] = 'test'
os.environ['SECRET_KEY'] = 'test'
import unittest
from blogin import create_app
from flask import url_for
from blogin.extension import db
from blogin.models import User, Role


class TestBase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        db.create_all()
        Role.init_role()
        super_user = User(username='Admin', email='804022023@qq.com', password='12345678', confirm=1,
                          avatar='/static/img/admin/admin.jpg')
        super_user.set_password('12345678')

        user = User(username='User', email='913538009@qq.com', password='12345678', confirm=1)
        user.set_password('12345678')

        unconfirm_user = User(username='UnconfirmedUser', email='1019467408@qq.com', password='12345678', confirm=1)
        unconfirm_user.set_password('12345678')
        db.session.add_all([super_user, user, unconfirm_user])
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()
        self.context.app()

    def login(self, usr_email=None, password=None):
        if usr_email is None and password is None:
            usr_email = 'Admin'
            password = '12345678'
        return self.client.post(url_for('auth_bp.login'), data=dict(usr_email=usr_email,
                                                                    password=password), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth_bp.logout'), follow_redirects=True)
