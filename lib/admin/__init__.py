# -*- coding: utf-8 -*-
from flask import redirect, url_for, request  # noqa
from flask.ext.login import current_user
from flask.ext.admin import Admin, AdminIndexView as _AdminIndexView


class AdminIndexView(_AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated() and \
            current_user.is_administrator

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('auth.login', next=request.url))

admin = Admin(
    name='SdutLib Admin',
    template_mode='admin',
    index_view=AdminIndexView(name='Index'),
)

from .role import *  # noqa
