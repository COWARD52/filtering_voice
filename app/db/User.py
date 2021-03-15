from flask_login import UserMixin
from flask_login import LoginManager

login_manager = LoginManager()
from . import Base
from sqlalchemy import Column, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base, UserMixin):
    phone = Column(String(64), primary_key=True, nullable=False)
    _password = Column('password', String(128), nullable=False)
    privilege = Column(SmallInteger, unique=False, default=3)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def get_id(self):
        return self.phone


@login_manager.user_loader
def get_user(uid):
    return User.query.get(str(uid))
