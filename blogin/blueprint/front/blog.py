"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : blog_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from blogin.models import Blog, BlogType, LoveMe, LoveInfo, BlogComment, Photo, Notification, Timeline, VisitStatistics, \
    LikeStatistics, CommentStatistics, Tag, User, FriendLink
from blogin.extension import db
from flask_login import current_user, login_required
from blogin.decorators import statistic_traffic

from blogin.utils import redirect_back

blog_bp = Blueprint('blog_bp', __name__)


@blog_bp.route('/', methods=['GET'])
@blog_bp.route('/index/', methods=['GET'])
@statistic_traffic(db, VisitStatistics)
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.order_by(Blog.create_time.desc()).paginate(page, per_page=current_app.
                                                                       config['BLOGIN_BLOG_PER_PAGE'])
    blogs = pagination.items
    cates = []
    for blog in blogs:
        cates.append(BlogType.query.filter_by(id=blog.type_id).first().name)
    categories = BlogType.query.all()
    loves = LoveMe.query.first()
    if loves is None:
        loves = 0
    else:
        loves = loves.counts
    su = User.query.filter(User.email=='804022023@qq.com').first()
    flinks = FriendLink.query.filter(FriendLink.flag==1).all()
    return render_template('main/index.html', per_page=current_app.config['BLOGIN_BLOG_PER_PAGE'],
                           pagination=pagination, blogs=blogs, cates=cates, categories=categories,
                           loves=loves, su=su, flinks=flinks)


@blog_bp.route('/blog/article/<blog_id>/')
def blog_article(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    blog.read_times += 1
    replies = []
    cate = BlogType.query.filter_by(id=blog.type_id).first()
    # 顶级评论
    comments = BlogComment.query.filter_by(blog_id=blog_id, parent_id=None).order_by(BlogComment.timestamp.desc()).all()

    for comment in comments:
        reply = BlogComment.query.filter_by(parent_id=comment.id, delete_flag=0). \
            order_by(BlogComment.timestamp.desc()).all()
        replies.append(reply)
    db.session.commit()
    return render_template('main/blog.html', blog=blog, cate=cate, comments=comments, replies=replies)


@blog_bp.route('/blog/cate/<cate_id>/', methods=['GET', 'POST'])
def blog_cate(cate_id):
    cate = BlogType.query.filter_by(id=cate_id).first()
    categories = BlogType.query.all()
    return render_template('main/blogCate.html', cate=cate, categories=categories, blogs=cate.blogs)


@blog_bp.route('/loveme/')
@statistic_traffic(db, LikeStatistics)
def love_me():
    love = LoveMe.query.first()
    if love is None:
        lv = LoveMe(counts=1)
        db.session.add(lv)
    else:
        love.counts += 1
    # 如果用户已经登录,则记录用户名 ip,否则记录 匿名用户 IP
    if current_user.is_authenticated:
        li = LoveInfo(user=current_user.username, user_ip=request.remote_addr)
    else:
        li = LoveInfo(user='Anonymous', user_ip=request.remote_addr)
    db.session.add(li)
    db.session.commit()
    flash('点赞成功!你们的支持就是我前进的动力啦~', 'success')
    return redirect(url_for('.index'))


@blog_bp.route('/blog/comment/', methods=['GET', 'POST'])
@login_required
@statistic_traffic(db, CommentStatistics)
def new_comment():
    comment = request.form.get('comment')
    blog_id = request.form.get('blogID')
    reply_id = request.form.get('replyID')
    parent_id = request.form.get('parentID')
    author = current_user._get_current_object()
    notify = comment
    blog = Blog.query.get_or_404(blog_id)
    comment = BlogComment(body=comment, author=author, blog=blog)
    if reply_id:
        comment.replied = BlogComment.query.get_or_404(reply_id)
        # title = Blog.query.get_or_404(blog_id).title
        new_notify = Notification(type=0, target_id=blog_id, send_user=author.username,
                                  receive_id=comment.replied.author_id, msg=notify, target_name=blog.title)
        db.session.add(new_notify)
    if parent_id:
        comment.parent_id = parent_id
    db.session.add(comment)
    db.session.commit()
    return redirect(request.referrer)


@blog_bp.route('/blog/comment/delete/', methods=['GET', 'POST'])
@login_required
def delete_comment():
    comm_id = request.form.get('comm_id')
    comment = BlogComment.query.get_or_404(comm_id)
    comment.delete_flag = 1
    db.session.commit()
    flash('评论删除成功', 'success')
    return ''


@blog_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if q == '':
        flash('小伙子你很皮，空的关键字你想搜啥呢？', 'info')
        return redirect_back()
    category = request.args.get('category', 'blog')
    if category == 'blog':
        results = Blog.query.whooshee_search(q).paginate(1, 20)
    if category == 'photo':
        results = Photo.query.whooshee_search(q).paginate(1, 20)
    if category == 'tag':
        results = Tag.query.whooshee_search(q).paginate(1, 20)
    results = results.items
    return render_template('main/search.html', results=results, q=q, category=category)


@blog_bp.route('/blogs/archive/', methods=['GET', 'POST'])
def archive():
    blogs = Blog.query.filter_by(delete_flag=1).order_by(Blog.create_time.desc()).all()
    categories = BlogType.query.all()
    archives = {}
    for blog in blogs:
        current_year = str(blog.create_time).split(' ')[0].split('-')[0]
        current_month = str(blog.create_time).split(' ')[0].split('-')[1]
        # 如果当前年份不存在,那么当前月份也不存在
        if not archives.get(current_year):
            # 记录当前年份以及当前月份
            archives.setdefault(current_year, {current_month: []})
            archives.get(current_year).get(current_month).append([blog.id, blog.title,
                                                                  str(blog.create_time).split(' ')[0][5:]])
        else:
            # 如果当前年份存在,月份不存在,则更新一条数据到当前年份中
            if not archives.get(current_year).get(current_month):
                archives.get(current_year).update({current_month: []})
                archives.get(current_year).get(current_month).append([blog.id, blog.title,
                                                                      str(blog.create_time).split(' ')[0][5:]])
            else:
                # 年月都存在则直接将数据拼接到后面
                archives.get(current_year).get(current_month).append([blog.id, blog.title,
                                                                      str(blog.create_time).split(' ')[0][5:]])
    return render_template('main/archive.html', archives=archives, categories=categories)


TIMELINE_STYLE = [['cd-location', 'cd-icon-location.svg'], ['cd-movie', 'cd-icon-movie.svg'],
                  ['cd-picture', 'cd-icon-picture.svg'], ]


@blog_bp.route('/timeline/')
def timeline():
    timelines = Timeline.query.filter_by(abandon=0).order_by(Timeline.timestamp.desc()).all()
    return render_template('main/timeline.html', timelines=timelines)
