import boto3
import pytest

from printrider import create_app
from printrider.config import Config


class TestConfiguration(Config):
    DEVELOPMENT = True
    DEBUG = True
    DB_CLIENT = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    PRINT_DOCUMENTS_DB_TABLE = "local-print-documents"
    DOMAIN_NAME = "http://test"


@pytest.fixture(scope='module')
def test_client():
    test_config = TestConfiguration()
    test_app = create_app(test_config)
    client = test_app.test_client()
    test_context = test_app.app_context()
    test_context.push()

    yield client

    test_context.pop()
