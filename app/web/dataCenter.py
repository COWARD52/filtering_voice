from app.db import db
from app.db.Volume import Volume
from . import web
from flask import render_template, request, Response, json
from flask_login import login_required, current_user
import requests


@web.route('/dataCenter')
@login_required
def dataCenter():
    dolphin = Volume.query.filter_by(attack_class=1).count()
    machine = Volume.query.filter_by(attack_class=2).count()
    win = Volume.query.filter_by(status=2).count()
    cautions = db.session.query(Volume.posi).filter(Volume.status == 1).group_by(Volume.posi).all()
    dict = []
    for caution in cautions:
        if Volume.query.filter_by(status=1, posi=caution.posi).count() < 2:
            continue
        dict.append({
            'posi': str(caution.posi),
            'dolphin': Volume.query.filter_by(status=1, posi=caution.posi, attack_class=1).count(),
            'machine': Volume.query.filter_by(status=1, posi=caution.posi, attack_class=2).count(),
        })
    r = len(dict)
    return render_template('dashboard.html',
                           data={'dolphin': dolphin, 'machine': machine, 'win': win, 'caution': r})


@web.route('/detail')
def detail():
    rank = request.args.get('class');
    if rank == 'dolphin':
        return render_template('detail_dolphin.html')
    elif rank == 'machine':
        return render_template('detail_machine.html')
    elif rank == 'win':
        return render_template('detail_win.html')
    return render_template('detail_caution.html')


@web.route('/loaddolphin')
def loaddolphin():
    dolphins = Volume.query.filter_by(attack_class=1).all()
    dict = []
    for dolphin in dolphins:
        dict.append({
            'longitude': str(dolphin.longitude), 'latitude': str(dolphin.latitude),
            'volume_filename': str(dolphin.volume_filename), 'create_time': str(dolphin.create_time),
            'phone': str(dolphin.phone), 'posi': str(dolphin.posi)
        })
    return Response(json.dumps(dict), mimetype='application/json')


@web.route('/loadmachine')
def loadmachine():
    machines = Volume.query.filter_by(attack_class=2).all()
    dict = []
    for machine in machines:
        dict.append({
            'longitude': str(machine.longitude), 'latitude': str(machine.latitude),
            'volume_filename': str(machine.volume_filename), 'create_time': str(machine.create_time),
            'phone': str(machine.phone), 'posi': str(machine.posi)
        })
    return Response(json.dumps(dict), mimetype='application/json')


@web.route('/loadwin')
def loadwin():
    wins = Volume.query.filter_by(status=2).all()
    dict = []
    for win in wins:
        dict.append({
            'longitude': str(win.longitude), 'latitude': str(win.latitude),
            'attack': '海豚音攻击' if str(win.attack_class) == '1' else '机器学习攻击', 'create_time': str(win.create_time),
            'phone': str(win.phone), 'posi': str(win.posi)
        })
    return Response(json.dumps(dict), mimetype='application/json')


@web.route('/loadcaution')
def loadcaution():
    cautions = db.session.query(Volume.posi).filter(Volume.status == 1).group_by(Volume.posi).all()
    dict = []
    for caution in cautions:
        if Volume.query.filter_by(status=1, posi=caution.posi).count() < 2:
            continue
        dict.append({
            'posi': str(caution.posi),
            'dolphin': Volume.query.filter_by(status=1, posi=caution.posi, attack_class=1).count(),
            'machine': Volume.query.filter_by(status=1, posi=caution.posi, attack_class=2).count(),
        })
    return Response(json.dumps(dict), mimetype='application/json')
