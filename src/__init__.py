from flask import Flask
from flask_admin.contrib.sqla import ModelView

from src.config import Config
from src.extensions import db, migrate, login_manager
from src.views import main_blueprint
from src.admin import admin
from src.admin.term import TermView, ConnectedTermView
from src.admin.user import UserView
from src.commands import init_db, populate_db
from src.models import User, Term, ConnectedTerm


COMMANDS = [
    init_db,
    populate_db
]

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    register_extensions(app)
    app.register_blueprint(main_blueprint)
    register_commands(app)

    return app



def register_extensions(app):

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # Login-Manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # Flask-Admin
    admin.init_app(app)
    admin.add_view(TermView(Term, db.session, endpoint="term_panel", name="Terms"))
    admin.add_view(ConnectedTermView(ConnectedTerm, db.session, endpoint="connected_term", name="Connected terms"))
    admin.add_view(UserView(User, db.session))




def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)


