from flask_login import UserMixin
from LandlordRecruitment import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    phone_number = db.Column(db.String(16), unique = True)
    email_addr = db.Column(db.String(128), unique = True)
    username = db.Column(db.String(40), unique = True)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    is_admin = db.Column(db.Integer, default = 0)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)
    
    def validatePassword(self, password):
        return check_password_hash(self.passwordHash, password)
    
class Enquiry(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    phone_number = db.Column(db.String(16))
    catagory = db.Column(db.Integer)
    email_addr = db.Column(db.String(128))
    content = db.Column(db.Text)
    created_time = db.Column(db.DateTime)
    replied = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class VerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6))
    expiration_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_usd = db.Column(db.Boolean, default = False)
