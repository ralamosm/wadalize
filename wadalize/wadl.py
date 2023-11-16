import re
from urllib.parse import unquote
from urllib.parse import urlparse
from urllib.parse import urlunparse

import exrex
from furl import furl
from lxml import etree

from .models import Request


class WADLHandler:
    """
    WADL Files Parser
    Args:
        from_string (str): WADL string to be parsed.
        base (str): Base url to replace the value from argument
        <resources base="...">.
        default_values (dict): Dictionary holding default values to be used in
        place of params found in the WADL file.
    Attributes:
        _requests (list of WADLRequest): List of parsed requests from the WADL
        file.
    Properties:
        requests (list of WADLRequest): This is just a "front end" for the
        _requests attribute.
    """

    def __init__(self, from_string=None, base=None, default_values={}):
        if not from_string:
            raise ValueError("You need to pass a WADL string to be parsed")

        try:
            if isinstance(from_string, bytes):
                self.root = etree.fromstring(from_string)
            else:
                self.root = etree.fromstring(from_string.encode())
            self.ns = self.root.tag.replace("application", "")
        except etree.XMLSyntaxError as e:
            raise ValueError("XML syntax error: {}".format(e))

        self.base = base
        # Sometimes we want to override the base attribute of the
        # main <resources> element.
        self.default_values = default_values
        # Dict with pairs of name of var -> value, to be used in
        # place of params
        self._requests = []

    def _tag(self, tag):
        return "{}{}".format(self.ns, tag)

    def _format_default_values(self, url):
        """Method that takes care of replacing {param} placeholders with
        their default values"""

        for key, val in self.default_values.items():
            url = url.replace("{" + key + "}", val)

        return url

    def _normalize_url(self, path_l):
        """This method normalizes a url generated from a list of url parts as
        obtained by the _parse method. After getting sure a "/" is the prefix
        for each of the elements of the path_l list of "url parts", except for
        the first one, it's the furl class the one at charge of actually
        normalizing the url
        """
        url = ""

        for num, path in enumerate(path_l):
            if num < (len(path_l) - 1) and not path.endswith("/"):
                path = "{}/".format(path)

            url = "{}{}".format(url, path)

        f = furl(self._format_default_values(url))
        f.path.normalize()
        return f.url

    @property
    def requests(self):
        """Returns a list with all the parsed requests for the given
        WADL string"""
        if not self._requests:
            # To parse each request, we look for each <method> element,
            # and pass it as param to the _parse method that will do the magic
            # to actually extract a request object from that point.
            for x in self.root.iter():
                if x.tag == self._tag("method"):
                    represn = self._getrepresentation(x)
                    if represn:
                        for i in represn:
                            self._requests.append(i)
                    else:
                        for i in self._parse(x):
                            self._requests.append(i)

        return self._requests

    def _getrepresentation(self, method):
        """
        Method that identifies whether a representation exists and its values
        are extracted
        If the representation has direct parameters,
        they are associated with the representation.
        """
        representation = []
        representation_final = []
        array_wadl = []

        path_l = []
        parent = method.getparent()

        for child in method.iter():
            if child.tag == self._tag("representation") and child.getparent().tag == self._tag("request"):
                representation.append(child)

        for r in representation:
            representation_param = []
            for child in r.iter():
                if child.tag == self._tag("param"):
                    representation_param.append(child)
            representation_final.append({"representation": r, "param": representation_param})

        while parent.tag != self._tag("application"):
            # Keep track of route parts
            if parent.tag == self._tag("resources"):
                path_l.insert(0, self.base if self.base else parent.get("base"))
            elif parent.tag == self._tag("resource"):
                path_l.insert(0, parent.get("path"))

            parent = parent.getparent()

        for i in representation_final:
            # Extract params of the url
            urls = self.param_url(unquote(self._normalize_url(path_l)))

            # In the end, return a array WADLRequest object representing the
            # given parsed request
            for url in urls:
                array_wadl.append(
                    WADLRequest(
                        url,
                        method=method.get("name"),
                        params=i.get("param"),
                        headers={"Content-Type": i.get("representation").get("mediaType")},
                        default_values=self.default_values,
                    )
                )
        return array_wadl

    def _parse(self, method):
        """Extract a request from the WADL string, starting from a <method> element.
        The goal of this task goes like this:
        - Build the complete URL/route to the given call, provided by the main
          <resources> method and the parent <resource> elements
          preceding the given <method> element. The HTTP method is obviously
          provided by the own <method> element.
        - Find all the associated <param> to the current request being parsed.
        By observation of several WADL samples, the parsing procedure was
        thought like this:
        - Parse inwards for all <param> children of the current <method>
            element, and keep track of them.
        - Parse outwards looking to build the url/route of this request
            (using <resources> and <resource>s) and parse any
            additional <param> element that's associated with a direct
            ancestor of the current <method> element. It's important not to mix
            in with <param>s which are associated with sibling <method>s or
            <resource> elements that are not direct ancestors.
        """

        path_l = []
        params = []
        array_wadl = []

        # Iterate inwards to find children params
        for child in method.iter():
            if child.tag == self._tag("param"):
                params.append(child)

        # Iterate outwards to fetch complete route and other params associated
        # with this request being parsed
        parent = method.getparent()
        while parent.tag != self._tag("application"):
            # Iterate inwards this parent to find other parameters
            for child in parent.iter():
                if child.tag == self._tag("param") and parent == child.getparent():
                    params.append(child)

            # Keep track of route parts
            if parent.tag == self._tag("resources"):
                path_l.insert(0, self.base if self.base else parent.get("base"))
            elif parent.tag == self._tag("resource"):
                path_l.insert(0, parent.get("path"))

            parent = parent.getparent()

        # Extract params of the url
        urls = self.param_url(unquote(self._normalize_url(path_l)))

        # In the end, return a array WADLRequest object representing the
        # given parsed request
        for url in urls:
            array_wadl.append(WADLRequest(url, method=method.get("name"), params=params, default_values=self.default_values))
        return array_wadl

    def param_url(self, path):
        """
        That Us will help to extract the params of the url, the param must have
        this format { var: regex } or {vardefault}.
        This def will deliver as many urls exist with the combinations of
        the parameters in the url
        Parameters
        ----------
            path : String (url)
        Return
        ______
            array: String (Array urls)
        """
        try:
            origin = furl(path).origin
            segments = path.replace(origin, "").split("/")
            urls = []
            auxurls = []

            # verify format parameter url { var: regex }
            regex = r"^[{]\s*\w*\s*[:]\s*.*\s*[}]$"
            for se in segments:
                if re.search(regex, se):
                    param = se.split(":")[1].replace("}", "")
                    if "|" in param:
                        array = exrex.generate(param)
                        if urls:
                            for a in array:
                                if not isinstance(urls, list):
                                    urls = [urls]
                                for u in urls:
                                    auxurls.append(u + "/" + a.strip())
                            urls = auxurls
                        else:
                            for a in array:
                                urls.append(origin + "/" + a)
                    else:
                        er = exrex.getone(param).lstrip()
                        if not isinstance(urls, list):
                            urls = [urls]
                        urls = [u + "/" + er for u in urls] if urls else origin + "/" + er
                else:
                    if se:
                        if urls and isinstance(urls, list):
                            urls = [u + "/" + se for u in urls]
                        else:
                            urls = (str(urls) if urls else origin) + "/" + se
        except Exception as e:
            raise ValueError("Error extracting parameter from url {}".format(e))

        return urls if isinstance(urls, list) else [urls]


