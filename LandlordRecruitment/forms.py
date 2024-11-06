from flask_wtf import FlaskForm
from wtforms.validators import *
from wtforms import *

class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators = [DataRequired("Please enter your username here"),
                                                Length(6, 20, message = "6-20 chars"),
                                                Regexp("^\w+$", message = "It can only contain 0-9, a-z and _")])
    password = PasswordField("Password",
                             validators = [DataRequired("Please enter your password"),
                                                 Length(8, 20, message = "8-20 chars"),
                                                 Regexp("^\w+$", message = "It can only contain 0-9, a-z and _")])
    """    
    repPassword = PasswordField("Repeat Password",
                                validators = [DataRequired("Please repeat your password"),
                                              Length(1, 20),
                                              EqualTo("password", "Password not the same")])
    """
    submit = SubmitField("Submit")

