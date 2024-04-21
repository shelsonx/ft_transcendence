from abc import ABC, abstractmethod
from http import client

class HttpClientData:
    def __init__(self, url: str, data: dict, headers: dict) -> None:
        self.url = url
        self.data = data
        self.headers = headers

class IHttpClient:

    @abstractmethod
    def get(self, url: str, headers: dict) -> client.HTTPResponse:
        pass

    @abstractmethod
    def post(self, url: str, data: dict, headers: dict) -> client.HTTPResponse:
        pass

    @abstractmethod
    def put(self, url: str, data: dict, headers: dict) -> client.HTTPResponse:
        pass

    @abstractmethod
    def delete(self, url: str, headers: dict) -> client.HTTPResponse:
        pass

    def serialize(self, data: dict) -> str:
        pass
