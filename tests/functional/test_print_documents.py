from http import HTTPStatus
from urllib.parse import urlparse

from printrider.utils import b64_encode


def _create_print(test_client, document_code):
    print_doc = dict(
        document=document_code
    )
    return test_client.post('/prints', json=print_doc)


def _extract_path(url):
    result = urlparse(url)
    return result.path


def test_save_print_document(test_client):
    # When a new print is saved
    res = _create_print(test_client, 'c29tZXRoaW5n')

    # Then header should contain the location of the saved print
    assert res.status_code == HTTPStatus.CREATED
    assert res.headers["Location"].startswith("http://test")


def test_load_print_document(test_client):
    # Given a new print
    original_text = "Hello World"
    new_print_res = _create_print(test_client, b64_encode(original_text))
    new_print_location = new_print_res.headers['Location']
    print_path = _extract_path(new_print_location)

    # When the print is retrieved
    res = test_client.get(print_path)

    # Then the response should contain the original html text
    assert res.status_code == HTTPStatus.OK
    assert original_text in res.data.decode()


def test_error_if_unable_to_find_document(test_client):
    # When an invalid document is retrieved
    res = test_client.get("/prints/unknown-print-id")

    # Then
    assert res.status_code == HTTPStatus.OK
    assert "Unable to find document with id unknown-print-id" in res.data.decode()


def test_error_if_an_empty_json_is_saved(test_client):
    # When an empty json is saved
    res = test_client.post("/prints", json="")

    # Then
    assert res.status_code == HTTPStatus.OK
    assert "Invalid document:" in res.data.decode()


def test_error_if_an_empty_document_is_saved(test_client):
    # When an invalid document is saved
    res = _create_print(test_client, "")

    # Then
    assert res.status_code == HTTPStatus.OK
    assert "Invalid document:" in res.data.decode()

