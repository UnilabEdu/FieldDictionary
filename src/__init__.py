from flask import Flask
from flask_admin.contrib.sqla import ModelView
from werkzeug import serving

from src.config import Config
from src.extensions import db, migrate, login_manager, ckeditor
from src.views import main_blueprint
from src.admin import admin
from src.admin.term import TermView, CategoryView
from src.admin.user import UserView
from src.commands import init_db, populate_db
from src.models import User, Term, Category

COMMANDS = [
    init_db,
    populate_db
]


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    app.config['CKEDITOR_PKG_TYPE'] = 'basic'

    register_extensions(app)
    app.register_blueprint(main_blueprint)
    register_commands(app)
    configure_logger()

    return app


def register_extensions(app):
    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # Login-Manager
    login_manager.init_app(app)

    # CKEditor
    ckeditor.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # Flask-Admin
    admin.init_app(app)
    admin.add_view(TermView(Term, db.session, endpoint="term_panel", name="ტერმინები"))
    admin.add_view(CategoryView(Category, db.session, endpoint="category", name="დარგები"))
    admin.add_view(UserView(User, db.session, name="მომხმარებელი"))


def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)


def configure_logger():
    default_logger = serving.WSGIRequestHandler.log_request

    def log_request(self, *args, **kwargs):
        if str(args[0]) == '304':
            return

        if 'static' in self.path:
            return

        default_logger(self, *args, **kwargs)

    serving.WSGIRequestHandler.log_request = log_request