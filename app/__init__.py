# Import Flask and Flask Restful
from flask import Flask
from flask_restful import Api

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the uWSGI application object
app = Flask(__name__)

# Define main entry point for the application
api = Api(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import resources
from module_users.user import User



