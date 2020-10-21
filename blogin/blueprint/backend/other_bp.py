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
from flask_login import current_user, login_required

from blogin.blueprint.backend.forms import TimelineForm, AddFlinkForm
from blogin import basedir
from blogin.decorators import permission_required
from blogin.models import Timeline, FriendLink, States
from blogin.extension import db
import psutil
from blogin.extension import rd
from blogin.emails import send_server_warning_mail

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
@login_required
@permission_required
def server_status():
    if request.method == 'POST':
        # 获取redis中历史缓存数据
        history_percent = rd.lrange(current_user.id, 0, -1)
        history_memory = rd.lrange(str(current_user.id) + 'mem', 0, -1)
        times = rd.lrange('times', 0, -1)
        # 获取cpu相关信息
        cpu_use_rate = psutil.cpu_percent()
        history_percent.append(cpu_use_rate)

        # 获取内存相关信息
        memory = psutil.virtual_memory()
        history_memory.append(memory.percent)
        # 磁盘信息
        disk = psutil.disk_usage('/')

        now_time = datetime.now().strftime('%H:%M:%S')
        times.append(now_time)
        net = psutil.net_io_counters()
        # 只保留历史200条数据
        if len(times) > 200:
            times.pop(0)
            history_percent.pop(0)
            rd.lpop(1)
            rd.lpop('times')
            rd.lpop('1mem')

            # 存入到redis缓存数据库
            rd.rpush(current_user.id, cpu_use_rate)
            rd.rpush('times', now_time)
            rd.rpush(str(current_user.id) + 'mem', memory.percent)
        else:
            # 存入到redis缓存数据库
            rd.rpush(current_user.id, cpu_use_rate)
            rd.rpush('times', now_time)
            rd.rpush(str(current_user.id) + 'mem', memory.percent)
        if cpu_use_rate > 95 or memory.percent > 95:
            # 发送告警邮件
            send = rd.get('warningEmail')
            if not send:
                # 发送间隔三小时，不然会一直收到邮件，如果该条件满足
                send_server_warning_mail(cpu_rate=cpu_use_rate, mem_rate=memory.percent)
                rd.set('warningEmail', 1, ex=60 * 60 * 3)

        return jsonify({'times': times, 'cpu_rates': history_percent, 'mem_rates': history_memory,
                        'disk': [round(disk.free / 1024 / 1024 / 1024, 2), round(disk.used / 1024 / 1024 / 1024, 2)],
                        'net': [round(net.bytes_sent / 1024 / 1024, 2), round(net.bytes_recv / 1024 / 1024, 2),
                                net.packets_sent, net.packets_recv, net.errin, net.errout, net.dropin, net.dropout]})

    cpu_counts = psutil.cpu_count()
    cpu_use_rate = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    return render_template('backend/serverStatus.html', cpu_counts=cpu_counts, cpu_use_rate=cpu_use_rate,
                           memory_total=round(memory.total / 1024 / 1024 / 1024, 2),
                           memory_used=round(memory.used / 1024 / 1024 / 1024, 2),
                           mem_percent=memory.percent,
                           disk_total=round(disk.total / 1024 / 1024 / 1024, 2),
                           disk_used=round(disk.used / 1024 / 1024 / 1024, 2),
                           disk_free=round(disk.free / 1024 / 1024 / 1024, 2),
                           net=net)


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


@other_bp.route('/flink/add/', methods=['GET', 'POST'])
@login_required
@permission_required
def add_flink():
    form = AddFlinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.link.data
        desc = form.desc.data
        status = States.query.filter(States.name=='正常').first()
        flink = FriendLink(name=name, link=url, flag=status.id, desc=desc)
        db.session.add(flink)
        db.session.commit()
        return redirect(url_for('blog_bp.index'))
    return render_template('backend/addFlink.html', form=form)


@other_bp.route('/flink/edit/', methods=['GET', 'POST'])
@login_required
@permission_required
def edit_flink():
    flinks = FriendLink.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        desc = request.form.get('desc')
        flink_id = request.form.get('btnID')
        flink = FriendLink.query.get_or_404(flink_id)
        if flink:
            flink.name = name
            flink.link = url
            flink.desc = desc
            db.session.commit()
        return jsonify({'tag': 1})
    return render_template('backend/editFlink.html', flinks=flinks)
