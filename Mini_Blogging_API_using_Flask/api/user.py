from flask import Blueprint, request, jsonify, Response
from flask_login import login_user, logout_user, current_user, LoginManager
from models.models import db, User
import bcrypt
import random
import os
import requests
from .response import custom_response
from http import HTTPStatus as status

# Blueprint
user = Blueprint('user', __name__)
login_manager = LoginManager()

#---- User loader for Flask-Login Session ----
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#------ Sign Up - Create Account ---
@user.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    mobile_number = data.get('mobileNumber')
    user_type = data.get('userType', 'user')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return custom_response("fail", message="User already exists", status_code=status.CONFLICT)

    #Encrypted the password for better individual data security
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = User(
        username=username,
        password=hashed_password,
        firstName=first_name,
        lastName=last_name,
        email=email,
        mobileNumber=mobile_number,
        userType=user_type,
        activeFlag=True
    )
    db.session.add(new_user)
    db.session.commit()

    return custom_response("success", message="User registered successfully", status_code=status.CREATED)

#---- Login with every possible scenarios with encrypted password. ----
@user.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username:
            return custom_response("fail", message="Username required", status_code=status.BAD_REQUEST)

        if not password:
            return custom_response("fail", message="Password required", status_code=status.BAD_REQUEST)

        user = User.query.filter(
            (User.username == username) | (User.email == username) | (User.mobileNumber == username)
        ).first()

        if user:
            if not user.activeFlag:
                return custom_response("fail", message="Account on hold, please contact the support team.", data=None, status_code=status.FORBIDDEN)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                login_user(user)
                user_data = {key: value for key, value in user.__dict__.items() if key not in ['_sa_instance_state', 'password', 'otp']}
                return custom_response("success", data=user_data, message="Logged in successfully")

            return custom_response("fail", message="Invalid Password", data=None, status_code=status.UNAUTHORIZED)
        else:
            return custom_response("fail", message="User-Id doesn't exist!", data=None, status_code=status.NOT_FOUND)

    except Exception as e:
        print(e)
        return custom_response("fail", message="Something went wrong!", data=None, status_code=status.INTERNAL_SERVER_ERROR)

#----- Logout session ---------
@user.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return custom_response("success", message="Logged out successfully")


#--- Random 4 digit otp generation for forget password ---
def generate_otp(length=4):
    return ''.join(random.choices('0123456789', k=length))


# Request OTP for now it'll get in response
# For OTP Mobile we'll have to verify it TRAI and register the company there.
# Also alternately we can do SMTP email for OTP.
@user.route('/request-otp', methods=['POST'])
def request_otp():
    data = request.json
    mobile = data.get('mobileNumber')
    user = User.query.filter_by(mobileNumber=mobile).first()
    if not user:
        return custom_response("fail", message="Mobile number not registered", status_code=status.NOT_FOUND)

    otp = generate_otp()
    print(f"Generated OTP for {mobile}: {otp}")  # For development/testing only
    user.otp = bcrypt.hashpw(otp.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.session.commit()

    return custom_response("success", message=f"OTP generated : {otp}")


#---- Forget Password ----
@user.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    mobile = data.get('mobileNumber')
    otp_entered = data.get('otp')
    new_password = data.get('newPassword')

    user = User.query.filter_by(mobileNumber=mobile).first()
    if not user:
        return custom_response("fail", message="User not found", status_code=status.NOT_FOUND)

    if not bcrypt.checkpw(otp_entered.encode('utf-8'), user.otp.encode('utf-8')):
        return custom_response("fail", message="Invalid OTP", status_code=status.UNAUTHORIZED)

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password = hashed_password
    user.otp = None
    db.session.commit()

    return custom_response("success", message="Password updated successfully")
