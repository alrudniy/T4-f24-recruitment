from flask import render_template, redirect, url_for, flash, abort, request, make_response, jsonify
from LandlordRecruitment.models import User, Verification_code
#import LandlordRecruitment.models
from LandlordRecruitment import App, db
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
import random
import datetime

string_pool = "0123456789"
verification_code = dict()

@App.route("/send_code", methods = ["POST"])
def send_code():
    if request.method == "POST":
        try:
            request_data = request.get_json()
            phonenumber = request_data["phone"]
        except Exception as e:
            return {
                "code": 1,
                "msg": f"Insufficent parameters, {e}"
            }
        code = ""
        for _ in range(6):
            code += random.sample(string_pool, 1)[0]
        verification_code[phonenumber] = Verification_code(code)
        # TODO: call 3rd party api to send the code
        return {
            "code": 0,
            "msg": "Verification code sent",
            "code": code
        }
    else:
        return {
            "code": -1,
            "msg": "invalid method"
        }
        
@App.route("/login_password", methods = ["POST"])
def login_password():
    if request.method == "POST":
        request_data = request.get_json()
        username = request_data["username"]
        password = request_data["password"]
        user = User.query.filter(User.username == username).first()
        if not user:
            return {
                "code": 1,
                "msg": "Account not exist"
            }
        elif not check_password_hash(user.password_hash, password):
            return {
                "code": 2,
                "msg": "Password or username not correct"
            }
        else:
            #flask_login.login_user(user)
            return {
                "code": 0,
                "msg": "Login success"
            }
    else:
        return {
            "code": -1,
            "msg": "invalid method"
        }
    #return render_template("login.html", form = Logmsgrm)

def check_verification_code(phone, code, expire_time = 15 * 60 * 1000):
    db_code = verification_code.get(phone, None)
    if not db_code:
        return False
    now = datetime.datetime.now().timestamp()
    if now - db_code.create_time > expire_time:
        return False
    return  db_code.code == code
        
@App.route("/login_code", methods = ["POST"])
def login_code():
    if request.method == "POST":
        request_data = request.get_json()
        phone = request_data["phone"]
        code = request_data["code"]
        user = User.query.filter(User.phone_number == phone).first()
        if not user:
            return {
                "code": 1,
                "msg": "Phone number not exist"
            }
        elif not check_verification_code(phone, code):
            return {
                "code": 2,
                "msg": "Verification code not correct"
            }
        else:
            #flask_login.login_user(user)
            return {
                "code": 0,
                "msg": "Login success"
            }
    else:
        return {
            "code": -1,
            "msg": "invalid method"
        }
        
@App.route("/register", methods = ["POST"])
def register():
    if request.method == "POST":
        try:
            request_data = request.get_json()
            phone = request_data["phone"]
            first_name = request_data["firstName"]
            last_name = request_data["lastName"]
            email = request_data["email"]
            password = request_data["password"]
            username = request_data["username"]
        except Exception as e:
            return {
                "code": 1,
                "msg": f"Insufficent parameters, {e}"
            }
            
        new_user = User()
        new_user.phone_number = phone
        new_user.password_hash = generate_password_hash(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email_addr = email
        new_user.username = username
        new_user.is_admin = False
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return {
                "code": 2,
                "msg": f"Database connection error, {e}"
            }
        return {
            "code": 0,
            "msg": "Success"
        }
    else:
        return {
            "code": -1,
            "msg": "invalid method"
        }