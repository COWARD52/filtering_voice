from . import web
from flask import render_template, jsonify, Response, current_app, request
from flask_login import login_required
from app.db.Volume import Volume
import json
import math


@web.route('/heatmap')
@login_required
def heatmap():
    return render_template('heatmap.html')


@web.route('/getdata')
def getdata():
    precise = request.args.get('precise')
    dict = []
    volumes = Volume.query.all()
    for volume in volumes:
        dict.append({
            'lng': str(volume.longitude), 'count': '1', 'class': volume.attack_class, 'lat': str(volume.latitude)
        })

    if precise:
        return Response(json.dumps(dict), mimetype='application/json')

    i = 0
    while (i < len(dict)):
        j = i + 1
        temp = []
        temp.append(dict[i])
        while (j < len(dict)):
            if dict[j]['class'] == dict[i]['class'] and check_position(dict[i], dict[j]):
                temp.append(dict[j])
                dict.pop(j)
            else:
                j += 1
        dict[i] = sumaverage(temp)
        i += 1
    return Response(json.dumps(dict), mimetype='application/json')


def check_position(point1, point2):
    lng1 = float(point1['lng'])
    lng2 = float(point2['lng'])
    lat1 = float(point1['lat'])
    lat2 = float(point2['lat'])
    lng1 *= 1000000
    lng1 %= 1000000
    lng2 *= 1000000
    lng2 %= 1000000
    lat1 *= 1000000
    lat1 %= 1000000
    lat2 *= 1000000
    lat2 %= 1000000

    distance = math.sqrt((lng1 - lng2) ** 2 + (lat1 - lat2) ** 2)
    if distance < 1100:
        return True
    else:
        return False


def sumaverage(temp):
    i = 0
    Lng = 0
    Lat = 0
    Count = len(temp)
    Class = temp[0]['class']
    while (i < len(temp)):
        Lng += float(temp[i]['lng'])
        Lat += float(temp[i]['lat'])
        i += 1
    Lng /= Count
    Lat /= Count
    return {'lng': str(Lng), 'count': str(Count), 'class': Class, 'lat': str(Lat)}
