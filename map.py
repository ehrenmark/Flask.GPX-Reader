from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Waypoint, Track, Vehicle, Driver
from models import db
from upload_files import get_drivers, get_vehicles
from sqlalchemy import or_, and_

map = Blueprint('map', __name__)


@map.route('/map', methods=['GET', 'POST'])
@login_required
def map_function():
    waypoints_serialized = 0
    driver_list = get_drivers()
    vehicle_list = get_vehicles()

    if request.method == 'POST':
        driver = request.form["driver"]
        vehicle = request.form["vehicle"]
        start_date = request.form["datepicker_start"]
        end_date = request.form["datepicker_end"]

        result = db.session.query(Track.tid).filter(
            and_(
                or_(
                    and_(
                        Track.start_time <= start_date,
                        Track.end_time >= end_date
                    ),
                    and_(
                        Track.start_time >= start_date,
                        Track.start_time <= end_date
                    ),
                    and_(
                        Track.end_time >= start_date,
                        Track.end_time <= end_date
                    )
                ),
                Track.pid == driver,
                Track.fzid == vehicle
            )
        ).all()
        tid_list = [row[0] for row in result]

        waypoints_by_tid = {}

        for tid in tid_list:
            waypoints = db.session.query(Waypoint).filter(Waypoint.tid == tid).all()

            waypoints_by_tid[tid] = waypoints
            waypoints_serialized = {tid: [serialize_waypoint(waypoint) for waypoint in waypoints] for tid, waypoints in
                                    waypoints_by_tid.items()}

        return render_template("map.html",
                               user=current_user,
                               driver_list=driver_list,
                               vehicle_list=vehicle_list,
                               waypoints_by_tid=waypoints_serialized)

    return render_template("map.html",
                           user=current_user,
                           driver_list=driver_list,
                           vehicle_list=vehicle_list)


def serialize_waypoint(waypoint):
    return {
        "ptid": waypoint.ptid,
        "lat": waypoint.lat,
        "lon": waypoint.lon,
        "ele": waypoint.ele,
        "dt": waypoint.dt.strftime("%Y-%m-%d %H:%M:%S"),  # Beispiel: Datum in ein Textformat umwandeln
        "tid": waypoint.tid
    }
