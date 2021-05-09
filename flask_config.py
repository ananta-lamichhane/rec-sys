import os


class Configurations:
    DEBUG=True
    CSRF_ENABLED=True
    FLASK_APP ='run.py'
    SECRET_KEY = 'supersecretkey123'
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLITE_URI') ## temporary, replace with pgsql db later
    SQLALCHEMY_TRACK_MODIFICATIONS = False  ##supresses track modification memory usage warning
