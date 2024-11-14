from flask_login import UserMixin
from LandlordRecruitment import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class verification_code():
    def verification_code(self, code):
        self.code = code
        self.create_time = datetime.datetime.now().timestamp()
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    phone_number = db.Column(db.String(16), unique = True)
    email_addr = db.Column(db.String(128), unique = True)
    username = db.Column(db.String(40), unique = True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    is_admin = db.Column(db.Integer, default = 0)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)
    
    def validatePassword(self, password):
        return check_password_hash(self.passwordHash, password)