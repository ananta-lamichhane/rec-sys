import sys

from flask_security import SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

sys.path.append("..")  ### fix problem with not being able to import from higher level packages
from application import login_database

## relational table to assign roles (admin, customer, etc.)
roles_users = login_database.Table('roles_users',
                                   login_database.Column('user_id', login_database.Integer(),
                                                         login_database.ForeignKey('user.id')),
                                   login_database.Column('role_id', login_database.Integer(),
                                                         login_database.ForeignKey('role.id')))


class Role(login_database.Model, RoleMixin):
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(80), unique=True)
    description = login_database.Column(login_database.String(255))


class User(login_database.Model, UserMixin):
    id = login_database.Column(login_database.Integer, primary_key=True)
    email = login_database.Column(login_database.String(255), unique=True)
    password = login_database.Column(login_database.String(255))
    username = login_database.Column(login_database.String(255))
    active = login_database.Column(login_database.Boolean())
    confirmed_at = login_database.Column(login_database.DateTime())
    roles = login_database.relationship('Role', secondary=roles_users,
                                        backref=login_database.backref('users', lazy='dynamic'))


# Setup Flask-Security

user_datastore = SQLAlchemyUserDatastore(login_database, User, Role)

