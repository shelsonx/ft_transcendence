from typing import Any, Union
import requests
from urllib.parse import urljoin
import json
from ..interfaces.services.http_client import IHttpClient, HttpClientData

class HttpClientRequest(IHttpClient):

    def __init__(self, base_url) -> None:
        super().__init__()
        self.base_url = base_url

    def get(self, request_data: HttpClientData) -> requests.Response:
        return self._make_request("GET", request_data)

    def post(self, request_data: HttpClientData) -> requests.Response:
        return self._make_request("POST", request_data)

    def put(self, request_data: HttpClientData) -> requests.Response:
        return self._make_request("PUT", request_data)

    def delete(self, request_data: HttpClientData) -> requests.Response:
        return self._make_request("DELETE", request_data)

    def _make_request(self, method: str, request_data: HttpClientData
    ) -> requests.Response:
        url_with_base = urljoin(self.base_url.container, request_data.url.lstrip('/'))
        response = requests.request(method, url_with_base, data=request_data.data, headers=request_data.headers, verify=False)
        return response

    def deserialize(self, response: requests.Response)-> Union[Any, int]:
        try:
            json_resp, status = response.json(), response.status_code
        except json.JSONDecodeError:
            json_resp, status = response.text, response.status_code
        return json_resp, status

    def serialize(self, data: requests.Response) -> str:
        return json.dumps(data).encode('utf-8')
