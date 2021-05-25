from flask import render_template, Blueprint, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import redirect
from flask_security.utils import hash_password, verify_password
from sqlalchemy import desc

import json
import pandas as pd
import os

from utils.select_survey_items import select_movies_for_survey
from utils.serve_posters import generate_poster_url_dict

main_bp = Blueprint('main', __name__) # needs to be here

from database.user_model import User, user_datastore, Study, Rating, Item
from application import login_database


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    print(select_movies_for_survey())
    return render_template("home.html")


@main_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        print("submitted login form")
        ##take data from form

        user_email = request.form.get('email')
        user_username = request.form.get('username')
        user_password = request.form.get('password')

        u = User.query.filter_by(email=user_email).first()
        ## check if user u already exists
        # TODO: implemet hash and salt on passwords
        if u and verify_password(user_password, password_hash=u.password):
            login_user(u)
            flash('Successfully logged in!')
            return redirect(url_for('main.survey'))
        else:
            flash('User does not exist. Please register first.')
            return "user does not exist"
    return render_template("login.html")


@main_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    if request.method == "POST":
        print("form type: " + str(request.form.get('formtype')))
        if request.form.get('formtype') == "2": ## formtype helps to distinguish between different post requests.
            imdb_id = request.form.get('imdb_id')
            rating = request.form.get('rating')
            current_ratings = json.loads(current_user.ratings) ## load the dict with rating entries for current user.
            current_ratings[imdb_id] = rating ## add to the dict
            current_user.ratings = json.dumps(current_ratings)  ## make json string of the dict
            login_database.session.add(Rating(rating=rating, dataset_id=23, item_id=45678, user_id=current_user.id))
            login_database.session.commit() ## commit to db
            print("current rating str: " + str(current_user.ratings))
        if request.form.get('formtype') == "1": ## TODO: handle what to do when done button is clicked
            redirect('/recommendations', code=302)
        if request.form.get('formtype') == "3": ## debugging database addition errors.
            current_user.ratings = '{}' ## reset the dict
            login_database.session.commit()
            print(current_user.ratings)

    #test_ids = select_movies_for_survey()
    test_ids = ['tt0103859', 'tt0110443', 'tt0089489', 'tt0047677', 'tt0340163', 'tt0112573', 'tt0130445', 'tt0089459', 'tt0047577', 'tt0340273']
    poster_urls = generate_poster_url_dict(test_ids)
    return render_template("survey.html", poster_urls=poster_urls)


@main_bp.route('/bye')
@login_required
def bye():
    logout_user()
    return render_template("bye.html")


@main_bp.route('/about')
def about():
    return render_template("about.html")


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #if request.form.validate_on_submit():
            user_email = request.form.get('email')
            user_name = request.form["name"]
            user_password = hash_password(request.form.get('password')) ## password is hashed and salted

            print(user_password)

            u = User.query.filter_by(email=user_email).first()
            ## check if user u already exists
            if u:
                flash("A user with this email already exists. please log in.")
                return redirect('login')
            else:
                user_datastore.create_user(email=user_email, username=user_name, password=user_password, ratings='{}')
                login_database.session.commit()

    return render_template("register.html")






@main_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    users = User.query.all()
    studies = Study.query.all()
    ratings = login_database.session.query(Rating).all()
    for study in studies:
        print(study.name)
    if request.method == 'POST':
        if request.form.get('db-action') == "Clear Database":
            login_database.session.query(Item).delete()
            login_database.session.query(Rating).delete()
            login_database.session.commit()
        if request.form.get('db-action') == "Populate Database":
            ratings_file = os.path.realpath('./database/datasets/movielens_small/ratings.csv')
            movies_file =  os.path.realpath('./database/datasets/movielens_small/movies.csv')
            links_file = os.path.realpath('./database/datasets/movielens_small/links.csv')
            movies_df = pd.read_csv(movies_file, dtype='str')
            links_df = pd.read_csv(links_file, dtype='str')
            for row in movies_df.itertuples():
                imdb_id = 'tt' + links_df.loc[links_df['movieId'] == row.movieId]['imdbId'].astype('str')
                print(imdb_id)
                login_database.session.add(Item(id=row.movieId, name=row.title, imdb_id=imdb_id, dataset_id=1, poster_url="empty"))
                login_database.session.commit()

            ratings_df = pd.read_csv(ratings_file, dtype='str')
            print(ratings_df.head())
            for row in ratings_df.itertuples(): ## populate the ratings table
                login_database.session.add(Rating(rating = row.rating, dataset_id=5, item_id=row.movieId, user_id=row.userId))
                login_database.session.commit()
            survey_name = request.form.get('studies')
            survey_description = request.form.get('survey-desc')
            login_database.session.add(Study(description=survey_description, name=survey_name, dataset_id = 23))
            login_database.session.commit()

    return render_template("admin.html")

@main_bp.route('/recommendations', methods=['GET', 'POST'])
@login_required
def recommend():
    ## recommendations = highest rated movies by the user most similar to the current user, e.g. user no 483
    recoms = Rating.query.filter_by(user_id=483).order_by(desc(Rating.rating))
    movie_list=[]
    for i in range(10):
        imdb_no = Item.query.filter_by(id = recoms[i].item_id).first().imdb_id
        idstr = 'tt' + str(imdb_no)
        print(idstr)
        movie_list.append(idstr)
        print(recoms[i].rating + "  " + str(imdb_no))

    movie_data = generate_poster_url_dict(movie_list)
    return render_template('recommendations.html', poster_urls=movie_data)
