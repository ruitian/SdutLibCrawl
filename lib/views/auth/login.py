# -*- coding: utf-8 -*-

from flask import (  # noqa
    request,
    redirect,
    render_template,
    flash,
    url_for
)
from flask.views import MethodView
from lib.forms import LoginForm

from lib.data.task import account_init


class LoginView(MethodView):

    template = 'auth/login.html'

    def get(self):
        form = LoginForm()
        return render_template(self.template, form=form)

    def post(self):
        form = LoginForm()
        if not form.validate():
            return render_template(self.template, form=form)
        form.generate_account()
        account_init.delay(
            form.username.data,
            form.password.data,
        )
        flash('Login Successful')
        return redirect(url_for('index.index'))
