import requests

from app.db import db
from app.db.Consumer import Consumer
from app.db.Consumerattack import Consumerattack
from app.db.Consumermission import Consumermission
from app.db.Mission import Mission
from app.db.Volume import Volume
from app.form.auth import enrollform
from app.web import web
from flask import request, jsonify
import time


@web.route('/enroll', methods=['POST'])
def enroll():
    form = enrollform(request.form)
    if form.validate():
        try:
            consumer = Consumer()
            consumer.set_attrs(form.data)
            db.session.add(consumer)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return "0"
    else:
        return form.errors['phone'][0]


@web.route('/getmission', methods=['POST'])
def getmission():
    phone = request.form['phone']
    consumer = Consumer.query.get(phone)
    missions = Mission.query.filter_by(recommend_phone=consumer.phonetype,
                                       recommend_voiceass=consumer.voiceassistance).all()
    i = 0
    quchu = []
    for mission in missions:
        if Consumermission.query.filter_by(missionid=mission.missionid, phone=phone).first():
            quchu.append(i)
        i += 1
    dict = []
    i = 0
    for mission in missions:
        if i in quchu:
            i += 1
            continue
        dict.append({
            'Area': mission.area,
            'date': mission.date,
            'time': mission.time,
            'missionid': mission.missionid
        })
        i += 1
    return jsonify(dict)


@web.route('/agree_disargee', methods=['POST'])
def agree_disargee():
    phone = request.form['phone']
    missionid = request.form['missionid']
    agree = request.form['agree']
    consumermission = Consumermission()
    consumermission.set_attrs({
        'missionid': missionid,
        'phone': phone,
        'agree': agree,
        'huishou': 0
    })
    try:
        db.session.add(consumermission)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return 'ok'

@web.route('/ha')
def ha():
    volumes = Volume.query.filter().all()
    for volume in volumes:
        r = requests.get(
            "http://api.map.baidu.com/geocoder/v2/?location=" + str(volume.latitude) + "," + str(
                volume.longitude) + "&output=json&ak=gdKRvXNF4CvRD04YVRnwUuATXi33Doeg")
        volume.posi = r.json()['result']['formatted_address']
    db.session.commit()