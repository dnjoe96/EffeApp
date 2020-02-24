import os

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER ='app/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# creating a configuration class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///vehicle.sqlite3"
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = UPLOAD_FOLDER