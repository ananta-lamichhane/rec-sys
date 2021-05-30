from flask import render_template, Blueprint, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_user import roles_required
from werkzeug.utils import redirect
from flask_security.utils import hash_password, verify_password
from sqlalchemy import desc, func, asc

import json
import pandas as pd
import os


from utils.select_survey_items import select_movies_for_survey
from utils.serve_posters import generate_poster_url_dict, load_next_movie

main_bp = Blueprint('main', __name__)  # needs to be here

from database.user_model import User,  Study, Rating, Item, Crossvalidation, Item_Genres, Study_Algorithms, Algorithm, Dataset, user_datastore
from application import login_database


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    login_database.session.query(Rating).filter(Rating.user_id == current_user.id).delete()
    login_database.session.commit()
    return render_template("home.html")


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    #TODO: implement login system using token and username as in the database model
    if request.method == 'POST':
        print("submitted login form")
        #take data from form

        token_nr = request.form.get('token_number')
        user_username = request.form.get('username')
        user_password = request.form.get('password')

        u = User.query.filter_by(token_id=token_nr).first()
        ## check if user u already exists
        if u and u.password == user_password:
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
    no_of_questions=10 ## number of survey questionnaires, we can query it from database later.
    if request.method == "POST":
        if request.form.get('formtype') == "2" and int(request.form.get('next_item')) < no_of_questions:  ## form is submitting movie ratings.
            imdb_id = request.form.get('imdb_id')
            next_item = request.form.get('next_item')
            print("next item "+ str(next_item))
           # print("imdb id :  " + imdb_id)
            rating = request.form.get('rating')
            itemid = login_database.session.query(Item).filter_by(imdb_id=imdb_id).first().id
            if login_database.session.query(Rating).filter_by(item_id=itemid).first():
                login_database.session.query(Rating).filter_by(item_id=itemid).first().rating=rating
                login_database.session.commit()  ## commit to db
            else:
                login_database.session.add(Rating(rating=rating, dataset_id=1, item_id=itemid, user_id=current_user.id))
                login_database.session.commit()  ## commit to db
            # we can query currently saved rating to current user from database.
            current_ratings = login_database.session.query(Rating).filter_by(user_id=current_user.id)
            for r in current_ratings:
                print("rating: " + str(r.rating) + " movieId: " + str(r.item_id))



            currnt_movieId = login_database.session.query(Item).filter_by(imdb_id=imdb_id).first().id
            next_movieId  = login_database.session.query(Item).order_by(Item.id.asc()).filter(Item.id > currnt_movieId).first().id

            print("current movie id : " + str(currnt_movieId) + "next imdb id : " + str(next_movieId))
            next_imdbId = login_database.session.query(Item).filter_by(id=next_movieId).first().imdb_id
            poster_url = generate_poster_url_dict(next_imdbId)

            print("current imdbid : " + imdb_id + "next imdb id : " + next_imdbId)
            return poster_url # return the json data as it is so ajax can handle it instead


        if request.form.get('formtype') == "1":  ## TODO: handle what to do when done button is clicked
            redirect('/recommendations', code=302)
        if request.form.get('formtype') == "3":  ## debugging database addition errors.
            #login_database.session.query(Rating.) # TODO: implement delete ratings when clear my ratings button pressed
            current_ratings = json.loads(current_user.ratings) ## load the dict with rating entries for current user.
            current_ratings[imdb_id] = rating ## add to the dict
            current_user.ratings = json.dumps(current_ratings)  ## make json string of the dict
            login_database.session.commit() ## commit to db
            print("current rating str: " + str(current_user.ratings))
        if request.form.get('formtype') == "1": ## TODO: handle what to do when done button is clicked
            print(current_user.email)
            print(current_user.ratings)
        if request.form.get('formtype') == "3": ## debugging database addition errors.
            print("add online users")
        if request.form.get('formtype') == "1": ## TODO: handle what to do when done button is clicked
            redirect('/recommendations', code=302)
        if request.form.get('formtype') == "3": ## debugging database addition errors.
            current_user.ratings = '{}' ## reset the dict
            login_database.session.commit()
            print(current_user.ratings)

    # test_ids = select_movies_for_survey()
    ##TODO: make sure the list of movies in the database, handle error otherwise
    test_id = 'tt0103859'
    poster_url = generate_poster_url_dict(test_id)
    #next_movie = movieId+1
    #next_data =
    return render_template("survey.html", poster_url=poster_url)


