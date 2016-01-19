# Import Flask and Flask Restful
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Url for moodle
MOODLE_URL = 'https://ucilnica.fri.uni-lj.si'

# Define the uWSGI application object
app = Flask(__name__)
ma = Marshmallow(app)

# Define main entry point for the application
api = Api(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import resources
from module_auth.user import User
from module_auth.user import Users

from module_lpp.stations import Stations



