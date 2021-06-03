import sys

from flask_security import SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin

sys.path.append("..")  ### fix problem with not being able to import from higher level packages
from application import db, login_manager


# TODO:check unique constrants and if they make sense
## relational table to assign roles (admin, customer, etc.)

# class Role(login_database.Model, RoleMixin):
##   __tablename__ = 'role'
#  id = login_database.Column(login_database.Integer(), primary_key=True)
# name = login_database.Column(login_database.String(80), unique=True)
# description = login_database.Column(login_database.String(255))

# UserMixin and RoleMixin allow for flask_login functioons such as login_user, is_authenticated, etc.
# For that we'll need User and Role class and user_datastore

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))

class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), unique=True)
    size = db.Column(db.Integer())
    category = db.Column(db.String(200))
    description = db.Column(db.String(200))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    #user_id = login_database.Column(login_database.Integer(), unique=True)
    #account = login_database.Column(login_database.String(255), unique=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(1024))
    token_id = db.Column(db.Integer(), db.ForeignKey('token.id'))
    online_user = db.Column(db.Boolean())
    dataset_id = db.Column(db.Integer(), db.ForeignKey('dataset.id'))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    # username = login_database.Column(login_database.String(255))  ## Why ?
    # is_active = login_database.Column(login_database.Boolean())  ## Why ?


# confirmed_at = login_database.Column(login_database.DateTime())  ## Why ?
# email = login_database.Column(login_database.String(255), unique=True)
# ratings = login_database.Column(login_database.String(1024))  ## Why ?


class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer(), primary_key=True)
    rating = db.Column(db.Float())
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id')) ## can't be unique one item has many ratings (by many users)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id')) ## can'be unique one user can leave many ratings (for many items)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    imdb_id = db.Column(db.Integer(), unique=True)
    dataset_id = db.Column(db.Integer(), db.ForeignKey('dataset.id'))
    poster_url = db.Column(db.String(1024))


class ReclistItem(db.Model):
    __tablename__ = 'reclistitem'
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    reclist_id = db.Column(db.Integer, db.ForeignKey('reclist.id'))
    prediction = db.Column(db.Float())


class Reclist(db.Model):
    __tablename__ = 'reclist'
    id = db.Column(db.Integer(), primary_key=True)
    length = db.Column(db.Integer(), unique=True)
    algorithm_id = db.Column(db.Integer(), db.ForeignKey('algorithm.id'))#,unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))#, unique=True)


class Study_Algorithms(db.Model):
    __tablename__ = 'study_algorithms'
    id = db.Column(db.Integer(), primary_key=True)
    algorithm_id = db.Column(db.Integer(), db.ForeignKey('algorithm.id'),
                             unique=True)
    study_id = db.Column(db.Integer(), db.ForeignKey('study.id'), unique=True)


class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    id = db.Column(db.Integer(), primary_key=True)
    reclist_id = db.Column(db.Integer(), db.ForeignKey('reclist.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    study_id = db.Column(db.Integer(), db.ForeignKey('study.id'))
    utility = db.Column(db.Float())
    serendipity = db.Column(db.Float())
    novelty = db.Column(db.Float())
    diversity = db.Column(db.Float())
    unexpectedness = db.Column(db.Float())
    accuracy_mae = db.Column(db.Float())
    accuracy_mse = db.Column(db.Float())
    accuracy_rmse = db.Column(db.Float())
    non_rating_rate = db.Column(db.Float())


class Study(db.Model):
    __tablename__ = 'study'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.String(1024))
    active = db.Column(db.Integer())
    dataset_id = db.Column(db.Integer())
    reclist_length = db.Column(db.Integer())


class Algorithm(db.Model):
    __tablename__ = 'algorithm'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(1024))


class Item_Genres(db.Model):
    __tablename__ = 'intemgenres'
    id = db.Column(db.Integer(), primary_key=True)
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'), unique=True)
    moviegenre_id = db.Column(db.Integer(), db.ForeignKey('moviegenre.id'),
                              unique=True)


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40), unique=True)
    valid = db.Column(db.Boolean())


class Moviegenre(db.Model):
    __tablename__ = 'moviegenre'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(1024))


class Crossvalidation(db.Model):
    __tablename__ = 'crossvalidation'
    id = db.Column(db.Integer(), primary_key=True)
    algorithm_id = db.Column(db.Integer, db.ForeignKey('algorithm.id'), unique=True)
    dataset_id = db.Column(db.Integer(), db.ForeignKey('dataset.id'))
    rmse = db.Column(db.Float())
    mae = db.Column(db.Float())
    fit_time = db.Column(db.Float())
    test_time = db.Column(db.Float())


# Setup Flask-Security
## datastore is required by flask security


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
