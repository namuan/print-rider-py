import uuid
from typing import Dict

import time

from printrider.utils import log, sanitise_html


def ts():
    return int(time.time() * 1000)


def validate_document_json(doc_json: Dict):
    if not doc_json:
        raise ValueError("Invalid document: {}".format(doc_json))

    html_code = doc_json.get('document')
    if not html_code:
        raise ValueError("Invalid document: {}".format(doc_json))

    return html_code


def save_document(dt, doc_json):
    html_code = validate_document_json(doc_json)
    sanitised_html = sanitise_html(html_code)
    timestamp = ts()
    item = {
        'id': str(uuid.uuid4()),
        'documentCode': sanitised_html,
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    dt.save(item)
    log("Saved document with {}".format(item['id']))
    return item['id']


def find_document(dt, print_id):
    log("Looking up document with Id {}".format(print_id))
    result = dt.load(print_id)
    print_document = result.get('Item', None)
    if not print_document:
        raise ValueError("Unable to find document with id {}".format(print_id))
    return print_document.get('documentCode')
