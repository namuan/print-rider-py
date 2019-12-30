import base64
from datetime import datetime

from bleach import clean

from printrider.bleach_ext import *


def log(msg):
    t = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] {msg}")


def error(msg):
    t = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] ERROR: {msg}")


def sanitise_html(encoded_html):
    return clean(
        b64_decode(encoded_html),
        tags=EXTENDED_ALLOWED_TAGS,
        attributes=EXTENDED_ALLOWED_ATTRS
    )


def b64_encode(raw_str: str) -> str:
    return base64.standard_b64encode(bytes(raw_str, encoding='utf-8')).decode()


def b64_decode(encoded_str: str) -> str:
    return base64.standard_b64decode(encoded_str).decode()
