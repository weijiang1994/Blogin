"""
# coding:utf-8
@Time    : 2020/9/30
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : forms
@Software: PyCharm
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class ResetPwdForm(FlaskForm):
    email = StringField(u'注册邮箱', validators=[DataRequired()], render_kw={'type': 'email',
                                                                         'placeholder': '请输入注册时使用的邮箱'})
    new_pwd = StringField(u'新的密码', validators=[DataRequired(), Length(min=8, max=20, message='密码长度需要在8-20位之间'),
                                               EqualTo('confirm_pwd', message='两次密码不一致')],
                          render_kw={'placeholder': '请输入新的密码',
                                     'type': 'password'})
    confirm_pwd = StringField(u'确认密码', validators=[DataRequired(), Length(min=8, max=20, message='密码长度需要在8-20位之间')],
                              render_kw={'placeholder': '请输入新的密码', 'type': 'password'})
    ver_code = StringField(u'验证码', validators=[DataRequired(), Length(min=6, max=6, message='验证码必须为6位')],
                           render_kw={'placeholder': '请输入邮箱验证码', 'type': 'number'})
    submit = SubmitField(u'重置密码')
