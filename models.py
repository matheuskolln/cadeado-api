from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    logs = db.relationship('Log', backref='user', lazy=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "logs": [log.to_dict() for log in self.logs]
        }


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    serviceUUID = db.Column(db.String, nullable=False)
    characteristicUUID = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    smartphone_name = db.Column(db.String, nullable=False)
    esp_name = db.Column(db.String, nullable=False)
    esp_mac = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'serviceUUID': self.serviceUUID,
            'characteristicUUID': self.characteristicUUID,
            'state': self.state,
            'smartphone_name': self.smartphone_name,
            'esp_name': self.esp_name,
            'esp_mac': self.esp_mac,
            'datetime': self.datetime,
            'user_id': self.user_id,
        }
