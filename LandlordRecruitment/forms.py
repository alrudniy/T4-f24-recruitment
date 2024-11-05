from flask_wtf import FlaskForm
from wtforms.validators import *
from wtforms import *

class RegisterForm(FlaskForm):
    username = StringField("Username",
                           validators = [DataRequired("Please enter your username here"),
                                                Length(6, 20, message = "6-20 chars"),
                                                Regexp("^\w+$", message = "It can only contain 0-9, a-z and _")])
    password = PasswordField("Password",
                             validators = [DataRequired("Please enter your password"),
                                                 Length(8, 20, message = "8-20 chars"),
                                                 Regexp("^\w+$", message = "It can only contain 0-9, a-z and _")])
    repPassword = PasswordField("Repeat Password",
                                validators = [DataRequired("Please repeat your password"),
                                              Length(1, 20),
                                              EqualTo("password", "Password not the same")])
    submit = SubmitField("Submit")

    def validate_username(form, field):
        username = field.data
        for ch in nickname_data:
            if not (form.is_char(ch) or ch.isalnum() or ch == '-'):
                raise ValidationError('昵称中只能包含汉字、数字、字母与下划线')
        from majcalc.models import User
        user = User.query.filter(User.nickname == field.data).first()
        if user:
            raise ValidationError('昵称已存在')