import pytest
from lxml import etree

from wadalize import WADLRequest
from wadalize.models import Request


def test_ok_no_params():
    wr = WADLRequest("https://example.com/api/yolo", "POST")
    assert wr.location == "https://example.com/api/yolo" and wr.method == "POST" and len(wr.params) == 0


def test_ok_params():
    params = []
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo1" \
                style="header" type="xs:double" />'
        )
    )
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo2" \
                style="header" type="xs:double" />'
        )
    )
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo3" \
                style="header" type="xs:double" />'
        )
    )

    wr = WADLRequest("https://example.com/api/yolo", "POST", params=params)

    assert len(wr.params) == 3


def test_dump_as_dict():
    params = []
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo1" \
                style="header" type="xs:double" />'
        )
    )
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo2" \
                style="header" type="xs:double" />'
        )
    )
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo3" \
                style="header" type="xs:double" />'
        )
    )

    wr = WADLRequest("https://example.com/api/yolo", "POST", params=params)
    jr = wr.dump_as_dict()

    assert jr["location"] == wr.location
    assert jr["method"] == wr.method
    assert jr["params"] == [
        {
            "name": "foo1",
            "type": "xs:double",
            "style": "header",
            "value": None,
        },
        {
            "name": "foo2",
            "type": "xs:double",
            "style": "header",
            "value": None,
        },
        {
            "name": "foo3",
            "type": "xs:double",
            "style": "header",
            "value": None,
        },
    ]


def test_dump_as_request():
    params = []
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo1" \
                style="header" type="xs:double" />'
        )
    )
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo2" \
                style="query" type="xs:double" />'
        )
    )
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo3" \
                style="query" type="xs:double" />'
        )
    )
    params.append(
        etree.XML(
            '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo3" \
                style="template" type="xs:double" />'
        )
    )

    wr = WADLRequest("https://example.com/api/yolo", "POST", params=params)
    r = wr.dump_as_request()
    assert isinstance(r, Request)
    assert str(r.url) == "https://example.com/api/yolo?foo2=&foo3="
    assert r.method == "POST"
    assert len(r.headers.keys()) == 1
    assert len(r.query.keys()) == 2


def test_har_not_implemented():
    wr = WADLRequest("https://example.com/api/yolo", "POST")

    with pytest.raises(NotImplementedError):
        wr.dump_as_har()
