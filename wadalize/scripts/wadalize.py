import sys

import click
import requests
import urllib3

from wadalize import WADLHandler

urllib3.disable_warnings()


def open_or_get(source, allow_redirects=False):
    """
    Returns the content of a local file or HTTP url

    Raises all exceptions without catching them.
    """
    if not (source.startswith("http://") or source.startswith("https://")):
        # This is a local file
        with open(source, "r") as file:
            wadl_string = file.read()
    else:
        # This is a url. We don't care about the status returned,
        # just the content
        r = requests.get(source, verify=False, allow_redirects=allow_redirects)
        wadl_string = r.content

    return wadl_string


def output_params(wadl_string):
    wh = WADLHandler(wadl_string)
    params = []

    for wr in wh.requests:
        for p in wr.params:
            if p.name not in params:
                params.append(p.name)

    params = sorted(map(lambda x: "{}:".format(x), params))
    return "\n".join(params)


def output_urls(wadl_string, base, headers, default_values, query_params):
    wh = WADLHandler(wadl_string, base=base, default_values=default_values)

    for wr in wh.requests:
        # turn into a python request
        req = wr.dump_as_request()

        click.echo(req.url)


def run_requests(wadl_string, base, headers, default_values, query_params, deny_methods):
    wh = WADLHandler(wadl_string, base=base, default_values=default_values)

    for wr in wh.requests:
        # turn into a python request
        req = wr.dump_as_request()

        if req.method.upper() in deny_methods:
            # Do not run deny methods
            continue

        # add the given header and query string parameters
        req.headers.update(headers)
        req.params.update(query_params)

        # run request!
        requests.request(req.method, str(req.url), verify=False, headers=req.headers)
        click.echo("METHOD: {}, URL: {}, HEADERS: {}".format(wr.method, wr.location, wr.headers))


def get_params_from_string(data_str):
    return dict(map(lambda z: z.strip(), x.split(":", 1)) for x in data_str.split("\n") if x)


@click.command()
@click.option(
    "-b",
    "--base",
    help="Base location to use when \
    parsing the WADL file.",
)
@click.option("-H", "--headers", default=[], help='The response headers instance. Example: -H "Location:evil.com"', multiple=True)
@click.option("-p", "--params", default=[], help="Default value for any given param name. Example: -p sort:asc", multiple=True)
@click.option("-q", "--query-params", default=[], help="A query string param name and value. Example: -q pi:3.14", multiple=True)
@click.option(
    "-dm",
    "--deny-methods",
    help="Comma separated list of HTTP verbs to avoid when running \
        the requests. No values are checked.",
)
@click.option(
    "--dump-params",
    is_flag=True,
    default=False,
    help="Use this option when you only want to dump the list of params \
        of your WADL file.",
)
@click.option(
    "--dump-urls",
    is_flag=True,
    default=False,
    help="Use this option when you only want to dump the list of urls \
        of your WADL file.",
)
@click.option(
    "-f",
    "--use-file",
    type=click.Path(exists=True),
    required=False,
    help="Pass a file as a source of params values. Required \
    format: key1:val1\nkey2:val2\n...\nkeyN:valN. Params passed \
    by command line take precedence.",
)
@click.argument("source")
def run(base, headers, params, query_params, deny_methods, dump_params, dump_urls, use_file, source):
    """
    Script that receives a WADL source from a file path or url, and does one of
    two things with it:

    1) If given the --dump-params param, it dumps a list of all the params from
        the different requests found on the WADL.

    2) Else, it RUNS all the calls of the WADL source, using the different
        parameters to fill on different aspects of the parsing: base url,
        include given headers, query string parameters and param default
        values.

    Obviously both options implicitly interpret the WADL source using our
    WADLHandler class.
    """

    try:
        wadl_string = open_or_get(source)
    except IOError as e:
        raise click.ClickException(e)
    except requests.exceptions.ConnectionError:
        raise click.ClickException("Couldn't connect to the given url.")

    # If we got to dump the params do it and exit
    if dump_params:
        click.echo(output_params(wadl_string))
        sys.exit(0)

    # Turns deny_methods into a list
    if deny_methods:
        deny_methods = [x.upper().strip() for x in deny_methods.split(",") if x]
    else:
        deny_methods = []

    # Check if we got use params
    default_values = {}
    if use_file:
        # Get params from file
        try:
            with open(use_file) as f:
                default_values = get_params_from_string(f.read())
        except ValueError:
            raise click.ClickException(
                "The input file is not in the required format. Eg. \
                    key1:val1\nkey2:val2\n...\nkeyN:valN"
            )

    # params passed by -p options take precedence over those from --use-file
    try:
        default_values.update(dict(map(lambda z: z.strip(), x.split(":", 1)) for x in params))
    except ValueError:
        pass

    # Preparing params
    try:
        headers = dict(map(lambda z: z.strip(), x.split(":", 1)) for x in headers)
    except ValueError:
        headers = {}

    try:
        query_params = dict(map(lambda z: z.strip(), x.split(":", 1)) for x in query_params)
    except ValueError:
        query_params = {}

    # Run requests with the available parameters
    if dump_urls:
        output_urls(wadl_string, base, headers, default_values, query_params)
        sys.exit(0)
    else:
        run_requests(wadl_string, base, headers, default_values, query_params, deny_methods=deny_methods)


if __name__ == "__main__":
    run()
