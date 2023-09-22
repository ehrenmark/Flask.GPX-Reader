
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
    tracks = relationship('Track', back_populates='driver')

class Vehicle(db.Model):
    fzid = db.Column(db.Integer, primary_key=True)
    polkz = db.Column(db.String(150))
    vin = db.Column(db.String(150))
    tracks = relationship('Track', back_populates='vehicle')


class Waypoint(db.Model):
    ptid = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    ele = db.Column(db.Float)
    dt = db.Column(db.DateTime)

class Track:
    tid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150))

    fzid = db.Column(db.Integer, db.ForeignKey('vehicle.fzid'))
    vehicle = relationship('Vehicle', back_populates='tracks')

    pid = db.Column(db.Integer, db.ForeignKey('driver.pid'))
    driver = relationship('Driver', back_populates='tracks')

    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
