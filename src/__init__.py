from flask import Flask

from src.config import Config
from src.extensions import db, migrate, login_manager
from src.views import main_blueprint
from src.commands import init_db, populate_db
from src.models import User


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



def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)


