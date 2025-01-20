from os import path, environ


class Config:
    BASE_DIRECTORY = path.abspath(path.dirname(__file__))
    SECRET_KEY = "abhdlhrjekls75akkjlllakqawash"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(BASE_DIRECTORY, "database.db")
    UPLOAD_PATH = path.join(BASE_DIRECTORY, "static", "images")

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = environ.get("MAIL_USER")
    MAIL_PASSWORD = environ.get("MAIL_PASS")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False