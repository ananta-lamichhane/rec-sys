from flask import Flask, render_template
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import email_validator




load_dotenv('.ENV')
login_database = SQLAlchemy() ## initialize a new database
login_manager = LoginManager()



def create_app(): #config_file='flask_config.py'):
    app = Flask(__name__)
    app.config.from_object('flask_config.Configurations')
    login_database.init_app(app)

    from views import main_bp

    app.register_blueprint(main_bp)

    from database.user_model import User, Role, user_datastore
    security = Security(app, user_datastore)
    with app.app_context(): ### need application context to initialize database.
        login_database.create_all()
        login_database.session.commit()
        login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.unauthorized_handler ## serves forbidden.html in case user no logged in.
    def unauth_handler():
        return render_template('forbidden.html')

    return app
