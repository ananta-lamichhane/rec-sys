from flask import Flask
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import email_validator




login_database = SQLAlchemy() ## initialize a new database
login_manager = LoginManager()



def create_app(): #config_file='flask_config.py'):
    app = Flask(__name__)
    app.config.from_object('flask_config.Configurations')
    login_database.init_app(app)

    from database.user_model import User, Role, user_datastore
    security = Security(app, user_datastore)
    with app.app_context(): ### need application context to initialize database.
        login_database.create_all()
        login_database.session.commit()
        login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from views import main_bp

    app.register_blueprint(main_bp)

    return app
