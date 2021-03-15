from flask import Flask

from app.db import db
from app.db.Consumermission import Consumermission
import pymysql,secure
from app.db.User import login_manager, User
from app.db.Volume import Volume
from app.web import web
from app import templates
app = Flask(__name__)
app.config.from_object('secure')
app.register_blueprint(web)
app.template_folder = 'app/templates'
app.static_folder = 'app/static'
db.init_app(app)
db.create_all(app=app)

login_manager.init_app(app)
login_manager.login_view = 'web.login'

from threading import Timer


def printHello():
    with app.app_context():
        volumes = Volume.query.filter(Volume.phone != '').all()
        for volume in volumes:
            missions = Consumermission.query.filter_by(agree=1, huishou=0, phone=volume.phone).all()
            for mission in missions:
                if mission:
                    mission.huishou = 1
                    db.session.commit()
    t = Timer(30, printHello)
    t.start()


printHello()

if __name__ == '__main__':
    with app.app_context():
        try:
            user = User()
            data = {'phone': '11111111111', 'password': '123456', 'log': None}
            user.set_attrs(data)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            pass
    print()
    print("物语安-物联网语音安全管家启动成功!")
    print("请在浏览器输入127.0.0.1进行访问，局域网环境下输入本机ip地址也可访问")
    print("初次使用，请确保已安装mysql8.0及以上版本，并需创建名为volume的数据库，连接设置：{端口-3306，用户名-root，密码-54321abc76}")
    print("用户名:11111111111")
    print("密码:123456")
    print()
    app.run(port=app.config['PORT'], host='0.0.0.0', debug=False)

    input()