from flask import Flask, render_template
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import email_validator
from utils.serve_posters import generate_poster_url_dict
import os


load_dotenv('.ENV')
login_database = SQLAlchemy() ## initialize a new database
login_manager = LoginManager()



def create_app(): #config_file='flask_config.py'):
    app = Flask(__name__)
    app.config.from_object('flask_config.Configurations')
    login_database.init_app(app)

    from views import main_bp

    app.register_blueprint(main_bp)

    from database.user_model import User, Role, user_datastore,Item
    security = Security(app, user_datastore)
    with app.app_context(): ### need application context to initialize database.
        login_database.create_all()
        login_database.session.commit()
        login_manager.init_app(app)

    # add or update imdb data
    #test_ids = select_movies_for_survey()
        test_ids = ['tt0103859', 'tt0110443', 'tt0089489', 'tt0047677', 'tt0340163', 'tt0112573', 'tt0130445', 'tt0089459', 'tt0047577', 'tt0340273']
        poster_urls = generate_poster_url_dict(test_ids)
        items = []
        for item in poster_urls:
            db_item = Item.query.filter_by(**item).first()
            if not db_item:
                items.append(Item(**item))
        if items:
            login_database.session.bulk_save_objects(items)
            login_database.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.unauthorized_handler ## serves forbidden.html in case user no logged in.
    def unauth_handler():
        return render_template('forbidden.html')

    return app