"""
coding:utf-8
file: contents.py
@time: 2024/10/7 23:08
@desc:
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from blogin.api.decorators import get_params, check_permission
from blogin.models import OneSentence, Poem, Poet, Dynasty, SongCiAuthor, SongCi, Soul
from blogin.responses import R


api_contents_bp = Blueprint('api_contents_bp', __name__, url_prefix='/api/contents')


@api_contents_bp.route('/one-word/list', methods=['GET'])
@jwt_required
@check_permission
def one_word_list():
    keyword = request.args.get('content')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    query = (OneSentence.id > 0,)
    if keyword:
        query += (OneSentence.content.contains(keyword),)
    one_words = OneSentence.query.filter(
        *query
    ).order_by(
        OneSentence.day.desc()
    ).paginate(
        per_page=limit,
        page=page
    )
    data = []
    for one_word in one_words.items:
        item = one_word.to_dict()
        data.append(item)
    return R.success(
        total=one_words.total,
        data=data
    )


@api_contents_bp.route('/djt/list', methods=['GET'])
@jwt_required
@check_permission
def djt_list():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    keyword = request.args.get('content')

    query = (Soul.id > 0,)

    if keyword:
        query += (Soul.content.contains(keyword),)

    souls = Soul.query.filter(
        *query
    ).order_by(
        Soul.hits.desc()
    ).paginate(
        per_page=limit,
        page=page
    )
    return R.success(
        total=souls.total,
        data=[soul.to_dict() for soul in souls.items]
    )
