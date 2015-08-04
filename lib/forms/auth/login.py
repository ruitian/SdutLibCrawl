# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required

from lib.models import UserModel


class LoginForm(Form):
    username = StringField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    submit = SubmitField('Login')

    def login(self):
        return UserModel.create_user(
            username=self.username.data,
            password=self.password.data
        )
