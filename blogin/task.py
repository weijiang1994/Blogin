"""
# coding:utf-8
@Time    : 2020/11/19
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : task.py
@Software: PyCharm
"""
from blogin.models import Contribute, VisitStatistics, LikeStatistics, CommentStatistics
from blogin.extension import db, aps, rd
import datetime
from blogin.utils import github_social
from blogin.setting import basedir


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


# noinspection PyBroadException
@aps.task('interval', id='update_github_info', minutes=5)
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
    except:
        import traceback
        with open(basedir + '/logs/task.log', 'a') as f:
            f.write(traceback.print_exc())
