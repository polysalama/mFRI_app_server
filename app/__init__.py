# Import Flask and Flask Restful
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

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
from module_users.user import User
from module_users.user import Users



