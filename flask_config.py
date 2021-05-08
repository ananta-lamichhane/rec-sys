import os


class Configurations:
    FLASK_APP ='run.py'
    SECRET_KEY = 'aklkadf8934rklls0f90a9f0' ## generate truly secure random string later.
    FLASK_ENV = 'Testing'
    SQLALCHEMY_DATABASE_URI = "sqlite://///tmp/test3.db" ## temporary, replace with pgsql db later
    SQLALCHEMY_TRACK_MODIFICATIONS = False  ##supresses track modification memory usage warning
