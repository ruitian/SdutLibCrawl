# -*- coding: utf-8 -*-

from lib import db, login_manager
from flask.ext.login import UserMixin
import base64


@login_manager.user_loader
def load_user(id):
    return UserModel.objects(id=id).first()


class UserModel(db.Document, UserMixin):
    username = db.StringField(max_length=12)
    password_encode = db.StringField(max_length=128)

    def __init__(self, username, password):
        self.username = username,
        self.password = password

    @property
    def password(self):
        raise AttributeError(
            'password is not a readable attribute'
        )

    @password.setter
    def generate_password(self, password):
        self.password_encode = base64.b64encode(password)

    @classmethod
    def create_user(self, username, password, **kwargs):
        password = self.generate_password(password)
        return self.objects.create(
            username=username,
            password=password,
            **kwargs
        )
        self.save()

    meta = {
        'collection': 'User'
    }
