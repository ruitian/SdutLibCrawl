# -*- coding: utf-8 -*-

from lib import db, login_manager
from flask.ext.login import UserMixin
import base64


@login_manager.user_loader
def load_user(id):
    return UserModel.objects(id=id).first()


class UserModel(db.Document, UserMixin):
    id = db.SequenceField(primary_key=True)
    username = db.StringField(max_length=128)
    password = db.StringField(max_length=128)

    @staticmethod
    def generate_password(password):
        password_encode = base64.b64encode(password)
        return password_encode

    @classmethod
    def create_user(cls, username, password):
        password = cls.generate_password(password)
        return cls.objects.create(
            username=username,
            password=password
        )

    meta = {
        'collection': 'User'
    }
