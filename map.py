from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Waypoint, Track, Vehicle, Driver
from models import db
from upload_files import get_drivers, get_vehicles
from sqlalchemy import or_, and_
import geojson
import json

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

        if driver is None or vehicle is None or start_date == '' or end_date == '':
            flash('Eingabe nicht vollständig!', 'error')
            return redirect(url_for('map.map_function'))

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
        waypoints_by_tid_for_mapbox = {}

        for tid in tid_list:
            waypoints = db.session.query(Waypoint).filter(Waypoint.tid == tid).all()

            # Filtere die Waypoints, um nur jeden zweiten Waypoint aufzunehmen

            # Erstelle waypoints_serialized mit den gefilterten Waypoints
            waypoints_serialized = {tid: [serialize_waypoint(waypoint) for waypoint in waypoints]}
            waypoints_by_tid[tid] = waypoints_serialized[tid]

            new_list = [[item.lon, item.lat] for item in waypoints]

            waypoints_by_tid_for_mapbox[tid] = new_list


        first_last_coordinates = {}  # A dictionary to store first and last coordinates for each entry

        for key, waypoints in waypoints_by_tid.items():
            if waypoints:
                first_coordinate = waypoints[0]
                last_coordinate = waypoints[-1]
                first_last_coordinates[key] = {
                    'first_coordinate': first_coordinate,
                    'last_coordinate': last_coordinate
                }
        coordinate_lists = []

        for key, coordinates in first_last_coordinates.items():
            first_coord = coordinates['first_coordinate']
            last_coord = coordinates['last_coordinate']

            first_lat = first_coord['lat']
            first_lon = first_coord['lon']

            last_lat = last_coord['lat']
            last_lon = last_coord['lon']

            coordinate_lists.append([first_lon, first_lat])
            coordinate_lists.append([last_lon, last_lat])

        return render_template("map.html",
                               user=current_user,
                               driver_list=driver_list,
                               vehicle_list=vehicle_list,
                               first_last_coordinates=coordinate_lists,
                               waypoints_by_tid_for_mapbox=waypoints_by_tid_for_mapbox)

    return render_template("map.html",
                           user=current_user,
                           driver_list=driver_list,
                           vehicle_list=vehicle_list,
                           first_last_coordinates=[],
                           waypoints_by_tid_for_mapbox=[]
                           )


def serialize_waypoint(waypoint):
    return {
        "ptid": waypoint.ptid,
        "lat": waypoint.lat,
        "lon": waypoint.lon,
        "ele": waypoint.ele,
        "dt": waypoint.dt.strftime("%Y-%m-%d %H:%M:%S"),  # Beispiel: Datum in ein Textformat umwandeln
        "tid": waypoint.tid
    }
