import sys
sys.path.append("..") ### fix problem with not being able to import from higher level packages
from application import login_database


class User(login_database.Model): ## create database model for a user.
    id = login_database.Column(login_database.Integer, primary_key=True)
    username = login_database.Column(login_database.String(50), unique=True, nullable=False)
    email = login_database.Column(login_database.String(50), unique=True, nullable=False)

    def __repr__(self):
        return 'User %r' % self.username
