"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@File    : commands
@Software: PyCharm
"""
import os
import traceback

import click
from flask import Flask

from blogin.extension import db
from blogin.models import User, Role, States, ThirdParty, Blog, BlogHistory


def register_cmd(app: Flask):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Drop database and create a new database')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Initializing the states...')
        States.init_states()
        click.echo('Initializing the third party login...')
        ThirdParty.init_tp()
        click.echo('Initialized database.')
        click.echo('Done.')

    @app.cli.command()
    def admin():
        try:
            username = input('请输入超级管理员用户名:')
            email = input('请输入超级管理员邮箱:')
            pwd = input('请输入超级管理员密码:')
            confirm = input('请确认密码:')
            if pwd != confirm:
                click.echo('两次密码不一致')
                click.echo('退出当前操作')
                return

            super_user = User(username=username, email=email, confirm=1, role_id=1)
            super_user.set_password(pwd)
            super_user.set_admin()
            db.session.add(super_user)
            db.session.commit()
            click.echo('超级管理员创建成功!')
            click.echo('应用初始化成功!')
            click.echo('程序退出...')
        except Exception:
            traceback.print_exc()
            db.session.rollback()
            click.echo('操作出现异常,退出...')

    @app.cli.command()
    def admin_docker():
        if User.query.filter_by(username='admin').first():
            click.echo('超级管理员已存在, 退出...')
            return

        default_pwd = os.getenv('SUPER_USER_PWD', '12345678')
        super_user = User(
            username='admin',
            email=os.getenv('SUPER_USER_EMAIL', 'admin@example.com'),
            confirm=1,
            role_id=1
        )
        super_user.set_password(default_pwd)
        super_user.set_admin()
        db.session.add(super_user)
        db.session.commit()
        click.echo('超级管理员创建成功!')
        click.echo(f'账号: admin, 密码: {default_pwd}')
        click.echo('程序退出...')

    @app.cli.command()
    def addtp():
        third_party_name = input('请输入第三方登录方式:')
        tp = ThirdParty(name=third_party_name)
        db.session.add(tp)
        db.session.commit()
        click.echo('添加成功')

    @app.cli.command()
    def archive():
        blogs = Blog.query.filter_by(delete_flag=1).order_by(Blog.create_time.desc()).all()
        archives = {}
        for blog in blogs:
            current_year = blog.create_time.year
            current_month = blog.create_time.month
            if not archives.get(current_year):
                archives[current_year] = {current_month: []}
                archives.get(current_year).get(current_month).append(
                    [blog.id, blog.title, str(blog.create_time).split(' ')[0][5:]])
            else:
                if not archives.get(current_year).get(current_month):
                    archives.get(current_year).update({current_month: []})
                    archives.get(current_year).get(current_month).append(
                        [blog.id, blog.title, str(blog.create_time).split(' ')[0][5:]])
                else:
                    archives.get(current_year).get(current_month).append(
                        [blog.id, blog.title, str(blog.create_time).split(' ')[0][5:]])
        click.echo(str(archives))

    @app.cli.command()
    def update_history():
        bhs = BlogHistory.query.all()
        for bh in bhs:
            bh.save_path = bh.save_path.replace('/home/ubuntu/Blogin/', '')
        db.session.commit()
        click.echo('修改成功')
