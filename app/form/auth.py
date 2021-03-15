from wtforms import Form, StringField, PasswordField, ValidationError, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired

from app.db.Consumer import Consumer
from app.db.User import User


class Loginform(Form):
    phone = StringField(validators=[DataRequired('phone cannot null'), Length(11, 64, 'length at least be eleven')])
    password = PasswordField(validators=[DataRequired('password cannot null'), Length(6, 32, 'length at least be six')])

    def validate_password(self, password):
        user = User.query.get(self.phone.data)
        if user and user.check_password(password.data):
            pass
        else:
            raise ValidationError('phone or password is incorrect')


class Authform(Loginform):
    log = IntegerField()

    def validate_password(self, password):
        pass

    def validate_phone(self, phone):
        if User.query.get(phone.data):
            raise ValidationError('phone is enrolled')


class enrollform(Form):
    phone = StringField(validators=[DataRequired('电话不能为空'), Length(11, 11, '电话格式不正确')])
    phonetype = StringField(validators=[DataRequired('电话类型不能为空')])
    voiceassistance = StringField(validators=[DataRequired('语音助手不能为空')])

    def validate_phone(self, phone):
        if Consumer.query.get(phone.data):
            raise ValidationError('电话号码已注册')
