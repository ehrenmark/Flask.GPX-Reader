from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Vehicle
from models import db



upload_vehicle = Blueprint('upload_vehicle', __name__)


@upload_vehicle.route('/upload_vehicle', methods=['GET', 'POST'])
@login_required
def upload_vehicle_in_db():



    if request.method == 'POST':
        polkz = request.form.get('license_plate')
        vin = request.form.get('vin')

        if polkz and vin:
            new_vehicle = Vehicle(polkz=polkz, vin=vin)
            db.session.add(new_vehicle)
            db.session.commit()

            flash('Fahrzeug wurde erfolgreich hinzugefügt.', 'success')
            return redirect(url_for('upload_vehicle.upload_vehicle_in_db'))

        else:
            flash('Bitte füllen Sie alle erforderlichen Felder aus.', 'danger')
    return render_template("upload_vehicle.html", user=current_user)