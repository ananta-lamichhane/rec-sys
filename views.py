from flask import render_template, Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template("home.html")

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@main_bp.route('/survey')
def survey():
    return render_template("survey.html")


@main_bp.route('/bye')
def bye():
    return render_template("bye.html")


@main_bp.route('/about')
def about():
    return render_template("about.html")

@main_bp.route('/admin')
def admin():
    return render_template("admin.html")