class WADLRequest:
    """
    Class representing a request represented in a WADL string
    This class doesn't match exactly the <request> element that's part of the
    WADL standard. Instead it represents
    what must be each request generated after interpreting a given WADL file,
    which depends on the chain of resources/resource
    elements, method element, request element if any and the associated param
    elements.
    Args:
        location (str): Complete url for the given request.
        method (str): HTTP verb corresponding to this request.
        params (list of lxml.etree._Element objects): List of <param> elements
            that are used in this request.
        default_values (dict): Dictionary holding default values to be used in
            place of params found in the WADL file.
    """

    def __init__(self, location, method, params=None, headers={}, default_values={}):
        if params is None:
            params = []

        self.location = location
        self.method = method
        self.default_values = default_values
        self.params = [WADLParam(param, default_values=default_values) for param in params] if params else []
        self.headers = headers

    def dump_as_har(self):
        raise NotImplementedError("HAR output is not yet implemented")

    def dump_as_dict(self):
        """Dumps current request as a simple dict composed of keys
        location (the url), method and params"""
        return dict(location=self.location, method=self.method, params=[p.dump_as_dict() for p in self.params])

    def dump_as_request(self):
        """
        Dumps current request as a Request object for easier handling
        """
        headers = self.headers if self.headers else {}
        params = {}  # querystring params (style="query")

        for p in self.params:
            if p.style == "header":
                headers.update({p.name: p.value})
            elif p.style == "query":
                params.update({p.name: p.value})

        query_list = []
        for key, val_list in params.items():
            if isinstance(val_list, str):
                query_list.append("{}={}".format(key, val_list))
            elif val_list is None:
                query_list.append("{}=".format(key))
            else:
                for val in val_list:
                    if val is not None:
                        query_list.append("{}={}".format(key, val))
                    else:
                        query_list.append("{}=".format(key))
        query_str = "&".join(query_list)

        p = urlparse(self.location)
        url = urlunparse((p.scheme, p.netloc, p.path, p.params, query_str, ""))
        return Request(url=url, method=self.method, headers=headers)


