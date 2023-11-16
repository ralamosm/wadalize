import pytest

from wadalize import WADLHandler

WADL_SAMPLE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<application xmlns="http://wadl.dev.java.net/2009/02">
    <doc xmlns:jersey="http://jersey.java.net/" jersey:generatedBy="Jersey:
        2.28 2019-01-25 15:18:13"/>
    <doc xmlns:jersey="http://jersey.java.net/"
        jersey:hint="This is simplified WADL with user and core resources only.
        To get full WADL with extended resources use the query parameter detail
        Link:
        http://openapi.paas.example.com:4443/api/application.wadl?detail=true"
    />
    <grammars/>
    <resources base="https://example.com/api">
        <resource path="/affiliate/v1">
            <resource path="/categories/tree">
                <method id="getCategoryTree" name="POST">
                    <request>
                        <representation mediaType="application/json"/>
                    </request>
                    <response>
                        <representation mediaType="application/json"/>
                    </response>
                </method>
            </resource>
            <resource path="/search/items">
                <method id="getItems" name="GET">
                    <request>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="q" style="query" type="xs:string"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="property" style="query" type="xs:string"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="offset" style="query" type="xs:int"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="limit" style="query" type="xs:int"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="categoryId" style="query" type="xs:int"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="categoryLevel" style="query" type="xs:int"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="sellerId" style="query" type="xs:string"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="maximumPrice" style="query" type="xs:int"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="minimumPrice" style="query" type="xs:int"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="sort" style="query" type="xs:string"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="cluster" style="query" type="xs:string"/>
                    </request>
                    <response>
                        <representation
                        mediaType="application/json;charset=utf-8"/>
                    </response>
                </method>
            </resource>
        </resource>
        <resource path="/access/{action}">
            <param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="action"
                style="template" type="xs:string"/>
            <method id="getResourceAccessExt" name="GET">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                        name="resource" style="query" type="xs:string"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                        name="domain" style="query" type="xs:string"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                        name="principal" style="query" type="xs:string"/>
                </request>
                <response>
                    <representation mediaType="application/json"/>
                </response>
            </method>
        </resource>
    </resources>
</application>"""


def test_ok_wadl_string():
    ah = WADLHandler(WADL_SAMPLE)
    assert len(ah.requests) == 3


def test_fail_no_wadl_string():
    with pytest.raises(ValueError, match=r"You need to pass a WADL string to be parsed"):
        WADLHandler()


def test_fail_non_xml_string():
    with pytest.raises(ValueError, match=r"XML syntax error"):
        WADLHandler("yolooooo")


def test_check_requests():
    ah = WADLHandler(WADL_SAMPLE, default_values={"action": "create"})
    values = [
        {
            "method": "POST",
            "url": "https://example.com/api/affiliate/v1/categories/tree",
            "num_params": 0,
        },
        {
            "method": "GET",
            "url": "https://example.com/api/affiliate/v1/search/items",
            "num_params": 11,
        },
        {
            "method": "GET",
            "url": "https://example.com/api/access/create",
            "num_params": 4,
        },
    ]

    for num, req in enumerate(ah.requests):
        assert req.method == values[num]["method"]
        assert req.location == values[num]["url"]
        assert len(req.params) == values[num]["num_params"]


def test_check_requests_rebase():
    ah = WADLHandler(
        WADL_SAMPLE,
        base="https://rebase.com",
        default_values={"action": "create"},
    )
    values = [
        {
            "method": "POST",
            "url": "https://rebase.com/affiliate/v1/categories/tree",
            "num_params": 0,
        },
        {
            "method": "GET",
            "url": "https://rebase.com/affiliate/v1/search/items",
            "num_params": 11,
        },
        {
            "method": "GET",
            "url": "https://rebase.com/access/create",
            "num_params": 4,
        },
    ]

    for num, req in enumerate(ah.requests):
        assert req.method == values[num]["method"]
        assert req.location == values[num]["url"]
        assert len(req.params) == values[num]["num_params"]


def test_check_requests_no_default_values():
    ah = WADLHandler(WADL_SAMPLE)
    values = [
        {
            "method": "POST",
            "url": "https://example.com/api/affiliate/v1/categories/tree",
            "num_params": 0,
        },
        {
            "method": "GET",
            "url": "https://example.com/api/affiliate/v1/search/items",
            "num_params": 11,
        },
        {
            "method": "GET",
            "url": "https://example.com/api/access/{action}",
            "num_params": 4,
        },
    ]

    for num, req in enumerate(ah.requests):
        assert req.method == values[num]["method"]
        assert req.location == values[num]["url"]
        assert len(req.params) == values[num]["num_params"]
