
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

db = SQLAlchemy()
DB_NAME = "database.db"



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Driver(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    forename = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)

class Vehicle(db.Model):
    fzid = db.Column(db.Integer, primary_key=True)
    polkz = db.Column(db.String(150))
    vin = db.Column(db.String(150))


class Waypoint(db.Model):
    ptid = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    ele = db.Column(db.Float)
    dt = db.Column(db.DateTime)
    tid = db.Column(db.Integer, db.ForeignKey('track.tid'), nullable=False)

class Track(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150))

    fzid = db.Column(db.Integer, db.ForeignKey('vehicle.fzid'), nullable=False)

    pid = db.Column(db.Integer, db.ForeignKey('driver.pid'), nullable=False)

    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
