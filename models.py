
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()
DB_NAME = "database.db"

db_gpx = SQLAlchemy()
DB_GPX_NAME = "gpx_daten.db"



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Person(db_gpx.Model):
    pid = db_gpx.Column(db_gpx.Integer, primary_key=True)
    nick = db_gpx.Column(db_gpx.String(150))
    name = db_gpx.Column(db_gpx.String(150))
    vorname = db_gpx.Column(db_gpx.String(150))
    email = db_gpx.Column(db_gpx.String(150), unique=True)

class Fahrzeug(db_gpx.Model):
    fzid = db_gpx.Column(db_gpx.Integer, primary_key=True)
    polkz = db_gpx.Column(db_gpx.String(150))
    fahrgestellnummer = db_gpx.Column(db_gpx.String(150))

class Punkt(db_gpx.Model):
    ptid = db_gpx.Column(db_gpx.Integer, primary_key=True)
    lat = db_gpx.Column(db_gpx.Float)
    lon = db_gpx.Column(db_gpx.Float)
    ele = db_gpx.Column(db_gpx.Float)
    dt = db_gpx.Column(db_gpx.DateTime)

class Track:
    tid = db_gpx.Column(db_gpx.Integer, primary_key=True)
    dateiname = db_gpx.Column(db_gpx.String(150))