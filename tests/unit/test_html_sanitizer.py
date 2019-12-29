import pytest

from printrider.utils import sanitise_html, b64_encode

test_data = [
    ("Hello World", "Hello World"),
    ("<strong>Hello</strong>", "<strong>Hello</strong>"),
    ("<script>alert('hello')</script>", "&lt;script&gt;alert('hello')&lt;/script&gt;")
]


@pytest.mark.parametrize("given, expected_result", test_data)
def test_sanitize_html(given, expected_result):
    # Given an encoded html string without any tags
    html = b64_encode(given)

    # When the string is sanitized
    res = sanitise_html(html)

    # Then the result should be cleaned
    assert res == expected_result
