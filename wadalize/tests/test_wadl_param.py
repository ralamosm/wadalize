import pytest
from lxml import etree

from wadalize import WADLParam


def test_ok_no_default_value():
    param = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:double" \
            style="query" name="foo"/>'
    )
    wp = WADLParam(param)

    assert wp.name == "foo" and wp.style == "query" and wp.type == "xs:double" and wp.value is None


def test_ok_default_value():
    param = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:double" \
            style="query" name="foo" default="bar" />'
    )
    wp = WADLParam(param)

    assert wp.name == "foo" and wp.style == "query" and wp.type == "xs:double" and wp.value == "bar"


def test_ok_default_values_list():
    param = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:double" \
            style="query" name="foo"/>'
    )
    wp = WADLParam(param, default_values=dict(foo="bar"))

    assert wp.name == "foo" and wp.style == "query" and wp.type == "xs:double" and wp.value == "bar"


def test_wrong_element_no_name():
    param = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:double" \
            style="query" />'
    )

    with pytest.raises(ValueError):
        WADLParam(param)


def test_ok_default_values_precedence_over_default_param():
    param = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:double" \
            style="query" name="foo" default="yolo" />'
    )
    wp = WADLParam(param, default_values=dict(foo="bar"))

    assert wp.value == "bar"


def test_wrong_element_no_style():
    param = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" \
            type="xs:double" name="foo" />'
    )

    with pytest.raises(ValueError):
        WADLParam(param)


def test_wrong_element_no_name_no_style():
    param = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" \
            type="xs:double" />'
    )

    with pytest.raises(ValueError):
        WADLParam(param)


def test_ok_dump_as_dict():
    param = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:double" \
            style="query" name="foo" default="bar" />'
    )
    wp = WADLParam(param)

    assert wp.dump_as_dict() == dict(name="foo", style="query", value="bar", type="xs:double")


def test_eq_comparison():
    param1 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo" \
            style="header" type="xs:double" />'
    )
    param2 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo" \
            style="header" type="xs:int" />'
    )

    wp1 = WADLParam(param1)
    wp2 = WADLParam(param2)

    assert wp1 == wp2


def test_ne_comparison_diff_name():
    param1 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo1" \
            style="header" type="xs:double" />'
    )
    param2 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo2" \
            style="header" type="xs:int" />'
    )

    wp1 = WADLParam(param1)
    wp2 = WADLParam(param2)

    assert wp1 != wp2


def test_ne_comparison_diff_style():
    param1 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo" \
            style="header" type="xs:double" />'
    )
    param2 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="foo" \
            style="query" type="xs:int" />'
    )

    wp1 = WADLParam(param1)
    wp2 = WADLParam(param2)

    assert wp1 != wp2


def test_lt():
    param1 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="abc" \
            style="header" type="xs:double" />'
    )
    param2 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" \
            name="def" style="query" type="xs:int" />'
    )

    wp1 = WADLParam(param1)
    wp2 = WADLParam(param2)

    assert wp1 < wp2


def test_not_lt():
    param1 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="def" \
            style="header" type="xs:double" />'
    )
    param2 = etree.XML(
        '<param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="abc" \
            style="query" type="xs:int" />'
    )

    wp1 = WADLParam(param1)
    wp2 = WADLParam(param2)

    assert wp1 > wp2
