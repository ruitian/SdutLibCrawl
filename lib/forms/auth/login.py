# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Required, ValidationError
from lib.models import UserModel


class LoginForm(Form):
    username = StringField('username', [Required()])
    password = PasswordField('password', [Required()])
    submit = SubmitField('Submit')

    def validate_password(self, field):
        user = UserModel.objects.filter(
            username=self.username.data
        ).first()
        print user.verify_password(field.data)
        if user is not None and user.verify_password(field.data):
            self.user = user
        else:
            raise ValidationError('usename or password Error')
