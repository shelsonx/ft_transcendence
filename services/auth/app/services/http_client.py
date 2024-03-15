
import http.client
from urllib.parse import urlparse, urlencode
import json
from ..interfaces.services.http_client import IHttpClient

class HttpClient(IHttpClient):
    
    def get(self, url: str, headers: dict) -> http.client.HTTPResponse:
        domain = self._get_domain(url)
        conn = http.client.HTTPSConnection(domain)
        path = self._get_path(url)
        conn.request("GET", f"/{path}", headers=headers)
        return conn.getresponse()

    def post(self, url: str, data: dict, headers: dict) -> http.client.HTTPResponse:
        domain = self._get_domain(url)
        path = self._get_path(url)
        conn = http.client.HTTPSConnection(domain)
        conn.request("POST", f"/{path}", urlencode(data), headers)
        return conn.getresponse()

    def serialize(self, response: http.client.HTTPResponse) -> str:
        data = response.read().decode()
        return json.loads(data)
    
    def _extract_url(self, url: str) -> str:
        url_parse = urlparse(url)
        return url_parse
    
    def _get_domain(self, url: str) -> str:
        url_parse = self._extract_url(url)
        return url_parse.netloc
    
    def _get_path(self, url: str) -> str:
        url_parse = self._extract_url(url)
        return url_parse.path
  