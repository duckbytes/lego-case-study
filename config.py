import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI") or "postgresql://localhost/lego"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
