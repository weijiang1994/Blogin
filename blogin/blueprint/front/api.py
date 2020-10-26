"""
# coding:utf-8
@Time    : 2020/10/26
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : api
@Software: PyCharm
"""
from flask import Blueprint, request, jsonify, render_template
from blogin.models import Soul, Blog, Poem, Poet, SongCi, SongCiAuthor
from sqlalchemy.sql.expression import func

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')


@api_bp.route('/introduce/')
def api_introduce():
    blog = Blog.query.filter_by(title='API介绍').first()
    return render_template("main/api/apiIntroduce.html", blog=blog)


@api_bp.route('/get-soul/')
def get_soul():
    counts = request.args.get('counts', 1)
    if counts == 'all':
        souls = Soul.query.all()
    else:
        souls = Soul.query.order_by(func.random()).limit(int(counts))
    result = {'result': [], 'code': 200}
    for soul in souls:
        ls = {'title': soul.title, 'hits': soul.hits}
        result.get('result').append(ls)
    return jsonify(result)


# 唐宋诗相关API
# 随机获取唐宋诗词
@api_bp.route('/get-ts-poem/')
def get_tang_poem():
    counts = request.args.get('counts', 1, type=int)
    if counts > 50:
        return jsonify({'code': 400, 'info': 'counts参数过大，请输入小于50的正数!'})
    poems = Poem.query.order_by(func.random()).limit(counts)
    result = {'result': [], 'code': 200, 'counts': counts}
    for poem in poems:
        ls = {'title': poem.title, 'content': poem.content, 'author': poem.poets.dynasties.name + '·' + poem.poets.name,
              'id': poem.id}
        result.get('result').append(ls)
    return jsonify(result)


# 根据作者名获取诗
@api_bp.route('/get-ts-poem/poet/')
def get_poet_poem():
    poet = request.args.get('author')
    counts = request.args.get('counts', 1)
    if poet is None:
        return jsonify({'code': 400, 'info': '参数无效！'})
    result = {'result': [], 'code': 200, 'counts': counts}
    db_poet = Poet.query.filter_by(name=poet).first()
    if db_poet is None:
        return jsonify({'code': 200, 'info': '未找到相关诗人！'})
    if counts == 'all':
        poems = Poem.query.filter_by(author_id=db_poet.id).all()
        result['counts'] = len(poems)
    else:
        poems = Poem.query.filter_by(author_id=db_poet.id).order_by(func.random()).limit(int(counts))
    c = 0
    for poem in poems:
        ls = {'title': poem.title, 'content': poem.content, 'author': poem.poets.dynasties.name + '·' + poem.poets.name,
              'id': poem.id}
        result.get('result').append(ls)
        c+=1
    result['counts'] = c
    return jsonify(result)


@api_bp.route('/get-ts-poem/title/')
def get_poem_with_title():
    title = request.args.get('title')
    if title is None:
        return jsonify({'code': 200, 'info': '参数错误'})
    poems = Poem.query.filter_by(title=title).all()
    if len(poems) == 0:
        return jsonify({'code': 200, 'info': '未找到相关数据！'})
    result = {'result': [], 'code': 200, 'counts': len(poems)}
    for poem in poems:
        ls = {'author': poem.poets.dynasties.name + '·' + poem.poets.name, 'title': title, 'content': poem.content,
              'id': poem.id}
        result.get('result').append(ls)
    return jsonify(result)


# 宋词相关api
# 随机获取宋词，数量不超过50条
@api_bp.route('/get-song-ci/')
def get_song_ci_api():
    counts = request.args.get('counts', 1, type=int)
    if counts > 50:
        return jsonify({'code': 400, 'info': 'counts参数过大，请输入小于50的正数!'})
    song_cis = SongCi.query.order_by(func.random()).limit(counts)
    result = {'result': [], 'code': 200, 'counts': counts}
    for song_ci in song_cis:
        ls = {'title': song_ci.rhythmic, 'content': song_ci.content, 'author': '宋' + '·' + song_ci.authors.name,
              'id': song_ci.id}
        result.get('result').append(ls)
    return jsonify(result)


# 根据作者获取宋词随机获取条数或者全部获取
@api_bp.route('/get-poet/ci/')
def get_poet_ci():
    poet = request.args.get('author')
    counts = request.args.get('counts', 1)
    if poet is None:
        return jsonify({'code': 400, 'info': '参数无效！'})
    result = {'result': [], 'code': 200, 'counts': counts}
    author = SongCiAuthor.query.filter_by(name=poet).first()
    if author is None:
        return jsonify({'code': 200, 'info': '未找到相关词人！'})
    if counts == 'all':
        cis = SongCi.query.filter_by(author_id=author.id).all()
        result['counts'] = len(cis)
    else:
        cis = SongCi.query.filter_by(author_id=author.id).order_by(func.random()).limit(int(counts))
    for ci in cis:
        ls = {'title': ci.rhythmic, 'content': ci.content, 'author': '宋' + '·' + ci.authors.name, 'id': ci.id}
        result.get('result').append(ls)
    return jsonify(result)


@api_bp.route('/get-ci/title/')
def get_ci_with_title():
    title = request.args.get('title')
    poet = request.args.get('author')

    # 当没有携带title参数时，返回错误信息
    if title is None:
        return jsonify({'code': 400, 'info': '参数无效！'})

    if poet is None:
        # 如果没有携带author参数则查询所有属于与title匹配的词
        cis = SongCi.query.filter_by(rhythmic=title).all()
    else:
        # 查询当前作者下title匹配的词
        author = SongCiAuthor.query.filter_by(name=poet).first()
        if author is None:
            # 如果数据库中查询结果作者为空，则返回错误信息
            return jsonify({'code': 400, 'info': '未找到该作者相关词！'})
        cis = SongCi.query.filter(SongCi.rhythmic==title, SongCi.author_id==author.id).all()

    if len(cis) == 0:
        # 如果未查询到匹配的词，则返回提示信息
        return jsonify({'code': 200, 'info': '未找到相关作品！'})
    result = {'result': [], 'code': 200, 'counts': len(cis)}
    for ci in cis:
        # 拼接结果
        ls = {'title': ci.rhythmic, 'content': ci.content, 'author': '宋' + '·' + ci.authors.name, 'id': ci.id}
        result.get('result').append(ls)
    return jsonify(result)
