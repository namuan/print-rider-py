from bleach.sanitizer import ALLOWED_ATTRIBUTES

EXTENDED_ALLOWED_TAGS = [
    "a", "b", "blockquote", "br", "caption", "cite", "code", "col",
    "colgroup", "dd", "div", "dl", "dt", "em", "h1", "h2", "h3", "h4", "h5", "h6",
    "i", "img", "li", "ol", "p", "pre", "q", "small", "span", "strike", "strong",
    "sub", "sup", "table", "tbody", "td", "tfoot", "th", "thead", "tr", "u",
    "ul"]

EXTENDED_ALLOWED_ATTRS = {**ALLOWED_ATTRIBUTES, **{"*": ["class"]}}
