"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : blog_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, jsonify, abort, \
    make_response, session
from blogin.models import Blog, BlogType, LoveMe, LoveInfo, BlogComment, Photo, Notification, Timeline, VisitStatistics, \
    LikeStatistics, CommentStatistics, Tag, User, FriendLink, Contribute, Plan, BlogHistory, PostContent, MessageBorder, \
    OneSentence
from blogin.extension import db, rd, cache
from flask_login import current_user, login_required
from blogin.decorators import statistic_traffic
import datetime
from blogin.utils import redirect_back, github_social, BOOTSTRAP_SUFFIX
import requests
from blogin.emails import send_comment_email
from blogin.setting import basedir
import configparser

blog_bp = Blueprint('blog_bp', __name__)


@blog_bp.route('/', methods=['GET'])
@blog_bp.route('/index/', methods=['GET'])
@statistic_traffic(db, VisitStatistics)
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter(Blog.delete_flag == 1, Blog.is_private == 0
                                   ).order_by(Blog.is_top.desc(), Blog.create_time.desc()
                                              ).paginate(page, per_page=current_app.config['BLOGIN_BLOG_PER_PAGE'])
    blogs = pagination.items
    cates = [BlogType.query.filter_by(id=blog.type_id).first().name for blog in blogs]
    categories = BlogType.query.all()
    loves = LoveMe.query.first()
    loves = 0 if loves is None else loves.counts
    plans = Plan.query.filter_by(is_done=0).all()
    su = User.query.filter(User.email == '804022023@qq.com').first()
    flinks = FriendLink.query.filter(FriendLink.flag == 1).all()
    msg_borders = MessageBorder.query.filter(MessageBorder.flag == 0, MessageBorder.parent_id == 0
                                             ).order_by(MessageBorder.timestamps.desc()).all()[0:5]
    return render_template('main/index.html', per_page=current_app.config['BLOGIN_BLOG_PER_PAGE'],
                           pagination=pagination, blogs=blogs, cates=cates, categories=categories,
                           loves=loves, su=su, flinks=flinks, plans=plans, msg_borders=msg_borders)


@blog_bp.route('/get-contribution/', methods=['POST'])
def get_contribution():
    # 获取开始日期结束日期，长度为90天
    t = datetime.date.today()
    s_day = t + datetime.timedelta(days=-89)
    result = []
    contributes = Contribute.query.filter(Contribute.date >= s_day).filter(Contribute.date <= t).all()

    for con in contributes:
        result.append([str(con.date), con.contribute_counts])
    return jsonify({'start': str(s_day), 'end': str(t), 'data': result})


