"""
# coding:utf-8
@Time    : 2020/12/30
@Author  : jiangwei
@File    : test_user_blog.py
@Desc    : test_user_blog
@Software: PyCharm
"""
from tests.test_base import TestBase
from flask import url_for


class TestUserBlog(TestBase):

    def setUp(self):
        super(TestUserBlog, self).setUp()
        self.login(usr_email='User', password='12345678')

    # 测试普通用户是否有后台管理权限
    def test_user_index_page(self):
        response = self.client.get(url_for('blog_bp.index'))
        data = response.get_data(as_text=True)
        self.assertNotIn('后台管理', data)

