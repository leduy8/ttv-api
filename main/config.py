import logging
import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    LOGGING_LEVEL = logging.INFO
    SECRET_KEY = os.getenv("SECRET_KEY") or "ttv-clone1234"
    BASE_ITEM_PER_PAGE = os.getenv("BASE_ITEM_PER_PAGE")
    STREAMS_PER_PAGE = BASE_ITEM_PER_PAGE
    GOOGLE_ID = os.getenv("GOOGLE_ID")
    GOOGLE_SECRET = os.getenv("GOOGLE_SECRET")

    # ? For sqlite
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '{db_name}.db')
    # ? For MySQL
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/{db_name}"
    # ? For PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_DEV")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(DevelopmentConfig):
    TESTING = True

    # ? For sqlite
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '{db_name}_test.db')
    # ? For MySQL
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/{db_name}_test"
    # ? For PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_TEST")
