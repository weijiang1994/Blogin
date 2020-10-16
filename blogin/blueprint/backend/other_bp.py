"""
# coding:utf-8
@Time    : 2020/10/13
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : other_bp
@Software: PyCharm
"""
import os
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for, jsonify
from flask_login import current_user

from blogin.blueprint.backend.forms import TimelineForm
from blogin import basedir
from blogin.models import Timeline
from blogin.extension import db
import psutil
from blogin.extension import rd

other_bp = Blueprint('other_bp', '__name__', url_prefix='/backend')


@other_bp.route('/timeline/add/', methods=['GET', 'POST'])
def add_timeline():
    form = TimelineForm()
    if form.validate_on_submit():
        title = form.timeline_title.data
        content = form.timeline_content.data
        if content[-1] != '；':
            flash('里程碑内容请以分号结尾!', 'danger')
            return render_template('backend/addTimeline.html', form=form)

        # 分割并拼接里程碑内容
        milestone_body = splice_tm_content(content)

        # 存储当前时间内容
        timeline = Timeline(title=title, content=milestone_body, timestamp=form.timestamp.data)
        db.session.add(timeline)
        db.session.commit()
        flash('里程碑添加成功!', 'success')
        return redirect(url_for('blog_bp.timeline'))
    return render_template('backend/addTimeline.html', form=form)


def splice_tm_content(content):
    contents = content.split('；')[:-1]
    milestone_body = "<ul>"
    for content in contents:
        milestone_body += '<li>' + content + '</li>'
    milestone_body += "</ul>"
    return milestone_body


@other_bp.route('/timeline/edit/')
def edit_timeline():
    timelines = Timeline.query.order_by(Timeline.timestamp.desc()).all()
    return render_template('backend/editTimeline.html', timelines=timelines)


@other_bp.route('/timeline/info-edit/<int:tm_id>/', methods=['GET', 'POST'])
def tm_info_edit(tm_id):
    form = TimelineForm()
    tm = Timeline.query.get_or_404(tm_id)
    if form.validate_on_submit():
        content = form.timeline_content.data
        if content[-1] != '；':
            flash('里程碑内容请以分号结尾!', 'danger')
            return render_template('backend/editTimelineInfo.html', form=form)

        milestone_body = splice_tm_content(content)
        tm.title = form.timeline_title.data
        tm.content = milestone_body
        tm.timestamp = form.timestamp.data
        db.session.commit()
        flash('里程碑编辑成功!', 'success')
        return redirect(url_for('.edit_timeline'))

    # 原始数据复现
    form.timestamp.data = tm.timestamp
    form.timeline_title.data = tm.title

    # 由于保存的时候拼接了ul，所以使用bs4来进行元素分割
    bs = BeautifulSoup(tm.content, 'html.parser')
    origin_tm_content = ''
    for l in bs.find_all('li'):
        origin_tm_content += l.string + '；'
    form.timeline_content.data = origin_tm_content
    form.submit.render_kw = {'value': '保存修改'}
    return render_template('backend/editTimelineInfo.html', form=form)


@other_bp.route('/timeline/abandon/<int:tm_id>/')
def abandon_tm(tm_id):
    tm = Timeline.query.get_or_404(tm_id)
    tm.abandon = 1
    db.session.commit()
    flash('遗弃该里程碑操作成功!', 'success')
    return redirect(url_for('.edit_timeline'))


@other_bp.route('/timeline/activate/<int:tm_id>/')
def activate_tm(tm_id):
    tm = Timeline.query.get_or_404(tm_id)
    tm.abandon = 0
    db.session.commit()
    flash('启用该里程碑操作成功!', 'success')
    return redirect(url_for('.edit_timeline'))


@other_bp.route('/logs/')
def look_logs():
    logs = []
    app_log_path = basedir + '/logs/'
    nginx_log_path = '/var/log/nginx/'
    # 运行日志
    get_log_file_info(app_log_path, logs)
    get_log_file_info(nginx_log_path, logs, log_cate='nginx access/error 文件日志!')
    return render_template('backend/logs.html', logs=logs)


def get_log_file_info(app_log_path, logs, log_cate='程序运行日志！'):
    for app_log in get_log_files(app_log_path):
        app_log_update_time = get_file_mtime(app_log)
        app_log_size = os.path.getsize(app_log)
        logs.append([os.path.split(app_log)[1], log_cate, app_log_update_time, app_log, str(app_log_size) + 'byte'])


@other_bp.route('/logs/detail/<path:file_path>/')
def log_detail(file_path):
    """
    显示日志文件内容
    :param file_path: 日志文件路径
    :return: 日志文件详细内容页面
    """
    contents = []
    with open('/' + file_path) as f:
        for line in f.readlines():
            line.strip('\n')
            if line.__contains__('[GET]') or line.__contains__('[POST]'):
                line = "<span style='color: red;'>" + line + "</span>"
            if line.__contains__('Traceback'):
                line = "<span style='color: red;'>" + line + "</span>"
            contents.append(line)
    return render_template('backend/logDetail.html', contents=contents, path='/' + file_path)


@other_bp.route('/logs/download/')
def download_log_file():
    """
    下载备份日志文件
    :return: 日志文件
    """
    file = request.args.get('filename')
    return send_from_directory(os.path.split(file)[0], filename=os.path.split(file)[1], as_attachment=True)


@other_bp.route('/server-status/', methods=['GET', 'POST'])
def server_status():
    if request.method == 'POST':
        history_percent = rd.lrange(current_user.id, 0, -1)
        times = rd.lrange('times', 0, -1)
        cpu_use_rate = psutil.cpu_percent()
        history_percent.append(cpu_use_rate)
        now_time = datetime.now().strftime('%H:%M:%S')
        times.append(now_time)
        # 存入到redis缓存数据库
        rd.rpush(current_user.id, cpu_use_rate)
        rd.rpush('times', now_time)
        return jsonify({'times': times, 'cpu_rates': history_percent})

    cpu_counts = psutil.cpu_count()
    cpu_use_rate = psutil.cpu_percent()
    return render_template('backend/serverStatus.html', cpu_counts=cpu_counts, cpu_use_rate=cpu_use_rate)


def get_file_mtime(path):
    """
    获取文件最后修改时间
    :param path: 文件路径
    :return: 文件最后修改时间
    """
    timestamp = os.path.getmtime(path)
    timestamp = datetime.fromtimestamp(timestamp)
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp


def get_log_files(path):
    """
    便利文件夹，获取文件夹中的log文件路径
    :param path: 需要遍历的目标文件夹
    :return: 目标文件夹根目录下的所有log文件
    """
    fl_ls = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.__contains__('log') and not f.__contains__('.gz'):
                fl_ls.append(os.path.join(root, f))
    return fl_ls
