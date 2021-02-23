"""
# coding:utf-8
@Time    : 2020/11/19
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : task.py
@Software: PyCharm
"""
from blogin.models import Contribute, VisitStatistics, LikeStatistics, CommentStatistics, OneSentence
from apscheduler.executors.base import BaseExecutor
from flask import current_app
from blogin.extension import db, aps, rd
import datetime
from blogin.utils import github_social, get_md5, get_current_time
from blogin.setting import basedir
import traceback
import requests


def write_task_log(info):
    with open(basedir + '/logs/task.log', 'a') as f:
        f.write(str(datetime.datetime.now()) + " " + info + '\n')


@aps.task('cron', id='get_one', day='*', hour='08', minute='10', second='00')
def get_one():
    try:
        with db.app.app_context():
            date = datetime.date.today()
            one = OneSentence.query.filter_by(day=date).first()
            if not one:
                import requests
                from bs4 import BeautifulSoup
                res = requests.get('http://wufazhuce.com/', timeout=30)
                bs = BeautifulSoup(res.text, 'html.parser')
                attr = {'class': 'fp-one-cita'}
                d = bs.find_all('div', attrs=attr)
                one = OneSentence(content=d[0].text, day=date)
                db.session.add(one)
                db.session.commit()
                write_task_log('插入每日一句成功!')
                rd.set('one', d[0].text)
    except:
        write_task_log('插入每日一句失败,错误原因:\n' + str(traceback.format_exc()))


@aps.task('cron', id='do_job_3', day='*', hour='00', minute='00', second='50')
def auto_insert_data():
    """
    定时任务,每天00:00:50时刻自动向数据库中插入一条数据,如果数据库中存在了则不作任何动作
    """
    with db.app.app_context():
        date = datetime.date.today()
        contribute = Contribute.query.filter_by(date=date).first()
        visit = VisitStatistics.query.filter_by(date=date).first()
        lk = LikeStatistics.query.filter_by(date=date).first()
        com = CommentStatistics.query.filter_by(date=date).first()
        if not contribute:
            con = Contribute(contribute_counts=0, date=date)
            db.session.add(con)
        if not visit:
            vis = VisitStatistics(date=date, times=0)
            db.session.add(vis)
        if not lk:
            like = LikeStatistics(date=date, times=0)
            db.session.add(like)
        if not com:
            comm = CommentStatistics(date=date, times=0)
            db.session.add(comm)
        db.session.commit()


@aps.task('interval', id='update_github_avatar', max_instances=1, minutes=30)
def update_github_avatar():
    try:
        link = rd.get('avatar')
        res = requests.get(link, timeout=30)
        md5 = get_md5(str(get_current_time()))
        with open(basedir + '/uploads/github/{}.png'.format(md5), 'wb') as f:
            f.write(res.content)

        # 移除上一次任务存储的图片
        pre_md5 = rd.get('pre_md5')
        if pre_md5:
            import os
            os.remove(basedir + '/uploads/github/{}.png'.format(pre_md5))

        # 更新redis中local_avatar的值
        rd.set('local_avatar', '/tool/github/{}.png'.format(md5))
        rd.set('pre_md5', md5)
        write_task_log('更新github头像成功!')
    except Exception as e:
        write_task_log('更新github头像失败!失败原因:\n' + str(e.args) + '\n' +
                       str(traceback.format_exc()))


# noinspection PyBroadException
@aps.task('interval', id='update_github_info', max_instances=1, minutes=10)
def update_github_info():
    try:
        star, fork, watcher, star_dark, fork_dark, watcher_dark, user_info, repo_info = github_social()
        if star.status_code == 200:
            rd.set('star', star.text)
        if fork.status_code == 200:
            rd.set('fork', fork.text)
        if watcher.status_code == 200:
            rd.set('watcher', watcher.text)
        if star_dark.status_code == 200:
            rd.set('star_dark', star_dark.text)
        if fork_dark.status_code == 200:
            rd.set('fork_dark', fork_dark.text)
        if watcher_dark.status_code == 200:
            rd.set('watcher_dark', watcher_dark.text)
        if user_info.status_code == 200:
            rd.set('avatar', user_info.json()['avatar_url'])
        if repo_info.status_code == 200:
            rd.set('repo_desc', repo_info.json()['description'])
        write_task_log('更新github仓库信息成功!')
    except Exception as e:
        write_task_log('更新github仓库信息失败!失败原因:\n' + str(e.args) + '\n' +
                       str(traceback.format_exc()))


@aps.task('cron', id='update_baidu_token', day='5, 20', hour='15', minute='43', second='05')
def update_bd_token():
    import configparser
    import requests
    c = configparser.ConfigParser()
    c.read(basedir + '/res/config.ini')
    ak = c.get('baidu', 'ak')
    sk = c.get('baidu', 'sk')
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    try:
        res = requests.get(url)
        if res.status_code == 200:
            token = res.json().get('access_token')
            c.set('baidu', 'token', token)
            c.write(open(basedir + '/res/config.ini', 'r+'))
            write_task_log('更新百度OCR token成功!')
        else:
            write_task_log('更新百度OCR失败，错误代码:' + str(res.status_code) + '请求连接:' + url)
    except Exception as e:
        write_task_log('更新百度OCR失败，错误原因:\n' + str(e.args) + '\n' + traceback.format_exc())

