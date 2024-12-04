from flask import render_template, redirect, url_for, flash, abort, request, make_response, jsonify
from LandlordRecruitment.models import User, VerificationCode, Enquiry
from flask_login import login_required
from LandlordRecruitment import App, db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
import random
import datetime


string_pool = "0123456789"

@App.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("index"))

@App.route("/")
@App.route("/index")
def index():
    return render_template("index.html")

@App.route("/homeowner_index")
@login_required
def homeowner_index():
    return render_template("homeowner_index.html")

@App.route("/faqs")
@login_required
def faqs():
    return render_template("faqs.html")

@App.route("/roadmap")
@login_required
def roadmap():
    return render_template("roadmap.html")

@App.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")

@App.route("/homeowner_login")
def homeowner_login():
    return render_template("admin_login.html")

@App.route("/send_code", methods = ["POST"])
def send_code():
    if request.method != "POST":
        return {
            "code": -1,
            "msg": "Method not allowed"
        }
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
    
    verification_code = VerificationCode()
    verification_code.code = code
    verification_code.expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
    user = User.query.filter(User.phone_number == phonenumber).first()
    if not user:
        return {
            "code": 2,
            "msg": "User does not exist"
        }
    verification_code.user_id = user.id
    VerificationCode.query.filter(VerificationCode.user_id == user.id).delete()
    try:
        db.session.add(verification_code)
        db.session.commit()
    except Exception as e:
        return {
            "code": 2,
            "msg": f"Database connection error, {e}"
        }
    return {
        "code": 0,
        "msg": "Verification code sent",
        "v_code": code
    }
        
@App.route("/login_password", methods = ["POST"])
def login_password():
    if request.method != "POST":
        return {
            "code": -1,
            "msg": "Method not allowed"
        }
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
    #return render_template("login.html", form = Logmsgrm)

def check_verification_code(id, input_code, expire_time = datetime.timedelta(minutes=15)):
    code = VerificationCode.query.filter(VerificationCode.user_id == id).filter(VerificationCode.is_used == 0).first()
    if not code:
        return False
    now = datetime.datetime.now()
    if now - code.expiration_time > expire_time:
        return False
    if code.code == input_code:
        code.is_used = 1
        db.session.commit()
        return True
    return False


@App.route("/login_code", methods = ["POST"])
def login_code():
    if request.method != "POST":
        return {
            "code": -1,
            "msg": "Method not allowed"
        }
    request_data = request.get_json()
    phone = request_data["phone"]
    code = request_data["code"]
    user = User.query.filter(User.phone_number == phone).first()
    if not user:
        return {
            "code": 1,
            "msg": "Phone number not exist"
        }
    elif not check_verification_code(user.id, code):
        return {
            "code": 2,
            "msg": "Verification code not correct"
        }
    else:
        #flask_login.login_user(user)
        flask_login.login_user(user)
        return {
            "code": 0,
            "msg": "Login success"
        }
        
@App.route("/register", methods = ["POST"])
def register():
    if request.method != "POST":
        return {
            "code": -1,
            "msg": "Method not allowed"
        }
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


@App.route("/create_enquiry", methods = ["POST"])
def create_enquiry():
    if request.method != "POST":
        return {
            "code": -1,
            "msg": "Method not allowed" # Deny non-POST requests
        }

    try:
        request_data = request.get_json()
        category = request_data.get("category")
        phone_number = request_data.get("phone_number")
        email_addr = request_data.get("email_addr")
        username = request_data.get("username") # Get username separately
        content = request_data.get("content")
        replied = 0
    except Exception as e:
        return {
            "code": 1,
            "msg": f"Insufficient parameters, {e}" # Fix typo
        }
    enquiry = Enquiry()
    enquiry.category = category # Fix typo
    enquiry.phone_number = phone_number
    enquiry.email_addr = email_addr
    enquiry.username = username
    enquiry.content = content
    enquiry.replied = replied
    enquiry.created_time = datetime.datetime.now() # Add timestamp

    try:
        db.session.add(enquiry)
        db.session.commit()
    except Exception as e:
        return {
            "code": 2,
            "msg": f"Database error. {e}"
        }
    return {
        "code": 0,
        "msg": "Enquiry created",
        "enquiry_id": enquiry.id # Return enquiry ID
    }

@App.route('/enquiries/<int:enquiry_id>', methods=['GET'])
def get_enquiry(enquiry_id):
    if not enquiry_id:
        return {
            "code": -1,
            "msg": "Enquiry id needed"
        }
    enquiry = Enquiry.query.get(enquiry_id)
    if enquiry:
        return jsonify({
            'id': enquiry.id,
            'phone_number': enquiry.phone_number,
            'category': enquiry.category,
            'email_addr': enquiry.email_addr,
            'username': enquiry.username,
            'content': enquiry.content,
            'created_time': enquiry.created_time.isoformat(),
            'replied': enquiry.replied
        })
    else:
        return {
            'code': 1, 
            'msg': 'Enquiry not found'
        }
