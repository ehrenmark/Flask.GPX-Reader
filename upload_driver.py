from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Driver
from models import db



upload_driver = Blueprint('upload_driver', __name__)

@upload_driver.route('/upload_driver', methods=['GET', 'POST'])
@login_required
def upload_driver_in_db():
    if request.method == 'POST':
        surname = request.form.get('surname')
        first_name = request.form.get('firstname')
        email_address = request.form.get('email')
        nickname = request.form.get('nickname')

        if surname and first_name and email_address and nickname:
            new_driver = Driver(nick=nickname, surname=surname, forename=first_name, email=email_address)
            db.session.add(new_driver)
            db.session.commit()

            flash('Fahrer wurde erfolgreich hinzugefügt.', 'success')
            return redirect(url_for('upload_driver.upload_driver_in_db'))

        else:
            flash('Bitte füllen Sie alle erforderlichen Felder aus.', 'danger')

    return render_template("upload_driver.html", user=current_user)