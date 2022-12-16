from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    devices = db.relationship('Device', backref='user', lazy=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "devices": [device.to_dict() for device in self.devices]
        }


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    information = db.Column(db.String, unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "information": self.information,
            "owner_id": self.owner
        }
