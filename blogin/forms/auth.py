"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : auth
@Software: PyCharm
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, BooleanField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from blogin.models import User

# noinspection PyMethodMayBeStatic


class LoginForm(FlaskForm):
    usr_email = StringField(u'邮箱/用户名', validators=[DataRequired(message='用户名或邮箱不能为空')],
                            render_kw={'placeholder': '请输入邮箱或用户名'})
    password = StringField(u'登录密码',
                           validators=[DataRequired(message='登录密码不能为空'),
                                       Length(min=8, max=40, message='登录密码必须在8-40位之间')],
                           render_kw={'type': 'password','placeholder': '请输入用户密码'})
    remember_me = BooleanField('记住我')
    submit = SubmitField(u'登录', render_kw={'class': 'btn btn-secondary'})


class RegisterForm(FlaskForm):
    user_name = StringField(u'用户名',
                            validators=[DataRequired(message='用户名不能为空'),
                                        Length(min=1, max=16, message='用户名长度限定在1-16位之间'),
                                        Regexp('^[a-zA-Z0-9_]*$',
                                               message='用户名只能包含数字、字母以及下划线.')],
                            render_kw={'placeholder': '请输入用户名长度1-8之间'})
    user_email = StringField(u'注册邮箱',
                             validators=[DataRequired(message='注册邮箱不能为空'),
                                         Length(min=4, message='注册邮箱长度必须大于4')],
                             render_kw={'placeholder': '请输入注册邮箱', 'type': 'email'})
    password = StringField(u'密码',
                           validators=[DataRequired(message='用户密码不能为空'),
                                       Length(min=8, max=40, message='用户密码长度限定在8-40位之间'),
                                       EqualTo('confirm_pwd', message='两次密码不一致')],
                           render_kw={'placeholder': '请输入密码', 'type': 'password'})
    confirm_pwd = StringField(u'确认密码',
                              validators=[DataRequired(message='用户密码不能为空'),
                                          Length(min=8, max=40, message='用户密码长度限定在8-40位之间')],
                              render_kw={'placeholder': '请确认密码', 'type': 'password'})
    submit = SubmitField(u'创建', render_kw={'class': 'btn btn-secondary'})

    def validate_user_name(self, filed):
        if User.query.filter_by(username=filed.data).first():
            raise ValidationError('用户名已被注册.')

    def validate_user_email(self, filed):
        if User.query.filter_by(email=filed.data.lower()).first():
            raise ValidationError('邮箱已被注册.')


class ChangePwdForm(FlaskForm):
    origin_pwd = StringField(u'原始密码', validators=[DataRequired(message='原始密码不能为空.')],
                             render_kw={'placeholder': '请输入原始密码', 'type': 'password'})
    change_pwd = StringField(u'新的密码', validators=[DataRequired(message='修改后的密码不能为空.'),
                                                  EqualTo('confirm_pwd', message='两次输入密码不一致.')],
                             render_kw={'placeholder': '请输入新的密码', 'type': 'password'})
    confirm_pwd = StringField(u'确认密码', validators=[DataRequired(message='原始密码不能为空')],
                              render_kw={'placeholder': '请再次确认密码', 'type': 'password'})
    submit = SubmitField(u'修改', render_kw={'class': 'btn btn-secondary'})

    def validate_origin_pwd(self, filed):
        if not User.query.filter_by(username=current_user.username).first().check_password(filed.data):
            raise ValidationError('原始密码错误')


class EditProfileForm(FlaskForm):
    user_name = StringField(u'用户名',
                            validators=[DataRequired(message='用户名不能为空'),
                                        Length(min=1, max=16, message='用户名长度限定在1-16位之间'),
                                        Regexp('^[a-zA-Z0-9_]*$',
                                               message='用户名只能包含数字、字母以及下划线.')],
                            render_kw={'placeholder': '请输入用户名长度1-8之间'})
    website = StringField(u'个人网站', render_kw={'placeholder': '请输入个人网站', 'type': 'url'})
    avatar = FileField(u'个人头像', validators=[FileAllowed(['png', 'jpg'], '只接收png和jpg图片')])
    slogan = TextAreaField(u'个性签名', render_kw={'placeholder': '签名不超过200个字符'})
    receive_email = BooleanField(u'邮件提醒', default=True)
    submit = SubmitField(u'保存', render_kw={'class': 'btn btn-secondary'})
