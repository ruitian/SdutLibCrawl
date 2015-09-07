# -*- coding: utf-8 -*-

from lib import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from lib.models.role import RoleModel
from .role import Permission
# import base64
from mongoengine import NULLIFY, DENY  # noqa


@login_manager.user_loader
def load_user(id):
    return UserModel.objects(id=id).first()


class VarifyItem(db.Document):
    number = db.StringField(max_length=128)
    passwd = db.StringField(max_length=128)
    status = db.StringField(default='False')
    meta = {
        'collection': 'VarifyItem'
    }


class AccountItem(db.Document):
    id = db.SequenceField(primary_key=True)
    number = db.StringField(max_length=128)
    passwd = db.StringField(max_length=128)
    name = db.StringField(max_length=64)
    books = db.DictField()
    meta = {
        'collection': 'AccountItem',
        # 'indexes': ['id', 'barcode']
    }


class UserModel(UserMixin, db.Document):
    id = db.SequenceField(primary_key=True)
    username = db.StringField(max_length=128)
    password = db.StringField(max_length=128)
    role = db.ReferenceField(RoleModel, reverse_delete_rule=DENY)
    # library = db.ReferenceField(VarifyItem, reverse_delete_rule=NULLIFY)

    @staticmethod
    def generate_password(password):
        password = generate_password_hash(password)
        return password

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, username, password):
        password = cls.generate_password(password)
        return cls.objects.create(
            username=username,
            password=password
        )

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    meta = {
        'collection': 'User'
    }
