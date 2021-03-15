from app.db import db
from app.db.Consumermission import Consumermission
from app.db.Mission import Mission
from app.db.Volume import Volume
from . import web
from flask import render_template, request, Response
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import desc
import json


@web.route('/mission')
@login_required
def mission():
    return render_template('mission.html')


@web.route('/addmission')
def addmission():
    area = request.args.get('area')
    time = request.args.get('time')
    date = request.args.get('date')
    recommend_phones = request.args.get('recommend_phones')
    recommend_voiceasses = request.args.get('recommend_voiceasses')
    recommend_phones = recommend_phones.split(',')
    recommend_voiceasses = recommend_voiceasses.split(',')
    for recommend_phone in recommend_phones:
        for recommend_voiceass in recommend_voiceasses:
            mission = Mission()
            mission.set_attrs({
                'area': area,
                'time': time,
                'date': date,
                'recommend_phone': recommend_phone,
                'recommend_voiceass': recommend_voiceass
            })
            try:
                if Mission.query.filter_by(area=area, time=time, date=date,
                                           recommend_phone=recommend_phone,
                                           recommend_voiceass=recommend_voiceass).first():
                    return '亲，不能重复添加哦'
                db.session.add(mission)
            except Exception as e:
                db.session.rollback()
    db.session.commit()
    return '已发布成功'


@web.route('/missondata')
def missondata():
    yifabu = Mission.query.filter_by().all().__len__()
    chakanrenci = Consumermission.query.filter_by().all().__len__()
    yiqueren = Consumermission.query.filter_by(agree=1).all().__len__()
    yihuishou = Consumermission.query.filter_by(agree=1, huishou=1).all().__len__() \
                + Consumermission.query.filter_by(
        agree=1, huishou=2).all().__len__()
    daihuishou = Consumermission.query.filter_by(agree=1, huishou=0).all().__len__()
    return str(yifabu) + ":" + str(chakanrenci) + ":" + str(yiqueren) + ":" + str(yihuishou) + ":" + str(daihuishou)


@web.route('/realtime')
def realtime():
    volumes = Volume.query.order_by(desc(Volume.create_time)).limit(100).all()
    now = int(datetime.now().timestamp())
    i = 0
    for volume in volumes:
        if abs(volume.create_time - now) < 3:
            i += 1
    return str(i)


@web.route('/newform')
def newform():
    news = Consumermission.query.filter_by(agree=1, huishou=1).limit(4).all()
    result = []
    for new in news:
        mission = Mission.query.filter_by(missionid=new.missionid).first()
        result.append({
            'username': new.phone,
            'area': mission.area,
            'time': mission.date,
            'fankuileibie': '海豚音攻击'
        })
    db.session.commit()
    return Response(json.dumps(result), mimetype='application/json')
