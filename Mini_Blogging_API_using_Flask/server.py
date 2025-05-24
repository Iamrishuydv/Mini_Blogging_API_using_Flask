from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from models.models import db, User


# Load .env
load_dotenv() 


#----- Initialize app ----
app = Flask(__name__) 
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#----- CORS for routing -----
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


#----- DB initializing -----
db.init_app(app)



#----- Login manager for session based auth ----
login_manager = LoginManager(app)


#---- Auth -----
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#----- Health check route to check your server is up and running -----
@app.route('/hc', methods=['GET'])
def hc():
    return {"success": True}




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
