from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import requests
from models import User, db
from config import FlaskConfig
from views import views
from auth import auth
from upload_vehicle import upload_vehicle
from upload_driver import upload_driver

app = Flask(__name__)


app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(upload_vehicle, url_prefix="/")
app.register_blueprint(upload_driver, url_prefix="/")




app.config.from_object(FlaskConfig)
with app.app_context():
    db.init_app(app)
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)




@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
