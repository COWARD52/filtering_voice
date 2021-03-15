from . import web
from flask import request
from flask import current_app
import os
from app.db import db
from app.db.Volume import Volume
from app.tool import predict
import random, requests


@web.route('/getWav', methods=['POST'])
def getWav():
    phone = request.form['phone']
    f = request.files['fileField']
    longitude = request.form['longitude']
    latitude = request.form['latitude']
    f_name = f.filename
    f_ext = f_name.split('.')[-1]
    filename = os.path.join(current_app.config['WAVFILE_PATH'], f_name)
    f.save(filename)
    attack_class = predict.get(filename)
    if attack_class:
        try:
            r = requests.get(
                "http://api.map.baidu.com/geocoder/v2/?location=" + str(latitude) + "," + str(
                    longitude) + "&output=json&ak=gdKRvXNF4CvRD04YVRnwUuATXi33Doeg")
            volume = Volume()
            datas = {
                'volume_filename': filename,
                'attack_class': attack_class,
                'longitude': longitude,
                'latitude': latitude,
                'phone': phone,
                'posi': r.json()['result']['formatted_address']
            }
            volume.set_attrs(datas)
            db.session.add(volume)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    return str(attack_class)


@web.route('/ss')
def homed():
    for i in range(200):
        volume = Volume()
        datas = {
            'volume_filename': str(i + 1000) + '.wav',
            'attack_class': random.randint(1, 2),
            'longitude': random.uniform(104.084781, 104.092973),
            'latitude': random.uniform(30.66229, 30.672043),
            'phone': '15328221047'
        }
        volume.set_attrs(datas)
        db.session.add(volume)
        db.session.commit()
    return 'ok'



