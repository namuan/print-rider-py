import os

import boto3
from dotenv import load_dotenv

from printrider.utils import log

is_offline = os.environ.get("AWS_SAM_LOCAL", False)

if is_offline:
    log("Offline detected. Loading .env.local")
    load_dotenv(".env.local", verbose=True)
else:
    log("Running on AWS Lambda. Loading .env.prod")
    load_dotenv(".env.prod", verbose=True)


class Config(object):
    CSRF_ENABLED = True
    PRINT_DOCUMENTS_DB_TABLE = os.getenv('APP_PRINT_DOCUMENTS_DB_TABLE')
    HOST_NAME = os.getenv("APP_HOST_NAME")
    DYNAMO_URL = os.getenv("APP_DYNAMO")


class ProductionConfig(Config):
    DB_CLIENT = boto3.resource('dynamodb')


class DevelopmentConfig(Config):
    DB_CLIENT = boto3.resource('dynamodb', endpoint_url=Config.DYNAMO_URL)


def setup_config():
    return DevelopmentConfig() if is_offline else ProductionConfig()
