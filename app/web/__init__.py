from flask import Blueprint, redirect

web = Blueprint('web', __name__)

from . import auth, check_acc, heatmap, dataCenter, mission, trail, user
from flask_login import current_user


@web.route('/')
def home():
    if current_user:
        return redirect('/heatmap')
    return redirect('/login')
