"""
coding:utf-8
file: index.py
@time: 2024/9/18 0:05
@desc:
"""
from flask import Blueprint, request

from blogin.responses import R
from blogin.models import Blog
from blogin.api.decorators import get_params

index_bp = Blueprint('index_bp', __name__, url_prefix='/api')


@index_bp.route('/index', methods=['GET'])
@get_params(
    params=['page'],
    types=[int],
)
def index(page):
    paginations = Blog.query.filter(Blog.delete_flag == 1).paginate(
        per_page=10,
        page=page,
    )
    blogs = paginations.items
    return R.success(
        blogs=[blog.to_dict(special_col={'pre_img': lambda x: 'http://localhost:5000' + x}) for blog in blogs],
        has_next=paginations.has_next,
        has_prev=paginations.has_prev,
        page=page,
        total=paginations.total,
    )
