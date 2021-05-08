from flask import render_template, Blueprint, request, url_for
from flask_login import login_required, current_user, login_user, logout_user
from flask_security.utils import encrypt_password
from werkzeug.utils import redirect

main_bp = Blueprint('main', __name__)
from database.user_model import User, Role, user_datastore
from application import login_database

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("submitted login form")
        ##take data from form
        user_email = request.form.get('email')
        user_username = request.form.get('username')
        user_password = request.form.get('password')

        u = User.query.filter_by(email=user_username).first()
        ## check if user u already exists
        if u:
            login_user(u)
            return redirect(url_for('main.survey'))
        else:
            return "user does not exist"


    return render_template("home.html")

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        print("debug1")
        user_email = request.form.get('email')
        user_name = request.form["name"]
        user_password = request.form.get('password')

        ## create a new user with above information

        u = User(username= user_name, email=user_email, password=user_password)
        user_datastore.create_user(email=user_email, username=user_name, pasword=user_password)
        login_database.session.commit()

        print(user_name)
    return render_template("login.html")

@main_bp.route('/survey')
@login_required
def survey():
    return render_template("survey.html")


@main_bp.route('/bye')
def bye():
    u = current_user
    logout_user()
    return render_template("bye.html")


@main_bp.route('/about')
def about():
    return render_template("about.html")

@main_bp.route('/admin')
def admin():
    return render_template("admin.html")


