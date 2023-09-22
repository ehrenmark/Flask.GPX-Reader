from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Waypoint, Track, Vehicle, Driver
from models import db



upload_files = Blueprint('upload_files', __name__)

@upload_files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_files_to_db():
    driver_list = get_drivers()
    vehicle_list = get_vehicles()


    return render_template("upload_files.html",
                           user=current_user,
                           driver_list=driver_list,
                           vehicle_list=vehicle_list)


def get_drivers():
    drivers = Driver.query.all()
    driver_list = []
    for driver in drivers:
        driver_dict = {
            'pid': driver.pid,
            'nick': driver.nick,
            'surname': driver.surname,
            'forename': driver.forename,
            'email': driver.email
        }
        driver_list.append(driver_dict)
    return driver_list

def get_vehicles():
    vehicles = Vehicle.query.all()
    vehicle_list = []
    for vehicle in vehicles:
        vehicle_dict = {
            'fzid': vehicle.fzid,
            'polkz': vehicle.polkz,
            'vin': vehicle.vin
        }
        vehicle_list.append(vehicle_dict)
    return vehicle_list
