from flask import Flask

from src.config import Config
from src.extensions import db, migrate
from src.views import main_blueprint
from src.commands import init_db, populate_db


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



def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)


