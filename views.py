from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask import session
from models import User, Fahrzeug
from models import db
import json
import random
from sqlalchemy import func


views = Blueprint('views', __name__)





@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    username = current_user.first_name

    return render_template("home.html", user=current_user, username=username)

@views.route('/map', methods=['GET', 'POST'])
@login_required
def map():

    return render_template("map.html", user=current_user)


@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():

    return render_template("upload_files.html", user=current_user)


@views.route('/upload_driver', methods=['GET', 'POST'])
@login_required
def upload_driver():


    return render_template("upload_driver.html", user=current_user)

