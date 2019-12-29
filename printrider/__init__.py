from flask import Flask

from printrider.dynamo_db import DynamoDatabase

db_config = DynamoDatabase()


def create_app(config_object):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    init_db(config_object)
    register_blueprints(app)
    return app


def init_db(config_object):
    db_config.init_app(config_object.DB_CLIENT, config_object.PRINT_DOCUMENTS_DB_TABLE)


def register_blueprints(app: Flask):
    from printrider.prints import prints_blueprint
    app.register_blueprint(prints_blueprint)
