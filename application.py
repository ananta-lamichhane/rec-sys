from flask import Flask, render_template
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import email_validator



load_dotenv('.ENV')
db = SQLAlchemy() ## initialize a new database
login_manager = LoginManager() ## login manager helps implement login_required, etc.



def create_app(): #config_file='flask_config.py'):
    app = Flask(__name__)
    app.config.from_object('flask_config.Configurations') ## load configs from the file
    db.init_app(app)

    from views import main_bp

    app.register_blueprint(main_bp) ## register blueprint

    from database.user_model import User
    from database.user_model import user_datastore
    security = Security(app, user_datastore)
    with app.app_context(): ### need application context to initialize database.
        db.create_all()
        db.session.commit()
        login_manager.init_app(app)
        if not db.session.query(User).filter_by(name='admin').first(): ## create admin during start
            user_datastore.create_user(id=999999,token_id=9999, name='admin', password='admin', online_user=True)
            db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).filter_by(id=user_id).first()

    @login_manager.unauthorized_handler ## serves forbidden.html in case user no logged in.
    def unauth_handler():
        return render_template('forbidden.html')

    return app
