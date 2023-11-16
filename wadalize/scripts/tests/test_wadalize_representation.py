import responses
from click.testing import CliRunner

from wadalize import WADLHandler
from wadalize.scripts.wadalize import run as wadalize


WADL_SAMPLE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<application xmlns="http://wadl.dev.java.net/2009/02">
    <doc xmlns:jersey="http://jersey.java.net/"
        jersey:generatedBy="Jersey: 2.15 ${buildNumber}"/>
    <doc xmlns:jersey="http://jersey.java.net/"
        jersey:hint="This is simplified WADL with user and core resources "/>
    <grammars/>
    <resources base="https://cdn.example.com/xb">
        <resource path="/v1/finance/w/importPortfolio">
            <method id="importPortfolioViaForm" name="POST">
                <request>
                    <representation
                        mediaType="application/x-www-form-urlencoded">
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="portfolio" style="query" type="xs:string"/>
                    </representation>
                </request>
                <response>
                    <representation mediaType="application/json"/>
                </response>
            </method>
            <method id="importPortfolioViaJson" name="POST">
                <request>
                    <representation mediaType="application/json"/>
                </request>
                <response>
                    <representation mediaType="application/json"/>
                </response>
            </method>
            <method id="importPortfolio" name="POST">
                <request>
                    <representation mediaType="text/plain"/>
                    <representation mediaType="text/csv"/>
                </request>
                <response>
                    <representation mediaType="application/json"/>
                </response>
            </method>
            <method id="importPortfolioViaFormOptions" name="OPTIONS">
                <request>
                    <representation
                        mediaType="application/x-www-form-urlencoded"/>
                </request>
                <response>
                    <representation mediaType="*/*"/>
                </response>
            </method>
        </resource>
        <resource path="/v1/finance/m/importPortfolio">
            <method id="importPortfolio" name="POST">
                <request>
                    <representation mediaType="text/plain"/>
                    <representation mediaType="text/csv"/>
                </request>
                <response>
                    <representation mediaType="application/json"/>
                </response>
            </method>
            <method id="importPortfolioViaForm" name="POST">
                <request>
                    <representation
                        mediaType="application/x-www-form-urlencoded">
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
                            name="portfolio" style="query" type="xs:string"/>
                    </representation>
                </request>
                <response>
                    <representation mediaType="application/json"/>
                </response>
            </method>
            <method id="importPortfolioViaJson" name="POST">
                <request>
                    <representation mediaType="application/json"/>
                </request>
                <response>
                    <representation mediaType="application/json"/>
                </response>
            </method>
        </resource>
    </resources>
</application>"""


def test_request_amount():
    wh = WADLHandler(WADL_SAMPLE)
    assert len(wh.requests) == 9


def test_header_representation():
    wh = WADLHandler(WADL_SAMPLE)
    conten_type_rep = []
    conten_type_rep.append("application/x-www-form-urlencoded")
    conten_type_rep.append("application/json")
    conten_type_rep.append("text/plain")
    conten_type_rep.append("text/csv")
    conten_type_rep.append("application/x-www-form-urlencoded")
    conten_type_rep.append("text/plain")
    conten_type_rep.append("text/csv")
    conten_type_rep.append("application/x-www-form-urlencoded")
    conten_type_rep.append("application/json")

    for i, req in enumerate(wh.requests):
        assert req.headers.get("Content-Type") == conten_type_rep[i]


@responses.activate
def test_check_override_header():
    responses.add(
        responses.POST,
        "https://cdn.example.com/xb/v1/finance/w/importPortfolio",
        status=200,
    )
    responses.add(
        responses.OPTIONS,
        "https://cdn.example.com/xb/v1/finance/w/importPortfolio",
        status=200,
    )
    responses.add(
        responses.POST,
        "https://cdn.example.com/xb/v1/finance/m/importPortfolio",
        status=200,
    )

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test_repre.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        header_custom = "type-custom"
        runner.invoke(
            wadalize,
            ["-H", "Content-Type:{}".format(header_custom), "test_repre.wadl"],
        )

        for req in responses.calls:
            assert req.request.headers.get("Content-Type") == header_custom


@responses.activate
def test_param_representation():
    responses.add(
        responses.POST,
        "https://cdn.example.com/xb/v1/finance/w/importPortfolio",
        status=200,
    )
    responses.add(
        responses.OPTIONS,
        "https://cdn.example.com/xb/v1/finance/w/importPortfolio",
        status=200,
    )
    responses.add(
        responses.POST,
        "https://cdn.example.com/xb/v1/finance/m/importPortfolio",
        status=200,
    )

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test_repre.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        runner.invoke(wadalize, ["-p", "portfolio:test", "test_repre.wadl"])

        for i, req in enumerate(responses.calls):
            if i in [0, 7]:
                assert req.request.params.get("portfolio") == "test"
            else:
                assert req.request.params == {}
