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

from lib.data.task import varify_login, login, books, get_books

user = {}


class LoginView(MethodView):

    template = 'libr/login.html'

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

            if result.result is not False:

                user = result.result
                result = books.delay(user['number'], user['passwd'])
                result.get()
                result = get_books.delay(user['number'])
                result.get()

                user = result.result
                return render_template(
                    'libr/index.html',
                    user=user)
            else:
                flash('number or password Error!')
                return redirect(url_for('libr.index'))
