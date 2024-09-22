"""
coding:utf-8
file: blog.py
@time: 2024/9/22 23:32
@desc:
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from blogin.models import Blog
from blogin.responses import R
from blogin.api.decorators import check_permission, get_params
from blogin.utils import config_ini

blog_bp = Blueprint('blog_backend_bp', __name__, url_prefix='/api/blog')


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
        data=[blog.to_dict(special_col={'pre_img': lambda x: config_ini.get('server', 'host') + x}) for blog in blogs.items],
        has_next=blogs.has_next,
        has_prev=blogs.has_prev,
        page=page,
        total=blogs.total,
    )