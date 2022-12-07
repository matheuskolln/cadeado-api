from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# We need to import models after of defining db
from models import User

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
            "status": 'success',
            "user": user.to_dict()
        }, 201

    existent_user = existent_user[0]
    if existent_user.password == password:
        return {
            "status": 'user has been created before',
            "user": existent_user.to_dict(),
        }, 200

    return {
        "status": 'already have a user using this email'
    }, 400

@app.route("/user", methods=['GET'])
def login_user_route():
    email = request.json.get('email')
    password = request.json.get('password')

    user = db.session.execute(select(User).where(User.email == email, User.password == password)).first()

    if user:
        return {
            'status': 'login successful',
            'user': user[0].to_dict()
        }, 200
    return {
        'status': 'bad credentials'
    }, 401
