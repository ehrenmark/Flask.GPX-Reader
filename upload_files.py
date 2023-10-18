from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Waypoint, Track, Vehicle, Driver
from models import db
import gpxpy
from gpxpy.gpx import GPXException

upload_files = Blueprint('upload_files', __name__)




@upload_files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_files_to_db():
    driver_list = get_drivers()
    vehicle_list = get_vehicles()

    if request.method == 'POST':
        file = request.files['file']
        driver_pid = request.form.get('driver')
        vehicle_fzid = request.form.get('vehicle')


        found_driver = db.session.query(Driver).filter_by(pid=driver_pid).first()
        found_vehicle = db.session.query(Vehicle).filter_by(fzid=vehicle_fzid).first()

        parts = file.filename.split('_')
        if len(parts) == 3:
            abkuerzung_fahrer = parts[0]
            kennzeichen = parts[1]
            nummer = parts[2]

        else:
            flash(f'Fehler beim Upload der Datei: {file.filename}: Ungültiges Dateinamenformat', 'error')
            return redirect(url_for('upload_files.upload_files_to_db'))

        if abkuerzung_fahrer == found_driver.nick and kennzeichen == found_vehicle.polkz:

            results = db.session.query(Track).filter(Track.filename == file.filename).all()
            if len(results) >= 1:
                flash('Datei befindet sich schon in der Datenbank!', 'error')
                return redirect(url_for('upload_files.upload_files_to_db'))

            try:

                if file and driver_pid and vehicle_fzid:


                    file_data = file.read()
                    gpx = gpxpy.parse(file_data)

                    for track in gpx.tracks:
                        start_time, end_time = extract_start_end_time(gpx)

                        new_track = Track(filename=file.filename, fzid=int(vehicle_fzid), pid=int(driver_pid), start_time=start_time, end_time=end_time)
                        db.session.add(new_track)
                        db.session.commit()

                        for segment in track.segments:
                            for point in segment.points:

                                new_track_segment_point = Waypoint(
                                    lat=point.latitude,
                                    lon=point.longitude,
                                    ele=point.elevation,
                                    dt=point.time,
                                    tid=new_track.tid
                                )
                                db.session.add(new_track_segment_point)
                                db.session.commit()



                    flash('Datei wurde erfolgreich hochgeladen.', 'success')
                    return redirect(url_for('upload_files.upload_files_to_db'))
            except GPXException as e:
                flash(f'Fehler beim Upload der Datei: {file.filename}: {e}', 'error')
                return redirect(url_for('upload_files.upload_files_to_db'))
        else:
            flash(f'Dateiname stimmt nicht mit dem Fahrer und/oder dem Fahrzeug überein!', 'error')
            return redirect(url_for('upload_files.upload_files_to_db'))

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


def extract_start_end_time(gpx):


    if gpx.tracks:
        # Nehmen wir an, wir betrachten den ersten Track.
        track = gpx.tracks[0]

        if track.segments:
            # Nehmen wir an, wir betrachten das erste Segment des Tracks.
            segment = track.segments[0]

            if segment.points:
                # Extrahieren der Anfangs- und Endzeit aus den Zeitstempeln der ersten und letzten Punkte im Segment.
                start_time = segment.points[0].time
                end_time = segment.points[-1].time

                return start_time, end_time

    return None, None