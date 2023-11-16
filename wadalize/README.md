# WADALIZE

Class and script allowing to manipulate [WADL](https://es.wikipedia.org/wiki/Web_Application_Description_Language) files.

## Usage

```python
from wadalize import WADLHandler

wh = WADLHandler(
        wadl_string,
        base=base,
        default_values=default_values
    )

for wr in wh.requests:
    # turn into a python request
    rj = wr.dump_as_json(proxies=PROXIES)

    # output or smth...
```
