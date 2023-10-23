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

        for tid in tid_list:
            waypoints = db.session.query(Waypoint).filter(Waypoint.tid == tid).all()

            # Filtere die Waypoints, um nur jeden zweiten Waypoint aufzunehmen

            # Erstelle waypoints_serialized mit den gefilterten Waypoints
            waypoints_serialized = {tid: [serialize_waypoint(waypoint) for waypoint in waypoints]}

            waypoints_by_tid.update(waypoints_serialized)  # Update the dictionary with the serialized waypoints

        # waypoints_by_tid now contains waypoints serialized by tid

        waypoints_for_geojson = []

        for waypoint in waypoints:


            feature_point = {
                                "type": "Feature",
                                "geometry":
                                    {
                                        "type": "Point",
                                        "coordinates": [waypoint.lon, waypoint.lat]
                                    },
                                "properties":
                                        {
                                            "datetime": waypoint.dt.isoformat(),
                                            "elevation": waypoint.ele,
                                            "name": f"Waypoint {waypoint.ptid}",
                                            "description": f"Description for Waypoint {waypoint.ptid}"
                                        }
                                    }

            waypoints_for_geojson.append(feature_point)

        filtered_waypoints = {}

        for tid, waypoints in waypoints_by_tid.items():
            if waypoints:
                # Sort waypoints by 'dt' (date and time)
                sorted_waypoints = sorted(waypoints,
                                          key=lambda waypoint: datetime.strptime(waypoint['dt'], '%Y-%m-%d %H:%M:%S'))

                # Extract the first and last waypoint
                first_waypoint = sorted_waypoints[0]
                last_waypoint = sorted_waypoints[-1]

                # Initialize a list to store the filtered waypoints
                filtered = [first_waypoint, last_waypoint]

                # Iterate through the sorted waypoints to find waypoints one hour apart
                for i in range(1, len(sorted_waypoints)):
                    current_time = datetime.strptime(sorted_waypoints[i]['dt'], '%Y-%m-%d %H:%M:%S')
                    prev_time = datetime.strptime(sorted_waypoints[i - 1]['dt'], '%Y-%m-%d %H:%M:%S')

                    # Check if the waypoints are one hour apart
                    if (current_time - prev_time) >= timedelta(hours=1):
                        filtered.append(sorted_waypoints[i])

                filtered_waypoints[tid] = filtered

        feature_collection = {
            "type": "FeatureCollection",
            "features": waypoints_for_geojson
        }
        with open("waypoints.geojson", "w") as geojson_file:
            json.dump(feature_collection, geojson_file, indent=2)

        new_list = [[item['lon'], item['lat']] for item in waypoints]

        return render_template("map.html",
                               user=current_user,
                               driver_list=driver_list,
                               vehicle_list=vehicle_list,
                               waypoints_by_tid=filtered_waypoints,
                               new_list = new_list)

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
