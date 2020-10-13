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

from flask import Blueprint, render_template, send_from_directory, request, make_response

from blogin import basedir

other_bp = Blueprint('other_bp', '__name__', url_prefix='/backend')


@other_bp.route('/timeline/add/')
def add_timeline():
    pass


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
