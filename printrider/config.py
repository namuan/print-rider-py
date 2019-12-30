import os

import boto3
from dotenv import load_dotenv

from printrider.utils import log

is_offline = os.environ.get("AWS_SAM_LOCAL", False)

if is_offline:
    log("Offline detected. Loading local.env")
    load_dotenv("local.env", verbose=True)
else:
    log("Running on AWS Lambda. Loading prod.env")
    load_dotenv("prod.env", verbose=True)


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


def setup_config():
    return DevelopmentConfig() if is_offline else ProductionConfig()
