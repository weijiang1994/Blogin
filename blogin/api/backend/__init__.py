"""
coding:utf-8
file: __init__.py.py
@time: 2024/9/17 0:21
@desc:
"""
import datetime
from datetime import timedelta

from flask import Blueprint
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.sql.expression import func

from blogin.api.decorators import get_params, check_permission
from blogin.models import Blog, User, BlogComment, VisitStatistics, CommentStatistics, LikeStatistics, Photo, LikePhoto
from blogin.responses import R

api_index_bp = Blueprint('api_index_bp', __name__, url_prefix='/api/index')


@api_index_bp.route('/overview', methods=['GET'])
@jwt_required
@check_permission
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
@check_permission
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


@api_index_bp.route('/top', methods=['GET'])
@jwt_required
@check_permission
def top():
    blogs = Blog.query.order_by(Blog.read_times.desc()).limit(5)
    photoes = Photo.query.join(
        LikePhoto,
        LikePhoto.img_id == Photo.id
    ).group_by(
        LikePhoto.img_id
    ).order_by(func.COUNT(LikePhoto.img_id)).with_entities(
        Photo.id, Photo.title, Photo.create_time, func.COUNT(LikePhoto.img_id).label('like_times')
    ).limit(5)
    return R.success(data=dict(
        blogs=[dict(
            title=blog.title,
            count=blog.read_times,
            created_at=blog.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        ) for blog in blogs],
        photoes=[dict(
            title=photo.title,
            like_times=photo.like_times,
            created_at=photo.create_time.strftime('%Y-%m-%m %H:%M:%S'),
        ) for photo in photoes]))


@api_index_bp.route('/rate', methods=['GET'])
@jwt_required
@check_permission
def rate():
    blog_count = Blog.query.count()
    comment_count = BlogComment.query.count()
    photo_count = Photo.query.count()
    return R.success(
        data=[
            dict(value=blog_count, name='博客'),
            dict(value=comment_count, name='评论'),
            dict(value=photo_count, name='图片')
        ]
    )


@api_index_bp.route('/recent', methods=['GET'])
@jwt_required
@check_permission
def recent():
    blogs = Blog.query.order_by(Blog.create_time.desc()).limit(10)
    photoes = Photo.query.order_by(Photo.create_time.desc()).limit(6)
    return R.success(
        data=dict(
            blogs=[dict(
                id=blog.id,
                title=blog.title,
                created_at=blog.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            ) for blog in blogs],
            photoes=[dict(
                id=photo.id,
                url=photo.url(),
                created_at=photo.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            ) for photo in photoes]
        )
    )


@api_index_bp.route('/user/info', methods=['GET'])
@jwt_required
@check_permission
def user_info():
    user = User.query.filter(User.id == current_user.id).first()
    return R.success(
        data=dict(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            avatar=user.url_for_avatar()
        )
    )
