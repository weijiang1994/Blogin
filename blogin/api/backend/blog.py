"""
coding:utf-8
file: blog.py
@time: 2024/9/22 23:32
@desc:
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from blogin.models import Blog, BlogType, States
from blogin.responses import R
from blogin.api.decorators import check_permission, get_params
from blogin.utils import config_ini

blog_bp = Blueprint('blog_backend_bp', __name__, url_prefix='/api/blog')


@blog_bp.errorhandler(404)
def page_not_found(e):
    return R.not_found()


@blog_bp.route('/list', methods=['GET'])
@get_params(
    params=['page', 'status', 'keyword'],
    types=[int, int, str],
)
@jwt_required
@check_permission
def blog_list(page, status=0, keyword=''):
    query = (Blog.id > 0,)

    if status:
        query += (Blog.delete_flag == status,)

    if keyword:
        query += (Blog.title.contains(keyword),)
        query += (Blog.content.contains(keyword),)

    blogs = Blog.query.filter(
        *query
    ).paginate(
        per_page=10,
        page=page,
    )

    return R.success(
        data=[blog.to_dict(special_col={'pre_img': lambda x: config_ini.get('server', 'host') + x}) for blog in
              blogs.items],
        has_next=blogs.has_next,
        has_prev=blogs.has_prev,
        page=page,
        total=blogs.total,
    )


@blog_bp.route('/blog/delete/<blog_id>', methods=['POST'])
@jwt_required
@check_permission
def delete(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    state = States.query.get_or_404(2)
    blog.state = state
    db.session.commit()
    return R.success(msg='博客删除成功')


@blog_bp.route('/blog/recover/<blog_id>', methods=['POST'])
@jwt_required
@check_permission
def recover(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    state = States.query.get_or_404(1)
    blog.state = state
    db.session.commit()
    return R.success(msg='博客恢复成功')


@blog_bp.route('/blog/category/add', methods=['POST'])
@get_params(
    params=['name', 'desc'],
    types=[str, str]
)
@jwt_required
@check_permission
def blog_category_add(name, desc):
    if BlogType.query.filter_by(name=name).first():
        return R.error(msg='分类已存在')
    cate = BlogType(name=category_name, description=desc)
    db.session.add(cate)
    db.session.commit()
    return R.success(msg='添加成功')
