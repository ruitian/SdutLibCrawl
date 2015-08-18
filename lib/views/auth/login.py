# -*- coding: utf-8 -*-

from flask.ext.login import login_user
from flask import (  # noqa
    render_template,
    redirect,
    url_for,
    flash
)
from lib.forms import LoginForm
from flask.views import MethodView


class LoginView(MethodView):

    template = 'auth/login.html'

    def get(self):
        form = LoginForm()
        return render_template(self.template, form=form)

    def post(self):
        form = LoginForm()
        if not form.validate():
            return render_template(self.template, form=form)
        login_user(form.user)
        flash('login success')
        return redirect(url_for('admin.index'))
