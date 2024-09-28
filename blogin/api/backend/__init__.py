"""
coding:utf-8
file: __init__.py.py
@time: 2024/9/17 0:21
@desc:
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required

from blogin.api.decorators import get_params
from blogin.models import Blog, User, BlogComment, VisitStatistics
from blogin.responses import R

api_index_bp = Blueprint('api_index_bp', __name__, url_prefix='/api/index')


@api_index_bp.route('/overview', methods=['GET'])
@jwt_required
def overview():
    blog_count = Blog.query.count()
    user_count = User.query.count()
    comment_count = BlogComment.query.count()
    visit_count = VisitStatistics.query.first().times
    return R.success(
        data=dict(
            blog_count=blog_count,
            user_count=user_count,
            comment_count=comment_count,
            visit_count=visit_count
        )
    )
