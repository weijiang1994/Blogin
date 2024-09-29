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


@api_index_bp.route('/traffic', methods=['GET'])
@jwt_required
def get_recent_7days_traffics():
    days = []
    result = []
    vst_data = []
    cst_data = []
    lst_data = []
    td = datetime.date.today()
    vsts = VisitStatistics.query.filter(VisitStatistics.date > td - timedelta(days=7)).all()
    csts = CommentStatistics.query.filter(CommentStatistics.date > td - timedelta(days=7)).all()
    lsts = LikeStatistics.query.filter(LikeStatistics.date > td - timedelta(days=7)).all()
    for vst in vsts:
        days.append(str(vst.date))
        vst_data.append(vst.times)
    for cst in csts:
        cst_data.append(cst.times)
    for lst in lsts:
        lst_data.append(lst.times)

    result.append(vst_data)
    result.append(cst_data)
    result.append(lst_data)
    return R.success(data={'result': result, 'days': days})
