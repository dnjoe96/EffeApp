from app import db
from datetime import datetime


class Personnel(db.Model):
    __tablename__ = 'personnel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    update_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return '<username {}>'.format(self.username)


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    register_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, lastname, firstname, pasword_hash):
        self.username = username
        self.lastname = lastname
        self.firstname = firstname
        self.password_hash = pasword_hash

    def __repr__(self):
        return '<username {}>'.format(self.username)


class Vehicle(db.Model):
    """Vehicle Model """

    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    chasis_num = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Vehicle {}>'.format(self.vehicle_number)

