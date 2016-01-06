# Statement for enabling the development environment
#DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'mFRI.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
