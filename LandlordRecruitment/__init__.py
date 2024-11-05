from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy

App = Flask("LandlordRecruitment")

App.config.from_pyfile("settings.py")

from LandlordRecruitment import views
