from flask import render_template, Blueprint, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import redirect
from flask_security.utils import hash_password, verify_password
import random
import json

from utils.select_survey_items import select_movies_for_survey
from utils.serve_posters import generate_poster_url_dict

main_bp = Blueprint('main', __name__) # needs to be here

from database.user_model import User, user_datastore,Item,Rating
from application import login_database


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # print(select_movies_for_survey())
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
        print(request.form)
        print("form type: " + str(request.form.get('formtype')))
        if request.form.get('formtype') == "2": ## formtype helps to distinguish between different post requests.
            item_id = request.form.get('item_id')
            no_rating = request.form.get('no_rating')
            print(request.form.get('rating'))
            rating = request.form.get('rating') if not no_rating else None
            rating_obj = Rating.query.filter_by(item_id=item_id,user_id=current_user.id).first()
            if not rating_obj:
                rating_obj = Rating(item_id=item_id,user_id=current_user.id,rating=rating)
                login_database.session.add(rating_obj)
                login_database.session.commit()
                print(item_id,rating)
        if request.form.get('formtype') == "1": ## TODO: handle what to do when done button is clicked
            print(current_user.email)
            print(current_user.ratings)
        if request.form.get('formtype') == "3": ## debugging database addition errors.
            current_user.ratings = '{}'
            login_database.session.commit()
            print(current_user.ratings)

    imdb_ids = [i.item.imdb_id for i in Rating.query.filter_by(user_id=current_user.id)]
    imdb_ids = list(imdb_ids)
    poster_urls = Item.query.filter(Item.imdb_id.notin_(imdb_ids)).all()
    poster_urls = [random.choice(poster_urls)]
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