class WADLParam:
    """
    Class representing WADL param elements. They might be query string
    variables, template parameters and HTTP headers.
    Examples:
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:double"
        style="query" name="userLon"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:int"
        style="query" name="local_count"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string"
        style="query" name=".intl"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="withStats"
        style="query" type="xs:boolean" default="true"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="woeid"
        style="query" type="xs:long"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="latitude"
        style="query" type="xs:float"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="If-None-Match"
        style="header" type="xs:string"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="cookie"
        style="header" type="xs:string"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="entityenc"
        style="header" type="xs:string"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" name="guid"
        style="header" type="xs:string"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
        name="javax.ws.rs.container.Suspended" type="xs:string"/>
    <param xmlns:xs="http://www.w3.org/2001/XMLSchema"
        name="y-ra" style="header" type="xs:string"/>
    Args:
        param_el (lxml.etree._Element): <param> element to handle.
        default_values (dict): Dictionary holding default values to be used in
        place of params found in the WADL file.
    Attributes:
        name (str): name attribute of the passed <param> element.
        type (str): type attribute of the passed <param> element.
        style (str): style attribute of the passed <param> element.
        value (str): value given to this <param> element. Will be set to
            (in this order of predecende)
                     value of the corresponding default_values key or
                     value of the "default" attribute of the <param> element
    """

    def __init__(self, param_el, default_values={}):
        if not param_el.get("name") or not param_el.get("style"):
            if param_el.get("name", "") != "javax.ws.rs.container.Suspended":
                raise ValueError("Attributes name and style are required")

        self.name = param_el.get("name")
        self.type = param_el.get("type")
        self.style = param_el.get("style") or "string"
        self.value = default_values.get(self.name) or param_el.get("default")  # default_values takes precedence over default param

    def dump_as_dict(self):
        """Dump param as a simple dict composed of keys name, type, style and
        value"""
        return dict(name=self.name, type=self.type, style=self.style, value=self.value)

    def __eq__(self, other):
        """Two WADLparam objects are considered equal if both their "name" and
        "style" attributes are equal"""
        return self.name == other.name and self.style == other.style

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        """WADLparams are ordered alphabetically according to their "name"
        attribute"""
        return self.name < other.name