@main_bp.route('/bye')
#@login_required
def bye():
    logout_user()
    return render_template("bye.html")


@main_bp.route('/about')
def about():
    return render_template("about.html")


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # if request.form.validate_on_submit():
        user_email = request.form.get('email')
        user_name = request.form["name"]
        user_password = hash_password(request.form.get('password'))  ## password is hashed and salted

        print(user_password)

        ## new model says account instead of email
        u = User.query.filter_by(account=user_email).first()
        # check if user u already exists
        if u:
            flash("A user with this email already exists. please log in.")
            return redirect('login')
        else:
            login_database.session.add(User(account=user_email, name=user_name, password=user_password))
            login_database.session.commit()

    return render_template("register.html")


@main_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    admin_tokenid= login_database.session.query(User).filter_by(name='admin').first().token_id
    if current_user.token_id == admin_tokenid:
        if request.method == 'POST':
            if request.form.get('db-action') == "Add Users":
                last_token_id = login_database.session.query(func.max(User.token_id))
                print("add users")
                for u in range(2, 52):
                    user_datastore.create_user(token_id=u, name='user' + str(u), password='password', online_user=True)
                    login_database.session.commit()
            if request.form.get('db-action') == "Populate Database":
                ##open the files
                ratings_file = os.path.realpath('./database/datasets/movielens_small/ratings.csv')
                movies_file = os.path.realpath('./database/datasets/movielens_small/movies.csv')
                links_file = os.path.realpath('./database/datasets/movielens_small/links.csv')
                ##load as dataframes
                movies_df = pd.read_csv(movies_file, dtype='str')
                links_df = pd.read_csv(links_file, dtype='str')
                ratings_df = pd.read_csv(ratings_file, dtype='str')
                ##user names are numbers going up from 1 to max of the column add them to db

                for u in range(ratings_df['userId'].astype('int').max() + 1):
                    print("user no" + str(u))
                    ## add users to database
                    user_datastore.create_user(online_user=False, dataset_id=1)
                for row in movies_df.itertuples():  ## add all movies to db
                    imdb_id = 'tt' + links_df.loc[links_df['movieId'] == row.movieId]['imdbId'].to_string(index=False)
                    login_database.session.add(
                        Item(id=row.movieId, name=row.title, imdb_id=imdb_id, dataset_id=1, poster_url="empty"))
                    login_database.session.commit()
                print(ratings_df.head())
                for row in ratings_df.itertuples():  ## add all the ratings to the db
                    login_database.session.add(
                        Rating(rating=row.rating, dataset_id=5, item_id=row.movieId, user_id=row.userId))
                    login_database.session.commit()
                # survey_name = request.form.get('studies')
                survey_name = request.form.get('survey-name')
                login_database.session.add(Study(description="", name=survey_name, dataset_id=1))
                login_database.session.commit()
        return render_template("admin.html")
    return render_template('forbidden.html')




@main_bp.route('/recommendations', methods=['GET', 'POST'])
@login_required
def recommend():
    ## recommendations = highest rated movies by the user most similar to the current user, e.g. user no 483
    recoms = Rating.query.filter_by(user_id=483).order_by(desc(Rating.rating))
    movie_list = []
    for i in range(5):
        imdb_no = Item.query.filter_by(id=recoms[i].item_id).first().imdb_id
        movie_list.append(imdb_no)
        print(str(recoms[i].rating) + "  " + str(imdb_no))

    movie_data = generate_poster_url_dict(movie_list)
    return render_template('recommendations.html', poster_urls=movie_data)
