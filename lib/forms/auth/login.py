# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required

from lib.models import UserModel, VarifyItem
import base64


class LoginForm(Form):
    username = StringField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    submit = SubmitField('Login')

    def generate_passwd(password):
        password = base64.b64encode(password)
        return password

    def generate_account(self):
        return VarifyItem(
            username=self.username.data,
            password=self.password.data
        )

    def generate_user(self):
        return UserModel.create_user(
            username=self.username.data,
            password=self.password.data
        )
