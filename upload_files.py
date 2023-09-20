from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Waypoint, Track, Vehicle, Driver
from models import db



upload_files = Blueprint('upload_files', __name__)

@upload_files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_files_to_db():


    return render_template("upload_files.html", user=current_user)