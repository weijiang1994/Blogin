"""
coding:utf-8
file: photo.py
@time: 2024/10/5 0:09
@desc:
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from blogin.models import Photo
from blogin.api.decorators import get_params, check_permission
from blogin.responses import R


api_photo_bp = Blueprint('api_photo_bp', __name__, url_prefix='/api/photo')


@api_photo_bp.route('/list', methods=['GET'])
@get_params(
    params=['page', 'limit', 'name', 'level'],
    types=[int, int, str, str],
    remove_none=True
)
@jwt_required
@check_permission
def photo_list(page=1, limit=12, name='', level=None):
    query = (Photo.id > 0,)

    if name:
        query += (Photo.title.contains(name),)

    if level is not None:
        query += (Photo.level == level,)

    photos = Photo.query.filter(
        *query
    ).order_by(
        Photo.create_time.desc()
    ).paginate(
        per_page=limit,
        page=page,
    )

    data = []
    for photo in photos.items:
        item = photo.to_dict()
        item['tags'] = [tag.name for tag in photo.tags]
        item['comments'] = len(photo.comments)
        item['likes'] = len(photo.likes)
        item['url'] = photo.url(small=True)
        data.append(item)

    return R.success(
        total=photos.total,
        data=data
    )


@api_photo_bp.route('/origin-image', methods=['GET'])
@jwt_required
@check_permission
def origin_image():
    photo_id = request.args.get('id')
    photo = Photo.query.get(photo_id)
    if not photo:
        return R.not_found()

    return R.success(
        url=photo.url(small=False)
    )


@api_photo_bp.route('/detail/<int:photo_id>', methods=['GET'])
@jwt_required
@check_permission
def photo_detail(photo_id):
    photo = Photo.query.get(photo_id)
    if not photo:
        return R.not_found()

    item = photo.to_dict()
    item['tags'] = [tag.name for tag in photo.tags]
    item['comments'] = len(photo.comments)
    item['likes'] = len(photo.likes)
    item['url'] = photo.url(small=True)

    return R.success(
        data=item
    )


@api_photo_bp.route('/edit', methods=['POST'])
@jwt_required
@check_permission
def photo_edit():
    data = request.json
    photo_id = data.get('id')
    title = data.get('title')
    level = data.get('level')
    tags = data.get('tags')
    description = data.get('description')

    photo = Photo.query.get(photo_id)
    if not photo:
        return R.not_found(msg='照片不存在')
    photo.update(
        title=title,
        level=level,
        description=description,
    )
    photo.update_tags(tags)
    return R.success()


@api_photo_bp.route('add', methods=['POST'])
@jwt_required
@check_permission
def photo_add():
    title = request.form.get('title')
    level = request.form.get('level')
    tags = request.form.get('tags')
    description = request.form.get('description')
    photo = Photo(
        title=title,
        level=level,
        description=description,
        save_path='',
        save_path_s=''
    )
    photo.save_photo(request.files.get('file'), current_user.id)
    photo.update_tags(tags.split(','))
    return R.success(msg='相片添加成功')
