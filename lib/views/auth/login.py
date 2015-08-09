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

from lib.data.task import account_init, test
from lib.models import UserModel, AccountItem
from celery.result import AsyncResult


class LoginView(MethodView):

    template = 'auth/login.html'

    def get(self):
        form = LoginForm()
        return render_template(self.template, form=form)

    def post(self):
        form = LoginForm()
        if not form.validate():
            return render_template(self.template, form=form)

        user = UserModel.objects(username=form.username.data).first()
        if user is None:
            form.generate_user()
            account = form.generate_account()
            account.save()

            UserModel.objects.update(library=account)

        account_init.delay(
            form.username.data,
            form.password.data)
        result = test.delay(3, 3)
        print account_init.id
        if result.ready():
            print 'has run'
            if result.successful():
                print 'ok!!!'
            else:
                if isinstance(result.result, Exception):
                    print "Task failed due to raising an exception"
                    raise result.result
                else:
                    print "Task failed without raising exception"
        else:
            print "Task has not yet run"

        content = AccountItem.objects(username=form.username.data).first()
        if content.status == 'False':
            flash('Error!')
            return redirect(url_for('auth.login'))
        else:
            flash(u'登陆成功！')
        return redirect(url_for('index.index'))
