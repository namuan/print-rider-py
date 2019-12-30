from pathlib import Path

import pytest

from printrider.utils import sanitise_html, b64_encode

test_data = [
    ("Hello World", "Hello World"),
    ("<strong>Hello</strong>", "<strong>Hello</strong>"),
    ("<script>alert('hello')</script>", "&lt;script&gt;alert('hello')&lt;/script&gt;"),
    ("<h2>[Client -&gt; Gateway] Submit payment</h2>", "<h2>[Client -&gt; Gateway] Submit payment</h2>"),
    ("<h3>Request</h3>", "<h3>Request</h3>")
]


@pytest.mark.parametrize("given, expected_result", test_data)
def test_sanitize_html(given, expected_result):
    # Given an encoded html string without any tags
    html = b64_encode(given)

    # When the string is sanitized
    res = sanitise_html(html)

    # Then the result should be cleaned
    assert res == expected_result


def test_sanitise_html_file():
    # Given an html file
    html = Path("tests/data/raw_exchange.html").read_text(encoding='utf-8')

    # When the html is sanitized
    res = sanitise_html(b64_encode(html))

    # Then the result should have the extended tags/attributes
    assert "class=\"nt\"" in res
    assert "div class=\"highlight\"" in res
    assert "<h2>" in res
