from . import web
from flask import request, render_template, url_for, redirect, Response
import json
from app.form.auth import Authform, Loginform
from app.db import db
from app.db.User import User
from flask_login import login_user, logout_user, login_required


@web.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        data = {}
        formerror = request.args.get('data')
        if not formerror:
            pass
        else:
            formerror = formerror.split(':')
            while len(formerror) > 0:
                key = formerror.pop(0)
                value = formerror.pop(0)
                data[key] = value
        return render_template('register.html', formerror=data, sign=True)
    else:
        form = Authform(request.form)
        if form.validate():
            try:
                user = User()
                user.set_attrs(form.data)
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print(e)
        else:
            data = []
            for key, value in form.errors.items():
                value[-1] = key + ':' + value[-1]
                data.extend(value)
            if request.form.get('sign') == '-1':
                return url_for('web.register') + ',' + ','.join(data)
            return url_for('web.login') + ',' + ','.join(data)
    return url_for('web.login')


@web.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        data = {}
        if request.args.get('next'):
            data['password'] = 'Please log in'
        formerror = request.args.get('data')
        if not formerror:
            pass
        else:
            formerror = formerror.split(':')
            data = {
                formerror[0]: formerror[1]
            }
        return render_template('register.html', formerror=data)
    else:
        form = Loginform(request.form)
        if form.validate():
            user = User.query.get(form.phone.data)
            login_user(user)
        else:
            data = []
            for key, value in form.errors.items():
                value[-1] = key + ':' + value[-1]
                data.extend(value)
            return url_for('web.login') + ',' + ','.join(data)
        next = request.args.get('next')
        if not next or not next.startswith('/'):
            next = url_for('web.heatmap')
    return next


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.login'))


@web.route('/profile')
@login_required
def profile():
    return 'hello world'


@web.route('/privilege', methods=['GET', 'POST'])
@login_required
def privilege():
    if request.method == 'GET':
        return render_template('privilege.html')
    else:
        try:
            for user in request.json:
                User.query.get(user['phone']).privilege = user['privilege']
        except Exception as e:
            print(e)
        db.session.commit()
        return 'ok'


@web.route('/loaduser')
def loaduser():
    users = User().query.all()
    dict = []
    for user in users:
        dict.append({
            'name': str(user.phone), 'privilege': user.privilege
        })
    return Response(json.dumps(dict), mimetype='application/json')
