"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : auth
@Software: PyCharm
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class LoginForm(FlaskForm):
    usr_email = StringField(u'邮箱/用户名', validators=[DataRequired(message='用户名或邮箱不能为空')],
                            render_kw={'placeholder': '请输入邮箱或用户名'})
    password = StringField(u'登录密码',
                           validators=[DataRequired(message='登录密码不能为空'),
                                       Length(min=8, max=40, message='登录密码必须在8-40位之间')])
    submit = SubmitField(u'登录', render_kw={'cl  ass': 'btn btn-outline-light'})


class RegisterForm(FlaskForm):
    user_name = StringField(u'用户名',
                            validators=[DataRequired(message='用户名不能为空'),
                                        Length(min=1, max=8, message='用户名长度限定在1-8位之间')],
                            render_kw={'placeholder': '请输入用户名长度1-8之间'})
    user_email = StringField(u'注册邮箱',
                             validators=[DataRequired(message='注册邮箱不能为空'),
                                         Length(min=4, message='注册邮箱长度必须大于4')],
                             render_kw={'placeholder': '请输入注册邮箱'})
    password = StringField(u'密码',
                           validators=[DataRequired(message='用户密码不能为空'),
                                       Length(min=8, max=40, message='用户密码长度限定在8-40位之间'),
                                       EqualTo('confirm_pwd', message='两次密码不一致')],
                           render_kw={'placeholder': '请输入密码'})
    confirm_pwd = StringField(u'密码',
                              validators=[DataRequired(message='用户密码不能为空'),
                                          Length(min=8, max=40, message='用户密码长度限定在8-40位之间')],
                              render_kw={'placeholder': '请输入密码'})
    submit = SubmitField(u'创建', render_kw={'class': 'btn btn-outline-success'})

    @staticmethod
    def validate_username(filed):
        # TODO 需要判断该邮箱是否存在了
        if 1:
            raise ValidationError('用户名已存在')

    @staticmethod
    def validate_email(filed):
        if 1:
            raise ValidationError('邮箱已存在')

