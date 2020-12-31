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
from blogin.models import User, Role, States, ThirdParty, BlogType, Blog, Photo


class TestBase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        # 数据库初始化操作
        db.drop_all()
        db.create_all()
        Role.init_role()
        States.init_states()
        ThirdParty.init_tp()
        bt = BlogType(name='Test', description='test type')
        blog1 = Blog(title='test1', content='Blog test1 contents.', introduce='blog1 introduce',
                     type_id=1, pre_img='test.jpg', delete_flag=1)
        blog2 = Blog(title='test2', content='Blog test2 contents.', introduce='blog2 introduce', type_id=1,
                     pre_img='test.jpg', delete_flag=1)
        blog3 = Blog(title='test3', content='Blog test3 contents.', introduce='blog3 introduce', type_id=1,
                     pre_img='test.jpg', delete_flag=1)

        ph1 = Photo(title='test photo1', description='test photo1 description',
              save_path='/test/save/', save_path_s='/test/save/', level=1)

        super_user = User(username='Admin', email='804022023@qq.com', password='12345678', confirm=1,
                          avatar='/static/img/admin/admin.jpg')
        super_user.set_password('12345678')

        user = User(username='User', email='913538009@qq.com', password='12345678', confirm=1)
        user.set_password('12345678')

        unconfirm_user = User(username='UnconfirmedUser', email='1019467408@qq.com', password='12345678', confirm=1)
        unconfirm_user.set_password('12345678')
        db.session.add_all([super_user, user, unconfirm_user, bt, blog1, blog2, blog3, ph1])
        db.session.commit()

    def tearDown(self):
        # 结束清除数据，结束上下文环境
        db.drop_all()
        self.context.pop()

    def login(self, usr_email=None, password=None):
        if usr_email is None and password is None:
            usr_email = 'Admin'
            password = '12345678'
        return self.client.post(url_for('auth_bp.login'), data=dict(usr_email=usr_email,
                                                                    password=password), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth_bp.logout'), follow_redirects=True)

    def get_res_data(self, endpoint, follow_redirects=True):
        res = self.client.get(url_for(endpoint), follow_redirects=follow_redirects)
        data = res.get_data(as_text=True)
        return data, res

    def post_res_data(self, endpoint, para=None, follow_redirects=True, **kwargs):
        if para:
            res = self.client.post(url_for(endpoint), data=para, follow_redirects=follow_redirects, **kwargs)
        else:
            res = self.client.post(url_for(endpoint), follow_redirects=follow_redirects, **kwargs)
        data = res.get_data(as_text=True)
        return data, res
