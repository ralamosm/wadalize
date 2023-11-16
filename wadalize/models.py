from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional
from urllib.parse import parse_qs
from urllib.parse import urlparse

from pydantic import BaseModel
from pydantic import field_validator
from pydantic import HttpUrl
from pydantic import model_validator


class Request(BaseModel):
    """Model representing a simple HTTP request"""

    url: HttpUrl
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "COPY"]
    headers: Optional[Dict] = {}
    _params: Optional[Dict] = {}
    _query: Optional[Dict] = {}

    @property
    def params(self) -> Dict:
        return self._params

    @params.setter
    def params(self, value: Dict) -> None:
        self._params = value
        return self

    @property
    def query(self) -> Dict:
        return self._query

    @query.setter
    def query(self, value: Dict) -> None:
        self._query = value
        return self

    @field_validator("method", mode="before")
    @classmethod
    def method_upper(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Method must be a string")
        return v.upper()

    @model_validator(mode="after")
    def check_query_params(self) -> Any:
        p = urlparse(str(self.url))
        self.params = dict(param.split("=") for param in p.params.split(";") if param)
        self.query = parse_qs(p.query, keep_blank_values=True) if p.query else {}
        return self
