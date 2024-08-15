from flask import Flask

from src.config import Config
from src.extensions import db, migrate
from src.views import main_blueprint



BLUEPRINTS = [
    main_blueprint,
]


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)

    return app



def register_extensions(app):

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)



def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)