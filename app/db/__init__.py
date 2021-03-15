from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger
from datetime import datetime

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer, nullable=False)
    status = Column(SmallInteger, default=1, nullable=False)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, datas):
        for key, value in datas.items():
            if hasattr(self, key):
                setattr(self, key, value)


from . import Volume, User, Consumer, Consumerattack, Mission, Consumermission
