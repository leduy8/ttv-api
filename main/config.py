import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    LOGGING_LEVEL = logging.INFO
    SECRET_KEY = os.getenv("SECRET_KEY") or "ttv-clone1234"
    BASE_ITEM_PER_PAGE = 10
    STREAMS_PER_PAGE = BASE_ITEM_PER_PAGE

    # ? For sqlite
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '{db_name}.db')
    # ? For MySQL
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/{db_name}"
    # ? For PostgreSQL
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql+psycopg2://postgres:123456@localhost/ttv_dev"
    )
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
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql+psycopg2://postgres:123456@localhost/ttv_test"
    )
