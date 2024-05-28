import http.client
from urllib.parse import urlparse, urlencode
import json
from ..interfaces.services.http_client import IHttpClient, HttpClientData
from urllib.parse import urljoin
from typing import Any, Union

class HttpClient(IHttpClient):

    def __init__(self, base_url) -> None:
        super().__init__()
        self.base_url = base_url

    def get(self, request_data: HttpClientData) -> http.client.HTTPResponse:
        return self._make_request("GET", request_data)

    def post(self, request_data: HttpClientData) -> http.client.HTTPResponse:
        return self._make_request("POST", request_data)

    def put(self, request_data: HttpClientData) -> http.client.HTTPResponse:
        return self._make_request("PUT", request_data)

    def delete(self, request_data: HttpClientData) -> http.client.HTTPResponse:
        return self._make_request("DELETE", request_data)

    def _make_request(self, method: str, request_data: HttpClientData
    ) -> http.client.HTTPResponse:
        url_with_base = urljoin(self.base_url.container, request_data.url.lstrip('/'))
        print("url_with_base", url_with_base)
        domain = self._get_domain(url_with_base)
        path = self._get_path(url_with_base)
        if url_with_base.startswith("https"):
            conn = http.client.HTTPSConnection(domain)
        else:
            conn = http.client.HTTPConnection(domain)
        conn.request(method, path, request_data.data, request_data.headers)
        return conn.getresponse()

    def deserialize(self, response: http.client.HTTPResponse) -> Union[Any, int]:
        data = response.read().decode()
        return json.loads(data), response.status

    def serialize(self, data: Any) -> str:
        return json.dumps(data).encode('utf-8')

    def _extract_url(self, url: str) -> str:
        url_parse = urlparse(url)
        return url_parse

    def _get_domain(self, url: str) -> str:
        url_parse = self._extract_url(url)
        return url_parse.netloc

    def _get_path(self, url: str) -> str:
        url_parse = self._extract_url(url)
        return url_parse.path
