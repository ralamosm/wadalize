# wadalize

Class and script allowing to manipulate [WADL](https://es.wikipedia.org/wiki/Web_Application_Description_Language) files.

## Class Usage

```python
from wadalize import WADLHandler

wh = WADLHandler(
        wadl_string,
        base=base,
        default_values=default_values
    )

for wr in wh.requests:
    # turn into a python request
    rj = wr.dump_as_dict(proxies=PROXIES)

    # output or smth...
```

# Cli usage

`wadalize` is an script capable of processing a WADL source to dump its list of params or run the requests. The script works
by receiving a WADL source (a local file or a url) and executing the corresponding action. **Its main goal is
to help process a WADL source, quickly do mass-assignment for param names and then run the requests so I can
get a quick look at how the API described by the WADL source works**.

## Help

```console
$ wadalize --help
Usage: wadalize [OPTIONS] SOURCE

  Script that receives a WADL source from a file path or url, and does one
  of two things with it:

  1) If given the --dump-params param, it dumps a list of all the params
  from the different requests found on the WADL.

  2) Else, it RUNS all the calls of the WADL source, using the different
  parameters to fill on different aspects of the parsing: base url,
  include given headers, query string parameters and param default values.

  Obviously both options implicitly interpret the WADL source using our
  WADLHandler class.

Options:
  -b, --base TEXT           Base location to use when parsing the WADL file.
  -H, --headers TEXT        The response headers instance. Example: -H
                            "Location:evil.com"

  -p, --params TEXT         Default value for any given param name. Example:
                            -p sort:asc

  -q, --query-params TEXT   A query string param name and value. Example: -q
                            pi:3.14

  -dm, --deny-methods TEXT  Comma separated list of HTTP verbs to avoid when
                            running the requests. No values are checked.

  --dump-params             Use this option when you only want to dump the
                            list of params of your WADL file.

  -f, --use-file PATH       Pass a file as a source of params values. Required
                            format: key1:val1 key2:val2 ... keyN:valN. Params
                            passed by command line take precedence.

  --help                    Show this message and exit.
```

## Description

As explained above, `--dump-params` simply returns the list of all params used on the WADL source, without
differentiating the call where they may appear. Actually, if you think about it, the same param name may mean
more than one thing depending on the call. For example `id` might be an object id for one call, and another kind
of object id in another, but the param name `id` will appear only once in the output list.

Getting this list of params helps when later using the `--use-file` option.

If you don't use `--dump-params` then the file is processed in order to execute each and every request contained
in the WADL source.

## Usage Examples

Dump the list of params of a WADL url

```console
$ wadalize --dump-params http://example.com/some/file.wadl | tee a.txt
acquire:
act:
actId:
authToken:
backwardCompatible:
bankCode:
bankGroup:
campaignEventId:
campaignId:
campaignIds:
categoryId:
categoryLevel:
```

> Now you can modify the file `a.txt` and given a value to the params of your choice, simply adding the value after the colon on each line.

Run all the requests from the same source, using file `a.txt` from above as the source for the param values. This execution
won't generate any output but will execute all the requests contained in the WADL file. You can watch requests
as they go through by looking at your proxy

```console
$ wadalize -f a.txt http://example.com/some/file.wadl
```

Or you can pass multiple parameter values from the command line and run the requests. The requests that hold those param names you passed as parameter will be filled with the values you sent

```console
$ wadalize -p actId:31415 -p bankCode:BCS -p campaignId:28182 http://example.com/some/file.wadl
```

Let's say you don't want to run DELETE nor PUT methods, you would do it with the `--deny-methods` option, like this

```console
$ wadalize --deny-methods "DELETE,PUT" -p actId:31415 -p bankCode:BCS -p campaignId:28182 http://example.com/some/file.wadl
```

Say you need to pass some headers to all calls in your WADL source. You can do it like this

```console
$ wadalize -H "Authorization:Bearer 123" -H "Content-Type:application/json" -p actId:31415 -p bankCode:BCS -p campaignId:28182 http://example.com/some/file.wadl
```

or maybe you need to pass a special query string value as an anti-CSRF token, on every request

```console
$ wadalize -q csrftoken:bGVzb3l1bnRva2Vu -H "Authorization:Bearer 123" -H "Content-Type:application/json" -p actId:31415 -p bankCode:BCS -p campaignId:28182 http://example.com/some/file.wadl
```

Finally, in case you need to change the base url for all your requests, you simply use `-b`

```console
$ wadalize -b https://proddomain.com/api/v1/ -q csrftoken:bGVzb3l1bnRva2Vu -H "Authorization:Bearer 123" -H "Content-Type:application/json" -p actId:31415 -p bankCode:BCS -p campaignId:28182 http://example.com/some/file.wadl
```
