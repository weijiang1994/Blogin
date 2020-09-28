"""
# coding:utf-8
@Time    : 2020/9/24
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : gallery
@Software: PyCharm
"""
from flask import Blueprint, render_template, send_from_directory, flash, redirect, url_for, request
from flask_login import login_required, current_user

from blogin import basedir, db
from blogin.models import Photo, LikePhoto
from blogin.models import PhotoComment

gallery_bp = Blueprint('gallery_bp', __name__, url_prefix='/gallery')


@gallery_bp.route('/all/', methods=['GET', 'POST'])
def index():
    photos = Photo.query.filter_by(level=0).order_by(Photo.create_time.desc()).all()
    return render_template('main/gallery.html', photos=photos)


@gallery_bp.route('/photo/<photo_id>', methods=['GET', 'POST'])
def photo(photo_id):
    replies = []
    img = Photo.query.get_or_404(photo_id)
    nex = Photo.query.filter(Photo.id > photo_id).order_by(Photo.id.asc()).first()
    pre = Photo.query.filter(Photo.id < photo_id).order_by(Photo.id.desc()).first()
    comments = PhotoComment.query.filter_by(photo_id=photo_id, parent_id=None).\
        order_by(PhotoComment.timestamp.desc()).all()
    for comment in comments:
        reply = PhotoComment.query.filter_by(parent_id=comment.id, delete_flag=0).\
                order_by(PhotoComment.timestamp.desc()).all()
        replies.append(reply)
    if nex is None:
        next_link = None
    else:
        next_link = '/gallery/photo/' + str(nex.id)
    if pre is None:
        pre_link = None
    else:
        pre_link = '/gallery/photo/' + str(pre.id)
    return render_template('main/photo.html', blog=img, nextLink=next_link, preLink=pre_link,
                           comments=comments, replies=replies)


@gallery_bp.route('/<path>/<filename>')
def get_blog_sample_img(path, filename):
    path = basedir + '/uploads/gallery/' + path + '/'
    return send_from_directory(path, filename)


@gallery_bp.route('/like/<photo_id>/')
@login_required
def like_photo(photo_id):
    img = Photo.query.get_or_404(photo_id)
    lp = LikePhoto(user=current_user, photo=img)
    db.session.add(lp)
    db.session.commit()
    flash('点赞成功，多谢啦~', 'success')
    return redirect(request.referrer)


@gallery_bp.route('/photo/comment/', methods=['GET', 'POST'])
@login_required
def new_comment():
    comment = request.form.get('comment')
    blog_id = request.form.get('imgID')
    reply_id = request.form.get('replyID')
    parent_id = request.form.get('parentID')
    author = current_user._get_current_object()
    img = Photo.query.get_or_404(blog_id)
    comment = PhotoComment(body=comment, author=author, photo=img)
    if reply_id:
        comment.replied = PhotoComment.query.get_or_404(reply_id)
    if parent_id:
        comment.parent_id = parent_id
    db.session.add(comment)
    db.session.commit()
    return redirect(request.referrer)


@gallery_bp.route('/comment/delete/', methods=['GET', 'POST'])
@login_required
def delete_comment():
    comm_id = request.form.get('comm_id')
    comment = PhotoComment.query.get_or_404(comm_id)
    comment.delete_flag = 1
    db.session.commit()
    flash('评论删除成功', 'success')
    return ''
