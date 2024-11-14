from flask import render_template, redirect, url_for, flash, abort, request, make_response, jsonify
from LandlordRecruitment.models import User, verification_code
from LandlordRecruitment import App, db
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
import json
import random
import datetime

string_pool = "0123456789"
verification_code = {}

@App.route("/send_code", methods = ["POST"])
def send_code():
    if request.method == "POST":
        request_data = request.get_json()
        phonenumber = request_data["phone"]
        code = ""
        for _ in range(6):
            code += random.sample(string_pool, 1)
        verification_code[phonenumber] = verification_code(code)
        # TODO: call 3rd party api to send the code
        return {
            "code": 0,
            "info": "Verification code sent"
        }
        
@App.route("/login_password", methods = ["POST"])
def login_password():
    if request.method == "POST":
        username = request.form["phoneNumber"]
        password = request.form["password"]
        user = User.query.filter(User.username == username).first()
        if not user:
            return {
                "code": 1,
                "info": "Account not exist"
            }
        elif not check_password_hash(user.password, password):
            return {
                "code": 2,
                "info": "Password or username not correct"
            }
        else:
            flask_login.login_user(user)
            return {
                "code": 0,
                "info": "Login success"
            }
    #return render_template("login.html", form = LoginForm)

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
        data = request.get_json()
        phone = data["phone"]
        code = data["code"]
        user = User.query.filter(User.phone_number == phone).first()
        if not user:
            return {
                "code": 1,
                "info": "Phone number not exist"
            }
        elif not check_verification_code(phone, code):
            return {
                "code": 2,
                "info": "Verification code not correct"
            }
        else:
            flask_login.login_user(user)
            return {
                "code": 0,
                "info": "Login success"
            }
        
@App.route("/register", methods = ["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        phone = data["phone"]
        first_name = data["firstName"]
        last_name = data["lastName"]
        email = data["email"]
        new_user = User()
        new_user.phone_number = phone
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email_addr = email
        new_user.is_admin = False
        db.session.add(new_user)
        db.session.commit()
        return {
            "code": 0,
            "info": "Success"
        }