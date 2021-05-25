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
    __tablename__ = 'role'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(80), unique=True)
    description = login_database.Column(login_database.String(255))


class Dataset(login_database.Model):
    __tablename__ = 'dataset'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200), unique=True)
    size = login_database.Column(login_database.Integer)
    category = login_database.Column(login_database.String(200))
    description = login_database.Column(login_database.String(200))


class User(login_database.Model, UserMixin): ## Usermixin required for flask_login functions
    __tablename__ = 'user'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    email = login_database.Column(login_database.String(255), unique=True)
    password = login_database.Column(login_database.String(255))
    username = login_database.Column(login_database.String(255))
    token_id = login_database.Column(login_database.Integer) ## unique?
    active = login_database.Column(login_database.Boolean())
    confirmed_at = login_database.Column(login_database.DateTime())
    ratings = login_database.Column(login_database.String(1024))
    roles = login_database.relationship('Role', secondary=roles_users,
                                        backref=login_database.backref('users', lazy='dynamic'))


class Rating(login_database.Model):
    __tablename__ = 'rating'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    rating = login_database.Column(login_database.String(512))
    dataset_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('dataset.id'))
    item_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('item.id'))
    user_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('user.id'))



class Item(login_database.Model):
    __tablename__ = 'item'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200))
    imdb_id= login_database.Column(login_database.String(32), unique=True) ## cant be integer as imdb id must be 7 digit and contains leading zero.
    dataset_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('dataset.id'))
    poster_url = login_database.Column(login_database.String(1024))


class Study(login_database.Model):
    __tablename__ = 'study'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200))
    description = login_database.Column(login_database.String(1024))
    dataset_id = login_database.Column(login_database.Integer, login_database.ForeignKey('dataset.id'))


# Setup Flask-Security

user_datastore = SQLAlchemyUserDatastore(login_database, User, Role)

