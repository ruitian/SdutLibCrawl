# -*- coding: utf-8 -*-
from flask import (  # noqa
    request,
    redirect,
    render_template,
    flash,
    url_for
)
from flask.views import MethodView
# from flask.ext.login import login_user
from lib.forms import LoginForm

from lib.data.task import varify_login, login


class LoginView(MethodView):

    template = 'auth/login.html'

    def get(self):
        form = LoginForm()
        return render_template(self.template, form=form)

    def post(self):
        form = LoginForm()
        if not form.validate():
            return render_template(self.template, form=form)

        result = login.delay(
            form.username.data,
            form.password.data
        )
        result.get()

        if result.state == 'SUCCESS':
            result = varify_login.delay(form.username.data)
            result.get()
            print result.result
            if result.result:
                flash('login SUCCESS')
                return redirect(url_for('index.index'))
            else:
                flash('number or password Error!')
                return redirect(url_for('auth.login'))
