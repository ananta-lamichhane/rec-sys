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
<<<<<<< HEAD
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200), unique=True)
    size = login_database.Column(login_database.Integer)
=======
    id = login_database.Column(login_database.Integer(11), primary_key=True)
    name = login_database.Column(login_database.String(200), unique=True)
    size = login_database.Column(login_database.Integer(11))
>>>>>>> 0edd2ec24e59cc1e475a18d2264926289737cbae
    category = login_database.Column(login_database.String(200))
    description = login_database.Column(login_database.String(200))


class User(login_database.Model, UserMixin):
    __tablename__ = 'user'
    id = login_database.Column(login_database.Integer(), primary_key=True)
<<<<<<< HEAD
    email = login_database.Column(login_database.String(255), unique=True)
    password = login_database.Column(login_database.String(255))
    username = login_database.Column(login_database.String(255))
    token_id = login_database.Column(login_database.Integer) ## unique?
    active = login_database.Column(login_database.Boolean())
    confirmed_at = login_database.Column(login_database.DateTime())
    ratings = login_database.Column(login_database.String(1024))
=======
    user_id = login_database.Column(login_database.Integer(11), unique=True)
    account = login_database.Column(login_database.String(255), unique=True)
    name = login_database.Column(login_database.String(200))
    token_id = login_database.Column(login_database.Integer(11),login_database.ForeignKey('token.id'), unique=True) ## unique?
    online_user = login_database.Column(login_database.Integer(1))
    dataset_id = login_database.Column(login_database.Integer(11),login_database.ForeignKey('dataset.id'), unique=True)
    
    username = login_database.Column(login_database.String(255)) ## Why ?
    active = login_database.Column(login_database.Boolean())## Why ?
    confirmed_at = login_database.Column(login_database.DateTime()) ## Why ?
    ratings = login_database.Column(login_database.String(1024))## Why ?
>>>>>>> 0edd2ec24e59cc1e475a18d2264926289737cbae
    roles = login_database.relationship('Role', secondary=roles_users,
                                        backref=login_database.backref('users', lazy='dynamic')) ## why ?


class Rating(login_database.Model):
    __tablename__ = 'rating'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    rating = login_database.Column(login_database.String(512))
    dataset_id = login_database.Column(login_database.Integer, login_database.ForeignKey('dataset.id'))


class Item(login_database.Model):
    __tablename__ = 'item'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200))
    imdb_id= login_database.Column(login_database.Integer(), unique=True)
    poster_url = login_database.Column(login_database.String(1024))
    
class ReclistItem(login_database.Model):
    __tablename__ = 'reclistitem'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    number = login_database.Column(login_database.Integer)
    item_id = login_database.Column(login_database.Integer, login_database.ForeignKey('item.id'))
    reclist_id = login_database.Column(login_database.Integer, login_database.ForeignKey('reclist.id'))
    prediction = login_database.Column(login_database.Integer(20,10))
    

class Reclist(login_database.Model):
    __tablename__ = 'reclist'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    length = login_database.Column(login_database.Integer, unique = True)
    algorithm_id = login_database.Column(login_database.Integer, login_database.ForeignKey('algorithm.id'), unique = True)
    user_id = login_database.Column(login_database.Integer, login_database.ForeignKey('user.id'), unique = True)
    
class Study_Algorithms(login_database.Model):
    __tablename__ = 'study_algorithms'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    algorithm_id = login_database.Column(login_database.Integer, login_database.ForeignKey('algorithm.id'), unique = True)
    study_id = login_database.Column(login_database.Integer, login_database.ForeignKey('study.id'), unique = True)
    
class Evaluation(login_database.Model):
    __tablename__ = 'evaluation'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    reclist_id = login_database.Column(login_database.Integer, login_database.ForeignKey('reclist.id')) 
    user_id = login_database.Column(login_database.Integer, login_database.ForeignKey('user.id'), unique = True)
    study_id = login_database.Column(login_database.Integer, login_database.ForeignKey('study.id'), unique = True)
    utility = login_database.Column(login_database.Integer(10,2))
    serendipity = login_database.Column(login_database.Integer(10,2))
    novelty = login_database.Column(login_database.Integer(10,2))
    diversity = login_database.Column(login_database.Integer(10,2))
    unexpectedness = login_database.Column(login_database.Integer(10,2))
    accuracy_mae = login_database.Column(login_database.Integer(10,2))
    accuracy_mse = login_database.Column(login_database.Integer(10,2))
    accuracy_rmse = login_database.Column(login_database.Integer(10,2))
    non_rating_rate = login_database.Column(login_database.Integer(10,2))

class Study(login_database.Model):
    __tablename__ = 'study'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200), unique=True)
    description = login_database.Column(login_database.String(200))
    active = login_database.Column(login_database.Integer(1))
    dataset_id = login_database.Column(login_database.Integer(11))
    reclist_length = login_database.Column(login_database.Integer(11))
    
class Algorithm(login_database.Model):
    __tablename__ = 'algorithm'
    id = login_database.Column(login_database.Integer(11), primary_key=True)
    name = login_database.Column(login_database.String(100), unique = True)
    description = login_database.Column(login_database.String(200))

class Item_Genres(login_database.Model):
    __tablename__ = 'intemgenres'
    id = login_database.Column(login_database.Integer(11), primary_key=True)
    item_id = login_database.Column(login_database.Integer(11), login_database.ForeignKey('item.id'), unique=True)
    moviegenre_id = login_database.Column(login_database.Integer(11), login_database.ForeignKey('moviegenre.id'), unique = True)   
    
class Token(login_database.Model):
    __tablename__ = 'token'
    id = login_database.Column(login_database.Integer(11), primary_key=True)
    name = login_database.Column(login_database.String(40), unique=True)
    valid = login_database.Column(login_database.Integer(1))
    
class Moviegenre(login_database.Model):
    __tablename__ = 'moviegenre'
    id = login_database.Column(login_database.Integer(11), primary_key=True)
    title = login_database.Column(login_database.String(100), unique=True)
    
class Crossvalidation(login_database.Model):
    __tablename__ = 'crossvalidation'
    id = login_database.Column(login_database.Integer(11), primary_key=True)
    algorithm_id = login_database.Column(login_database.Integer, login_database.ForeignKey('algorithm.id'), unique = True)
    dataset_id = login_database.Column(login_database.Integer(11), login_database.ForeignKey('dataset.id'))
    rmse = login_database.Column(login_database.Integer(12,10))
    mae = login_database.Column(login_database.Integer(12,10))
    fit_time = login_database.Column(login_database.Integer(20,4))
    test_time = login_database.Column(login_database.Integer(20,4))
    

    

class Rating(login_database.Model):
    __tablename__ = 'rating'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    rating = login_database.Column(login_database.String(512))
    dataset_id = login_database.Column(login_database.Integer, login_database.ForeignKey('dataset.id'))


class Item(login_database.Model):
    __tablename__ = 'item'
    id = login_database.Column(login_database.Integer(), primary_key=True)
    name = login_database.Column(login_database.String(200))
    imdb_id= login_database.Column(login_database.Integer(), unique=True)
    poster_url = login_database.Column(login_database.String(1024))


# Setup Flask-Security

user_datastore = SQLAlchemyUserDatastore(login_database, User, Role)



















