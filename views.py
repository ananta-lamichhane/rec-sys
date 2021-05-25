from flask import render_template, Blueprint, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import redirect
from flask_security.utils import hash_password, verify_password

import json

from utils.select_survey_items import select_movies_for_survey
from utils.serve_posters import generate_poster_url_dict

main_bp = Blueprint('main', __name__) # needs to be here

from database.user_model import User, user_datastore
from application import login_database


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    print(select_movies_for_survey)
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
            login_database.session.commit() ## commit to db
            print("current rating str: " + str(current_user.ratings))
        if request.form.get('formtype') == "1": ## TODO: handle what to do when done button is clicked
            print(current_user.email)
            print(current_user.ratings)
        if request.form.get('formtype') == "3": ## debugging database addition errors.
            current_user.ratings = '{}'
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
    print(current_user.ratings)
    return render_template("admin.html")
