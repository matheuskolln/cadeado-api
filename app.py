from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt
from sqlalchemy import select


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'th3b3stc4d34d0s3cretke1'

db = SQLAlchemy(app)
migrate = Migrate(app, db)



# We need to import models after of defining db
from models import Log, User

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']

       if not token:
           return jsonify({'message': 'A valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(id=data['user_id']).first()
       except:
           return jsonify({'message': 'Token is invalid'})

       return f(current_user, *args, **kwargs)
   return decorator

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/user", methods=['POST'])
def create_user_route():
    email = request.json.get('email')
    password = request.json.get('password')

    existent_user = db.session.execute(select(User).where(User.email == email)).first()
    if not existent_user:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return {
            "message": 'success',
            "user": user.to_dict()
        }, 201

    existent_user = existent_user[0]
    if existent_user.password == password:
        return {
            "message": 'user has been created before',
            "user": existent_user.to_dict(),
        }, 200

    return {
        "message": 'already have a user using this email'
    }, 400

@app.route("/user", methods=['GET'])
def login_user_route():
    email = request.json.get('email')
    password = request.json.get('password')

    user: User = db.session.execute(select(User).where(User.email == email, User.password == password)).first()[0]
    if user:
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=48)}, app.config['SECRET_KEY'])
        return {
            'message': 'login successful',
            'user': user.to_dict(),
            'token': token,
        }, 200
    return {
        'message': 'bad credentials'
    }, 401

@app.route("/user/log", methods=["POST"])
@token_required
def add_log(user):
    log_info = request.json
    log = Log(**log_info, user_id=user.id, datetime=datetime.utcnow())
    db.session.add(log)
    db.session.commit()

    return {
        'message': 'log added',
        'log': log.to_dict()
    }, 201

@app.route("/user/logs", methods=["GET"])
@token_required
def get_logs(user):
    return {
        "logs": [log.to_dict() for log in user.logs]
    }, 200
