import mock
import pytest
import requests
import responses
from click.testing import CliRunner

from wadalize.scripts.wadalize import get_params_from_string
from wadalize.scripts.wadalize import open_or_get
from wadalize.scripts.wadalize import run as wadalize


WADL_SAMPLE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<application xmlns="http://wadl.dev.java.net/2009/02">
    <doc xmlns:jersey="http://jersey.java.net/"
        jersey:generatedBy="Jersey: 2.28 2019-01-25 15:18:13"/>
    <doc xmlns:jersey="http://jersey.java.net/"
        jersey:hint="This is simplified WADL with user and core resources
        only. To get full WADL with extended resources use the query parameter
        detail. Link:
        http://openapi.paas.example.com:4443/api/application.wadl?detail=true"/>
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
                        name="principal" style="header" type="xs:string"/>
                </request>
                <response>
                    <representation mediaType="application/json"/>
                </response>
            </method>
        </resource>
    </resources>
</application>"""


# This method will be used by mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, content, status_code):
            self.content = content
            self.status_code = status_code

    return MockResponse(WADL_SAMPLE, 200)


def mocked_requests_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, content, status_code):
            self.content = content
            self.status_code = status_code

    return MockResponse('{"status": true}', 200)


# Utils
def test_ok_get_params_from_string():
    input = "action:get\ndomain:example.com\nprincipal:main\nproperty\
        :shop\nq:select\nresource:mall\n"
    params = get_params_from_string(input)

    assert params == {"action": "get", "domain": "example.com", "principal": "main", "property": "shop", "q": "select", "resource": "mall"}


def test_open_or_get_file_does_not_exist():
    with pytest.raises(IOError, match=r"No such file or directory"):
        open_or_get("whatever-this-file-doesn-exist")


@responses.activate
def test_open_or_get_non_200_url():
    responses.add(responses.GET, "https://example.com/whatever", body="Not found lol", status=404)
    r = open_or_get("https://example.com/whatever")

    assert r == b"Not found lol"
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://example.com/whatever"
    assert responses.calls[0].response.text == "Not found lol"


def test_no_get_params_from_string():
    input = "g23hn0g923 \n\rg32g2g3232g:g3g2332g2\r\n\n\twhatever"
    with pytest.raises(ValueError, match=r"dictionary update sequence element"):
        get_params_from_string(input)


def test_no_get_params_from_string_empty():
    input = ""
    params = get_params_from_string(input)
    assert params == {}


# cli
def test_dump_params_local_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        result = runner.invoke(wadalize, ["--dump-params", "test.wadl"])
        assert result.exit_code == 0
        assert result.output == "action:\ndomain:\nprincipal:\nproperty:\nq:\nresource:\n"


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_dump_params_url(mock_get):
    runner = CliRunner()
    result = runner.invoke(wadalize, ["--dump-params", "https://example.com/api/application.wadl"])
    assert result.exit_code == 0
    assert result.output == "action:\ndomain:\nprincipal:\nproperty:\nq:\nresource:\n"

    for args_list in mock_get.call_args_list:
        _, kwargs = args_list
        if "verify" in kwargs:
            kwargs.pop("verify")

    assert mock.call("https://example.com/api/application.wadl", allow_redirects=False) in mock_get.call_args_list


@mock.patch("requests.request", side_effect=mocked_requests_request)
def test_ok_run_requests_no_filename(mock_request):
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        result = runner.invoke(
            wadalize,
            [
                "-b",
                "https://example.com/api/v1/",
                "-p",
                "q:test",
                "-p",
                "domain:condorito",
                "-p",
                "resource:accounts",
                "-p",
                "principal:main",
                "-p",
                "action:run",
                "-H",
                "x-yolo1:header1",
                "-H",
                "x-yolo2:header2",
                "test.wadl",
            ],
        )
        assert result.exit_code == 0
        assert mock_request.call_count == 3

        for args_list in mock_request.call_args_list:
            _, kwargs = args_list
            if "verify" in kwargs:
                kwargs.pop("verify")

        assert (
            mock.call(
                "POST",
                "https://example.com/api/v1/affiliate/v1/categories/tree",
                headers={"Content-Type": "application/json", "x-yolo1": "header1", "x-yolo2": "header2"},
            )
            in mock_request.call_args_list
        )
        assert (
            mock.call(
                "GET",
                "https://example.com/api/v1/affiliate/v1/search/items?q=test&property=",
                headers={"x-yolo1": "header1", "x-yolo2": "header2"},
            )
            in mock_request.call_args_list
        )
        assert (
            mock.call(
                "GET",
                "https://example.com/api/v1/access/run?resource=accounts&domain=condorito",
                headers={"principal": "main", "x-yolo1": "header1", "x-yolo2": "header2"},
            )
            in mock_request.call_args_list
        )


@mock.patch("requests.request", side_effect=mocked_requests_request)
def test_ok_run_requests_with_filename(mock_request):
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        with open("params.txt", "w") as f:
            f.write(
                "q:test_file\ndomain:example.com\nresource:shop\nprincipal:\
                    one\naction:delete"
            )

        result = runner.invoke(
            wadalize, ["-b", "https://example.com/api/v1/", "-f", "params.txt", "-H", "x-yolo1:header1", "-H", "x-yolo2:header2", "test.wadl"]
        )
        assert mock_request.call_count == 3
        assert result.exit_code == 0

        for args_list in mock_request.call_args_list:
            _, kwargs = args_list
            if "verify" in kwargs:
                kwargs.pop("verify")

        assert (
            mock.call(
                "POST",
                "https://example.com/api/v1/affiliate/v1/categories/tree",
                headers={"Content-Type": "application/json", "x-yolo1": "header1", "x-yolo2": "header2"},
            )
            in mock_request.call_args_list
        )
        assert (
            mock.call(
                "GET",
                "https://example.com/api/v1/affiliate/v1/search/items?q=test_file&property=",
                headers={"x-yolo1": "header1", "x-yolo2": "header2"},
            )
            in mock_request.call_args_list
        )
        assert (
            mock.call(
                "GET",
                "https://example.com/api/v1/access/delete?resource=shop&domain=example.com",
                headers={"principal": "one", "x-yolo1": "header1", "x-yolo2": "header2"},
            )
            in mock_request.call_args_list
        )


@mock.patch("requests.request", side_effect=mocked_requests_request)
def test_ok_run_requests_with_filename_cli_precedence(mock_request):
    # Demonstrates params passed as -p over the cli take precedence over
    # those passed with -f
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        with open("params.txt", "w") as f:
            f.write(
                "q:test_file\ndomain:example.com\nresource:shop\nprincipal:\
                    one\naction:delete"
            )

        result = runner.invoke(
            wadalize,
            [
                "-b",
                "https://example.com/api/v1/",
                "-f",
                "params.txt",
                "-p",
                "q:cli_q",
                "-p",
                "action:cli_action",
                "-H",
                "x-yolo1:header1",
                "-H",
                "x-yolo2:header2",
                "test.wadl",
            ],
        )
        assert mock_request.call_count == 3
        assert result.exit_code == 0

        for args_list in mock_request.call_args_list:
            _, kwargs = args_list
            if "verify" in kwargs:
                kwargs.pop("verify")

        assert (
            mock.call(
                "POST",
                "https://example.com/api/v1/affiliate/v1/categories/tree",
                headers={"Content-Type": "application/json", "x-yolo1": "header1", "x-yolo2": "header2"},
            )
            in mock_request.call_args_list
        )
        assert (
            mock.call(
                "GET",
                "https://example.com/api/v1/affiliate/v1/search/items?q=cli_q&property=",
                headers={"x-yolo1": "header1", "x-yolo2": "header2"},
            )
            in mock_request.call_args_list
        )
        assert (
            mock.call(
                "GET",
                "https://example.com/api/v1/access/cli_action?resource=shop&domain=example.com",
                headers={"principal": "one", "x-yolo1": "header1", "x-yolo2": "header2"},
            )
            in mock_request.call_args_list
        )


@responses.activate
def test_ok_deny_methods():
    """Tests --deny-methods param, making sure only 2 requests of the test
    WADL are ran given we deny POST"""
    responses.add(responses.POST, "https://example.com/w/v1/affiliate/v1/categories/tree", body="yolo", status=200)
    responses.add(responses.GET, "https://example.com/w/v1/affiliate/v1/search/items", body="yolo", status=200)
    responses.add(responses.GET, "https://example.com/w/v1/access/run", body="yolo", status=200)

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        result = runner.invoke(
            wadalize,
            [
                "-b",
                "https://example.com/w/v1/",
                "--deny-methods",
                "POST",
                "-p",
                "q:test",
                "-p",
                "domain:condorito",
                "-p",
                "resource:accounts",
                "-p",
                "principal:main",
                "-p",
                "action:run",
                "-H",
                "x-yolo1:header1",
                "-H",
                "x-yolo2:header2",
                "test.wadl",
            ],
        )

        assert result.exit_code == 0
        assert len(responses.calls) == 2
        assert responses.calls[0].request.url == "https://example.com/w/v1/affiliate/v1/search/items?q=test&property="
        assert responses.calls[1].request.url in (
            "https://example.com/w/v1/access/run?resource=accounts&domain=condorito",
            "https://example.com/w/v1/access/run?domain=condorito&resource=accounts",
        )


@responses.activate
def test_ok_multiple_deny_methods():
    """Tests --deny-methods param, making NO requests are fired if we deny
    POST and GET while parsing our test WADL source"""
    responses.add(responses.POST, "https://example.com/w/v1/affiliate/v1/categories/tree", body="yolo", status=200)
    responses.add(responses.GET, "https://example.com/w/v1/affiliate/v1/search/items", body="yolo", status=200)
    responses.add(responses.GET, "https://example.com/w/v1/access/run", body="yolo", status=200)

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        result = runner.invoke(
            wadalize,
            [
                "-b",
                "https://example.com/w/v1/",
                "--deny-methods",
                "POST,GET",
                "-p",
                "q:test",
                "-p",
                "domain:condorito",
                "-p",
                "resource:accounts",
                "-p",
                "principal:main",
                "-p",
                "action:run",
                "-H",
                "x-yolo1:header1",
                "-H",
                "x-yolo2:header2",
                "test.wadl",
            ],
        )

        assert result.exit_code == 0
        assert len(responses.calls) == 0


@responses.activate
def test_ok_deny_methods_no_methods_deny():
    """Tests --deny-methods param allows any method if set to empty string"""
    responses.add(responses.POST, "https://example.com/w/v1/affiliate/v1/categories/tree", body="yolo", status=200)
    responses.add(responses.GET, "https://example.com/w/v1/affiliate/v1/search/items", body="yolo", status=200)
    responses.add(responses.GET, "https://example.com/w/v1/access/run", body="yolo", status=200)

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        result = runner.invoke(
            wadalize,
            [
                "-b",
                "https://example.com/w/v1/",
                "--deny-methods",
                "",
                "-p",
                "q:test",
                "-p",
                "domain:condorito",
                "-p",
                "resource:accounts",
                "-p",
                "principal:main",
                "-p",
                "action:run",
                "-H",
                "x-yolo1:header1",
                "-H",
                "x-yolo2:header2",
                "test.wadl",
            ],
        )

        assert result.exit_code == 0
        assert len(responses.calls) == 3
        assert responses.calls[0].request.url == "https://example.com/w/v1/affiliate/v1/categories/tree"
        assert responses.calls[1].request.url == "https://example.com/w/v1/affiliate/v1/search/items?q=test&property="
        assert responses.calls[2].request.url in (
            "https://example.com/w/v1/access/run?resource=accounts&domain=condorito",
            "https://example.com/w/v1/access/run?domain=condorito&resource=accounts",
        )


def test_fail_run_requests_with_filename_file_not_found():
    """Tests wadalize exists with an error if the WADL source is a file path
    that doesn't exists"""
    runner = CliRunner()
    result = runner.invoke(
        wadalize, ["-b", "https://example.com/api/v1/", "-f", "params.txt", "-H", "x-yolo1:header1", "-H", "x-yolo2:header2", "test.wadl"]
    )
    assert result.exit_code == 2
    assert "Invalid value for '-f'" in result.output


@mock.patch("requests.request", side_effect=mocked_requests_request)
def test_fail_run_requests_with_filename_wrong_syntax(mock_request):
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        with open("params.txt", "w") as f:
            f.write("\r\nb9n290b23\nff   fsa\tdd:yolo\r\n\n\n g2930()")

        result = runner.invoke(
            wadalize, ["-b", "https://example.com/api/v1/", "-f", "params.txt", "-H", "x-yolo1:header1", "-H", "x-yolo2:header2", "test.wadl"]
        )
        assert mock_request.call_count == 0
        assert result.exit_code == 1
        assert "The input file is not in the required format" in result.output


@responses.activate
def test_fail_connection_error():
    """Tests wadalize exits with an error if the given url returns \
        connection error"""
    responses.add(responses.GET, "https://example.com/yolo.wadl", body=requests.exceptions.ConnectionError("Connection error"))

    runner = CliRunner()
    result = runner.invoke(wadalize, ["https://example.com/yolo.wadl"])
    assert result.exit_code == 1
    assert "Connection error" in result.output


def test_fail_file_not_found():
    runner = CliRunner()
    result = runner.invoke(wadalize, ["idonotexist"])
    assert result.exit_code == 1
    assert "No such file or directory" in result.output
