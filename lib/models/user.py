# -*- coding: utf-8 -*-

from lib import db, login_manager
# from flask.ext.login import UserMixin
import base64
from mongoengine import NULLIFY


@login_manager.user_loader
def load_user(id):
    return AccountItem.objects(id=id).first()


class AccountItem(db.Document):
    username = db.StringField(max_length=128)
    password = db.StringField(max_length=128)
    status = db.StringField(default='False')
    books = db.DictField()
    meta = {
        'collection': 'AccountItem'
    }


class UserModel(db.Document):
    id = db.SequenceField(primary_key=True)
    username = db.StringField(max_length=128)
    password = db.StringField(max_length=128)
    library = db.ReferenceField(AccountItem, reverse_delete_rule=NULLIFY)

    @staticmethod
    def generate_password(password):
        password_encode = base64.b64encode(password)
        return password_encode

    @classmethod
    def create_user(cls, username, password, **kwargs):
        password = cls.generate_password(password)
        return cls.objects.create(
            username=username,
            password=password,
            **kwargs
        )

    meta = {
        'collection': 'User'
    }
