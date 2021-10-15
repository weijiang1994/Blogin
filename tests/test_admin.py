"""
# coding:utf-8
@Time    : 2020/12/31
@Author  : jiangwei
@File    : test_admin.py
@Desc    : 测试后台管理页面功能
@Software: PyCharm
"""
from tests.test_base import TestBase
from flask import url_for
from datetime import date
import io
from blogin.setting import basedir


class TestAdmin(TestBase):

    def setUp(self):
        super(TestAdmin, self).setUp()
        self.login(usr_email='Admin', password='12345678')

    def test_admin_index(self):
        res = self.client.get(url_for('index_bp_be.index'))
        data = res.get_data(as_text=True)
        self.assertIn('网站今日流量统计', data)

    def test_bad_permission(self):
        # 未登录的用户打开后台页面
        self.logout()
        res = self.client.get(url_for('index_bp_be.index'), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertNotIn('后台', data)
        self.assertIn('用户登录', data)

        # 普通权限用户打开后台页面
        self.login(usr_email='User', password='12345678')
        res = self.client.get(url_for('index_bp_be.index'), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn("FORBIDDEN!YOU DON'T HAVE PERMISSION", data)
        self.assertEqual(res.status_code, 403)

    def test_visit_statistic(self):
        # 测试获取最近七天访问数据
        res = self.client.post(url_for('index_bp_be.get_recent_7days_traffics'))
        data = res.get_data(as_text=True)
        self.assertIn('days', data)

    def test_create_blog(self):
        # 测试发布博客页面get方式
        data, res = self.get_res_data('be_blog_bp.blog_create')
        self.assertIn('发布博客', data)
        # 测试发布博客内容post方式
        params = {'blog_img_file': (io.BytesIO(b"abcdef"), 'test.jpg'),
                  'title': '测试博客',
                  'blog_type': 1,
                  'blog_level': 1,
                  'brief_content': '登鹳雀楼',
                  'body': '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。'}
        data, res = self.post_res_data('be_blog_bp.blog_create',
                                       para=params, content_type='multipart/form-data')
        self.assertIn('测试博客', data)
        self.assertIn('登鹳雀楼', data)
        self.assertEqual(res.status_code, 200)

    def test_edit_blog(self):
        # 测试博客编辑列表页面
        data, res = self.get_res_data('be_blog_bp.blog_edit')
        self.assertIn('test1', data)
        self.assertIn('test2', data)
        self.assertIn('test3', data)

    def test_edit_blog_content(self):
        # 测试内容编辑页面get方式
        res = self.client.get(url_for('be_blog_bp.blog_content_edit', blog_id=1))
        data = res.get_data(as_text=True)
        self.assertIn('Blog test1 contents.', data)
        # 测试提交编辑博客内容post方式
        res = self.client.post(url_for('be_blog_bp.blog_content_edit', blog_id=1),
                               data=dict(
                                   body='Edit blog1 content.',
                                   title='edit test1',
                                   blog_type=1,
                                   brief_content='edit blog1 introduce',
                                   blog_img_file=(io.BytesIO(b'asfasfa'), 'test1.jpg')),
                               follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('Edit blog1 content.', data)
        self.assertIn('edit test1', data)
        self.assertIn('edit blog1 introduce', data)

    def test_add_category(self):
        # 新增存在的类别
        data, res = self.post_res_data(endpoint='be_blog_bp.blog_category_add',
                                       para={'name': 'Test', 'desc': 'Test category.'})
        self.assertIn('"is_exists":true', data)
        # 新增不存在的类别
        data, res = self.post_res_data(endpoint='be_blog_bp.blog_category_add',
                                       para={'name': 'Test2', 'desc': 'Test category.'})
        self.assertIn('"is_exists":false', data)

    def test_delete_blog(self):
        res = self.client.get(url_for('be_blog_bp.delete', blog_id=1), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('博客删除成功', data)

    def test_recover_blog(self):
        res = self.client.get(url_for('be_blog_bp.recover', blog_id=1), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('博客恢复成功', data)

    def test_add_photo(self):
        # 测试添加相片页面get
        data, res = self.get_res_data(endpoint='be_photo_bp.add_photo')
        self.assertIn('相片标题', data)
        # 测试添加相片页面post
        data, res = self.post_res_data(endpoint='be_photo_bp.add_photo',
                           data={
                               'tags': 'tag1 tag2 tag3',
                               'photo_title': 'test-photo',
                               'photo_desc': 'test photo desc',
                               'img_file': (io.BytesIO(b'1234567'), 'test-photo.jpg')})
        self.assertIn('相片添加完成', data)
        self.assertIn('test-photo', data)
        self.assertEqual(res.status_code, 200)

    def test_edit_photo(self):
        data, res = self.get_res_data(endpoint='be_photo_bp.photo_edit')
        self.assertIn('test photo1', data)
        self.assertIn('test photo1 description', data)

    def test_photo_private(self):
        res = self.client.get(url_for('be_photo_bp.private', photo_id=1), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('设为私密照片成功', data)

    def test_photo_non_private(self):
        res = self.client.get(url_for('be_photo_bp.non_private', photo_id=1), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('设为公开照片成功', data)

    def test_edit_photo_info(self):
        # 测试编辑相片信息页面,获取原始相片信息
        res = self.client.get(url_for('be_photo_bp.info_edit', photo_id=1))
        data = res.get_data(as_text=True)
        # 测试编辑相片信息页面,修改相片信息并提交保存
        self.assertIn('test photo1 description', data)
        data = {'photo_title': 'edit photo title', 'photo_desc': 'edit photo description'}
        res = self.client.post(url_for('be_photo_bp.info_edit', photo_id=1), data=data, follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('edit photo title', data)
        self.assertIn('edit photo description', data)

    def test_user_manage_index(self):
        data, res = self.get_res_data(endpoint='user_m_bp.index')
        self.assertIn('User', data)
        self.assertIn('Admin', data)
        self.assertIn('UnconfirmedUser', data)

    def test_set_admin(self):
        res = self.client.get(url_for('user_m_bp.set_admin', user_id=1), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('操作成功', data)

    def test_set_user(self):
        # 测试超级号
        res = self.client.get(url_for('user_m_bp.set_user', user_id=1), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('禁止操作', data)

        # 测试普通号
        res = self.client.get(url_for('user_m_bp.set_user', user_id=2), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('操作成功', data)

    def test_lock(self):
        # 锁定超级号
        res = self.client.get(url_for('user_m_bp.lock', user_id=1), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('禁止操作', data)

        # 锁定普通号
        res = self.client.get(url_for('user_m_bp.lock', user_id=2), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertIn('操作成功', data)
