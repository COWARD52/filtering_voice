from . import web
from flask_login import login_required
from flask import request, jsonify
from app.tool.check_position import check


@web.route('/check_acc', methods=['POST'])
def check_acc():
    phone = request.form['phone']
    longitude = request.form['longitude']
    latitude = request.form['latitude']
    point = check(longitude, latitude).point
    return str(point)
