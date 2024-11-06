from flask_login import UserMixin
from LandlordRecruitment import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email_addr = db.Column(db.String(128), unique = True)
    #nickname = db.Column(db.String(128), unique = True)
    username = db.Column(db.String(40), unique = True)
    password_hash = db.Column(db.String(128))
#    avatar = db.Column(db.String(128), default = "defaultAvatar.png")
    first_mame = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    is_admin = db.Column(db.Integer)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)
    
    def validatePassword(self, password):
        return check_password_hash(self.passwordHash, password)