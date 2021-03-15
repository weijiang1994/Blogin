"""
# coding:utf-8
@Time    : 2020/10/26
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : oauth
@Software: PyCharm
"""
from flask import Blueprint, abort, redirect, url_for, flash
from flask_oauthlib.client import OAuthResponse
import os
from blogin.models import User, ThirdParty
from flask_login import current_user, login_user

from blogin.extension import db, oauth

github = oauth.remote_app(
    name='github',
    consumer_key=os.getenv('GITHUB_CLIENT_ID'),
    consumer_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    request_token_params={'scope': 'user'},
    base_url='https://api.github.com',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

gitee = oauth.remote_app(
    name='gitee',
    consumer_key=os.getenv('GITEE_CLIENT_ID'),
    consumer_secret=os.getenv('GITEE_CLIENT_SECRET'),
    request_token_params={'scope': 'user_info'},
    base_url='https://gitee.com/api/v5/user',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://gitee.com/oauth/token',
    authorize_url='https://gitee.com/oauth/authorize',
)

providers = {
    'github': github,
    'gitee': gitee
}

profile_endpoints = {
    'github': 'user',
    'gitee': 'user'
}

oauth_bp = Blueprint('oauth_bp', __name__)


def get_social_profile(provider, token):
    profile_endpoint = profile_endpoints[provider.name]
    response = provider.get(profile_endpoint, token=token)

    if provider.name == 'github':
        username = response.data.get('login')
        website = response.data.get('html_url')
        email = response.data.get('email')
        bio = response.data.get('bio')
        avatar = response.data.get('avatar_url')

    if provider.name == 'gitee':
        username = response.data.get('login')
        website = response.data.get('blog')
        email = response.data.get('email')
        bio = response.data.get('bio')
        avatar = response.data.get('avatar_url')

    return username, website, email, bio, avatar


@oauth_bp.route('/login/<provider_name>')
def oauth_login(provider_name):
    if provider_name not in providers.keys():
        abort(404)
    if current_user.is_authenticated:
        return redirect(url_for('blog_bp.index'))

    callback = url_for('.oauth_callback', provider_name=provider_name, _external=True)
    return providers[provider_name].authorize(callback=callback)


@oauth_bp.route('/callback/<provider_name>')
def oauth_callback(provider_name):
    try:
        if provider_name not in providers.keys():
            abort(404)

        provider = providers[provider_name]
        response = provider.authorized_response()

        if response is not None:
            if provider_name == 'twitter':
                access_token = response.get('oauth_token'), response.get('oauth_token_secret')
            if provider_name == 'github':
                access_token = response.get('access_token')
            if provider_name == 'gitee':
                access_token = response.get('access_token')
        else:
            access_token = None

        if access_token is None:
            flash('权限拒绝，请稍后再试!', 'danger')
            return redirect(url_for('auth_bp.login'))

        username, website, email, bio, avatar = get_social_profile(provider, access_token)

        if email is None:
            flash('未能正确的获取到您的邮箱，请到第三方社交网络设置邮箱后登录！', 'danger')
            return redirect(url_for('auth_bp.login'))

        user = User.query.filter_by(email=email).first()
        if user is None:
            tp = ThirdParty.query.filter_by(name=provider.name).first()
            user = User(username=username, email=email, website=website, password=provider.name, avatar=avatar,
                        slogan=bio, confirm=1, reg_way=tp.id)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash('使用{}社交账号登录成功!'.format(provider.name), 'success')
            return redirect(url_for('accounts_bp.profile', user_id=user.id))
        login_user(user, remember=True)
        flash('使用{}社交账号登录成功!'.format(provider.name), 'success')
        return redirect(url_for('blog_bp.index'))
    except:
        import traceback
        traceback.print_exc()
        flash('使用{}登录出现了意外了~稍后再试吧~'.format(provider.name), 'danger')
        return redirect(url_for('auth_bp.login'))
