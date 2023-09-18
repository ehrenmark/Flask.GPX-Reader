
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()
DB_NAME = "database.db"



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Person(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(150))
    name = db.Column(db.String(150))
    vorname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)

class Fahrzeug(db.Model):
    fzid = db.Column(db.Integer, primary_key=True)
    polkz = db.Column(db.String(150))
    fahrgestellnummer = db.Column(db.String(150))


class Punkt(db.Model):
    ptid = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    ele = db.Column(db.Float)
    dt = db.Column(db.DateTime)

class Track:
    tid = db.Column(db.Integer, primary_key=True)
    dateiname = db.Column(db.String(150))