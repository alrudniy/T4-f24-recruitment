from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

App = Flask("LandlordRecruitment")
App.config.from_pyfile("settings.py")
db = SQLAlchemy(App)
bootstrap = Bootstrap(App)

loginManager = LoginManager(App)
loginManager.login_view = "/login"
loginManager.login_message = "Please login to continue"

from LandlordRecruitment import views, models, extensions
with App.app_context():
    db.create_all()


