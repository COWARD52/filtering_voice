from app.web import web
from flask import render_template
from flask_login import login_required


@web.route('/trail')
@login_required
def trail():
    return render_template('trail.html')

@web.route('/sider')
def sider():
    return render_template('sider.html')