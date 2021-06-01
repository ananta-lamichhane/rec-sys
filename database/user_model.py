import sys

from flask_security import SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin

sys.path.append("..")  ### fix problem with not being able to import from higher level packages
from application import login_database, login_manager


# TODO:check unique constrants and if they make sense
## relational table to assign roles (admin, customer, etc.)

# class Role(login_database.Model, RoleMixin):
##   __tablename__ = 'role'
#  id = login_database.Column(login_database.Integer(), primary_key=True)
# name = login_database.Column(login_database.String(80), unique=True)
# description = login_database.Column(login_database.String(255))

# UserMixin and RoleMixin allow for flask_login functioons such as login_user, is_authenticated, etc.
# For that we'll need User and Role class and user_datastore

roles_users = login_database.Table('roles_users',
                                   login_database.Column('user_id', login_database.Integer(),
                                                         login_database.ForeignKey('user.id')),
                                   login_database.Column('role_id', login_database.Integer(),
                                                         login_database.ForeignKey('role.id')))

class Dataset(login_database.Model):
    __tablename__ = 'dataset'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200), unique=True)
    size = login_database.Column(login_database.Integer())
    category = login_database.Column(login_database.String(200))
    description = login_database.Column(login_database.String(200))

class Role(login_database.Model, RoleMixin):
    __tablename__ = 'role'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(80), unique=True)
    description = login_database.Column(login_database.String(255))


class User(login_database.Model, UserMixin):
    __tablename__ = 'user'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    #user_id = login_database.Column(login_database.Integer(), unique=True)
    #account = login_database.Column(login_database.String(255), unique=True)
    name = login_database.Column(login_database.String(200))
    password = login_database.Column(login_database.String(1024))
    token_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('token.id'))
    online_user = login_database.Column(login_database.Boolean())
    dataset_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('dataset.id'))
    active = login_database.Column(login_database.Boolean())
    roles = login_database.relationship('Role', secondary=roles_users,
                                        backref=login_database.backref('users', lazy='dynamic'))
    # username = login_database.Column(login_database.String(255))  ## Why ?
    # is_active = login_database.Column(login_database.Boolean())  ## Why ?


# confirmed_at = login_database.Column(login_database.DateTime())  ## Why ?
# email = login_database.Column(login_database.String(255), unique=True)
# ratings = login_database.Column(login_database.String(1024))  ## Why ?


class Rating(login_database.Model):
    __tablename__ = 'rating'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    rating = login_database.Column(login_database.Float())
    item_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('item.id')) ## can't be unique one item has many ratings (by many users)
    user_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('user.id')) ## can'be unique one user can leave many ratings (for many items)
    dataset_id = login_database.Column(login_database.Integer, login_database.ForeignKey('dataset.id'))


class Item(login_database.Model):
    __tablename__ = 'item'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200))
    imdb_id = login_database.Column(login_database.Integer(), unique=True)
    dataset_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('dataset.id'))
    poster_url = login_database.Column(login_database.String(1024))


class ReclistItem(login_database.Model):
    __tablename__ = 'reclistitem'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    number = login_database.Column(login_database.Integer)
    item_id = login_database.Column(login_database.Integer, login_database.ForeignKey('item.id'))
    reclist_id = login_database.Column(login_database.Integer, login_database.ForeignKey('reclist.id'))
    prediction = login_database.Column(login_database.Float())


class Reclist(login_database.Model):
    __tablename__ = 'reclist'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    length = login_database.Column(login_database.Integer(), unique=True)
    algorithm_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('algorithm.id'))#,unique=True)
    user_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('user.id'))#, unique=True)


class Study_Algorithms(login_database.Model):
    __tablename__ = 'study_algorithms'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    algorithm_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('algorithm.id'),
                                         unique=True)
    study_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('study.id'), unique=True)


class Evaluation(login_database.Model):
    __tablename__ = 'evaluation'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    reclist_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('reclist.id'))
    user_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('user.id'), unique=True)
    study_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('study.id'), unique=True)
    utility = login_database.Column(login_database.Float())
    serendipity = login_database.Column(login_database.Float())
    novelty = login_database.Column(login_database.Float())
    diversity = login_database.Column(login_database.Float())
    unexpectedness = login_database.Column(login_database.Float())
    accuracy_mae = login_database.Column(login_database.Float())
    accuracy_mse = login_database.Column(login_database.Float())
    accuracy_rmse = login_database.Column(login_database.Float())
    non_rating_rate = login_database.Column(login_database.Float())


class Study(login_database.Model):
    __tablename__ = 'study'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200), unique=True)
    description = login_database.Column(login_database.String(1024))
    active = login_database.Column(login_database.Integer())
    dataset_id = login_database.Column(login_database.Integer())
    reclist_length = login_database.Column(login_database.Integer())


class Algorithm(login_database.Model):
    __tablename__ = 'algorithm'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(100), unique=True)
    description = login_database.Column(login_database.String(1024))


class Item_Genres(login_database.Model):
    __tablename__ = 'intemgenres'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    item_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('item.id'), unique=True)
    moviegenre_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('moviegenre.id'),
                                          unique=True)


class Token(login_database.Model):
    __tablename__ = 'token'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(40), unique=True)
    valid = login_database.Column(login_database.Boolean())


class Moviegenre(login_database.Model):
    __tablename__ = 'moviegenre'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    title = login_database.Column(login_database.String(1024))


class Crossvalidation(login_database.Model):
    __tablename__ = 'crossvalidation'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    algorithm_id = login_database.Column(login_database.Integer, login_database.ForeignKey('algorithm.id'), unique=True)
    dataset_id = login_database.Column(login_database.Integer(), login_database.ForeignKey('dataset.id'))
    rmse = login_database.Column(login_database.Float())
    mae = login_database.Column(login_database.Float())
    fit_time = login_database.Column(login_database.Float())
    test_time = login_database.Column(login_database.Float())


# Setup Flask-Security
## datastore is required by flask security


user_datastore = SQLAlchemyUserDatastore(login_database, User, Role)
