# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required

from lib.models import AccountItem


class LoginForm(Form):
    username = StringField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    submit = SubmitField('Login')

    def generate_account(self):
        return AccountItem.create_account(
            username=self.username.data,
            password=self.password.data
        )