@blog_bp.route('/blog/article/<blog_id>/')
def blog_article(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    blog.read_times += 1
    replies = []
    cate = BlogType.query.filter_by(id=blog.type_id).first()
    # 顶级评论
    comments = BlogComment.query.filter_by(blog_id=blog_id, parent_id=None).order_by(BlogComment.timestamp.desc()).all()
    histories = BlogHistory.query.filter_by(blog_id=blog_id).order_by(BlogHistory.timestamps.desc()).all()

    # 获取上一篇下一篇
    next_post = Blog.query.filter(Blog.id > blog_id, Blog.delete_flag == 1).order_by(Blog.id.desc()).first()
    pre_post = Blog.query.filter(Blog.id < blog_id, Blog.delete_flag == 1).order_by(Blog.id.desc()).first()

    # 获取目录
    content = PostContent.query.filter_by(post_id=blog.id).first()
    if content:
        content = eval(content.content)

    for comment in comments:
        reply = BlogComment.query.filter_by(parent_id=comment.id, delete_flag=0). \
            order_by(BlogComment.timestamp.asc()).all()
        replies.append(reply)
    db.session.commit()
    return render_template('main/blog.html', blog=blog, cate=cate, comments=comments, replies=replies,
                           histories=histories, next_post=next_post, pre_post=pre_post, content=content)


@blog_bp.route('/blog/cate/<cate_id>/', methods=['GET', 'POST'])
def blog_cate(cate_id):
    cate = BlogType.query.filter_by(id=cate_id).first()
    categories = BlogType.query.all()
    flinks = FriendLink.query.filter(FriendLink.flag == 1).all()
    plans = Plan.query.filter_by(is_done=0).all()
    msg_borders = MessageBorder.query.filter(MessageBorder.flag == 0, MessageBorder.parent_id == 0). \
                      order_by(MessageBorder.timestamps.desc()).all()[0:5]
    return render_template('main/blog-cate.html', cate=cate, categories=categories, blogs=cate.blogs, flinks=flinks,
                           plans=plans, msg_borders=msg_borders)


@blog_bp.route('/blog/history/<h_id>/')
def blog_history(h_id):
    bh = BlogHistory.query.get_or_404(h_id)
    with open(bh.save_path, 'r', encoding='utf-8') as f:
        content = f.read()
    blog = Blog.query.get_or_404(bh.blog_id)
    return render_template('main/blog-history.html', content=content, blog=blog)


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
    remote_ip = request.headers.get('X-Real-Ip')
    if remote_ip is None:
        remote_ip = request.remote_addr

    if current_user.is_authenticated:
        li = LoveInfo(user=current_user.username, user_ip=remote_ip)
    else:
        li = LoveInfo(user='Anonymous', user_ip=remote_ip)
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
    admin = User.query.filter_by(email='804022023@qq.com').first()
    author = current_user._get_current_object()
    notify = comment
    blog = Blog.query.get_or_404(blog_id)
    comment = BlogComment(body=comment, author=author, blog=blog)
    if reply_id:
        pbc = BlogComment.query.get_or_404(reply_id)
        comment.replied = pbc
        # title = Blog.query.get_or_404(blog_id).title
        new_notify = Notification(type=0, target_id=blog_id, send_user=author.username,
                                  receive_id=comment.replied.author_id, msg=notify, target_name=blog.title)
        db.session.add(new_notify)
        if pbc.author.received_email_tag:
            send_comment_email(user=pbc.author, blog=blog)

    if parent_id:
        comment.parent_id = parent_id

    db.session.add(comment)
    db.session.commit()
    if not reply_id:
        send_comment_email(user=admin, blog=blog)
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
    flinks = FriendLink.query.filter(FriendLink.flag == 1).all()
    plans = Plan.query.filter_by(is_done=0).all()
    years = []
    months = []
    msg_borders = MessageBorder.query.filter(MessageBorder.flag == 0, MessageBorder.parent_id == 0). \
                      order_by(MessageBorder.timestamps.desc()).all()[0:5]
    for blog in blogs:
        current_year = blog.create_time.year
        current_month = blog.create_time.month
        # 如果当前年份不存在,那么当前月份也不存在
        if not archives.get(current_year):
            # 记录当前年份以及当前月份
            years.append(current_year)
            months.append(current_month)
            archives[current_year] = {current_month: []}
            archives.get(current_year).get(current_month).append([blog.id, blog.title,
                                                                  str(blog.create_time).split(' ')[0][5:]])
        else:
            # 如果当前年份存在,月份不存在,则更新一条数据到当前年份中
            if not archives.get(current_year).get(current_month):
                archives.get(current_year).update({current_month: []})
                months.append(current_month)
                archives.get(current_year).get(current_month).append([blog.id, blog.title,
                                                                      str(blog.create_time).split(' ')[0][5:]])
            else:
                # 年月都存在则直接将数据拼接到后面
                archives.get(current_year).get(current_month).append([blog.id, blog.title,
                                                                      str(blog.create_time).split(' ')[0][5:]])

    return render_template('main/archive.html', archives=archives, categories=categories, flinks=flinks, plans=plans,
                           years=years, months=months, msg_borders=msg_borders)


TIMELINE_STYLE = [['cd-location', 'cd-icon-location.svg'], ['cd-movie', 'cd-icon-movie.svg'],
                  ['cd-picture', 'cd-icon-picture.svg'], ]


@blog_bp.route('/timeline/')
def timeline():
    timelines = Timeline.query.filter_by(abandon=0).order_by(Timeline.timestamp.desc()).all()
    return render_template('main/timeline.html', timelines=timelines)


@blog_bp.route('/themes/<string:theme_name>/')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLOG_THEMES'].keys():
        abort(404)
    cache.clear()
    response = redirect(request.referrer)
    response.set_cookie('blog_theme', current_app.config['BLOG_THEMES'].get(theme_name), max_age=30 * 24 * 60 * 60)
    return response


# noinspection PyTypeChecker
@blog_bp.route('/load-github/', methods=['POST'])
@cache.cached(timeout=5 * 60)
def load_github():
    theme = request.form.get('theme')
    star = rd.get('star')
    if star is None:
        star, fork, watcher, star_dark, fork_dark, watcher_dark, user_info, repo_info = github_social()
        avatar = user_info.json()['avatar_url']
        repo_desc = repo_info.json()['description']

        # 获取浅色主题的shield
        rd.set('star', star.text, ex=5*60)
        rd.set('fork', fork.text, ex=5*60)
        rd.set('watcher', watcher.text, ex=5*60)

        # 获取深色主题的shield
        rd.set('star_dark', star_dark.text, ex=5*60)
        rd.set('fork_dark', fork_dark.text, ex=5*60)
        rd.set('watcher_dark', watcher_dark.text, ex=5*60)

        rd.set('avatar', avatar, ex=5*60)
        rd.set('repo_desc', repo_desc, ex=5*60)
        star = star.text

        if theme == 'dark':
            star = star_dark.text
            fork, watcher = fork_dark.text, watcher_dark.text
        else:
            fork, watcher = fork.text, watcher.text

    else:
        if theme == 'dark':
            fork = rd.get('fork_dark')
            watcher = rd.get('watcher_dark')
            star = rd.get('star_dark')
        else:
            fork = rd.get('fork')
            watcher = rd.get('watcher')

        avatar = rd.get('avatar')
        repo_desc = rd.get('repo_desc')
    return '<div style="border-bottom: 1px solid rgba(58,10,10,0.19); margin-bottom: 5px;padding-bottom: 3px;" class="d-flex">\
                <a href="https://github.com/weijiang1994/" target="_blank"><img class="avatar-s" id="githubAvatar"\
                                                                                alt="avatar"\
                                                                                src="{}"></a>\
                <div class="ml-2">\
                    <h5 class="mb-0"><b>Blogin</b></h5>\
                    <small id="repoDesc">{}</small>\
                </div>\
                <a class="btn btn-sm btn-light h-25" id="githubStar"\
                   href="https://github.com/weijiang1994/Blogin" target="_blank">Star</a>\
            </div>\
            <div id="shield-svg" class="text-left pr-1 d-flex">\
                <div class="mr-1">{}</div><div class="mr-1">{}</div><div class="mr-1">{}</div>\
            </div>'.format(avatar, repo_desc, star, fork, watcher)
    # return jsonify({'star': star,
    #                 'fork': fork,
    #                 'watcher': watcher,
    #                 'avatar': avatar,
    #                 'repo_desc': repo_desc
    #                 })


@blog_bp.route('/load-one/', methods=['POST', 'GET'])
def load_one():
    one = rd.get('one')
    # 防止服务器重启之后清空了redis数据导致前端获取不到当日one内容
    if not one:
        one = OneSentence.query.filter_by(day=datetime.date.today()).first()
        if request.method == 'GET':
            return "<p class='mb-1'>{}</p>".format(one.content)
        else:
            return jsonify({'one': one.content})
    if request.method == 'GET':
        return "<p class='mb-1'>{}</p>".format(one)
    return jsonify({'one': one})
