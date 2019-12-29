import os
from pathlib import Path

import boto3


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SENTRY_ENABLED = True
    SECRET_KEY = os.getenv('FLASK_SECRET')
    PRINT_DOCUMENTS_DB_TABLE = os.getenv('APP_PRINT_DOCUMENTS_DB_TABLE')
    DOMAIN_NAME = os.getenv("APP_DOMAIN_NAME")
    DYNAMO_URL = os.getenv("APP_DYNAMO")


class ProductionConfig(Config):
    DB_CLIENT = boto3.resource('dynamodb')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SENTRY_ENABLED = False
    PRINT_DOCUMENTS_DB_TABLE = "local-print-documents"
    DB_CLIENT = boto3.resource('dynamodb', endpoint_url=Config.DYNAMO_URL)
    DOMAIN_NAME = os.getenv("APP_DOMAIN_NAME")


def setup_config(is_offline):
    return DevelopmentConfig() if is_offline else ProductionConfig()

