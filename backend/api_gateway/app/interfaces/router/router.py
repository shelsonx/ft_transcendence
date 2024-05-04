
from ..services.http_client import IHttpClient
from abc import ABC, abstractmethod
from typing import List
from copy import deepcopy
import uuid
from django.http import Http404, HttpRequest
from ...interfaces.services.http_client import IHttpClient, HttpClientData
from ...utils.convert_to_json_response import convert_to_json_response
from django.http import HttpResponseRedirect
from urllib.parse import urlparse, parse_qs

class Route:

  def __init__(self, route_key, allowed_verbs, is_redirect = False) -> None:
    self.route_key = route_key
    self.allowed_verbs = allowed_verbs
    self.split = route_key.split('/')
    self.len = len(self.split)
    self.is_redirect = is_redirect

    self.path_converters = {
      "<str:": lambda x: str(x),
      "<int:": lambda x: int(x),
      "<uuid:": lambda x: uuid.UUID(str(x))
    }

  def path_converter(self, real_path: str, path: str):
    for path_convert in self.path_converters.keys():
      if path.startswith(path_convert):
        try:
          self.path_converters[path_convert](real_path)
          return True
        except ValueError:
          return False
    return False

  def return_route_if_match(self, path: str):
    if path == self.route_key:
      return deepcopy(self)
    path_split = path.split('/')
    if len(path_split) != self.len:
      return None
    counter = 0
    for i, each_path in enumerate(path_split):
      if each_path == self.split[i] or self.path_converter(each_path, self.split[i]):
        counter += 1
      else:
        continue
    if self.len == counter:
      return deepcopy(self)
    return None

  def __str__(self) -> str:
    return f"Route: {self.route_key} - {self.allowed_verbs}"

class IRouter(ABC):

  def __init__(self, http_client: IHttpClient, routes: List[Route]) -> None:
    self.http_client = http_client
    self.routes = { route.route_key: route for route in routes }


  def path_resolver(self, path: str):
    for route in self.routes.values():
      found_route = route.return_route_if_match(path)
      if found_route:
        return found_route
    return None

  def append_language_to_path_from_query_string(self, path):
    url_string = self.http_client.base_url.localhost + path
    parsed_url = urlparse(url_string)
    query_string = parsed_url.query
    query_params = parse_qs(query_string)
    language = query_params.get('language')
    if language:
        path = path.split("?")[0]
        query_params.pop('language')
        query_string = "&".join([f"{key}={value[0]}" for key, value in query_params.items()])
        path = f"{path}" + (f"?{query_string}" if query_string else "")
        self.http_client.base_url.rebuild_url(self.http_client.base_url.path, language[0])
        return path
    self.http_client.base_url.rebuild_url(self.http_client.base_url.path)
    return path

  def route(self, verb: str, path: str, request: HttpRequest, *args, **kwargs):
    if not isinstance(verb, str):
      raise ValueError("verb must be a string")
    path_without_query_str = path.split("?")[0]
    route = self.routes.get(path_without_query_str)
    if route is None:
      route = self.path_resolver(path_without_query_str)
      if route is None:
        raise Http404()

    route.route_key = self.append_language_to_path_from_query_string(path)
    print(route.route_key)

    if verb.upper() not in route.allowed_verbs:
      raise ValueError(f"verb '{verb}' not allowed for path '{path}'")
    if route.is_redirect:
      return HttpResponseRedirect(redirect_to=self.http_client.base_url.localhost + path.lstrip('/'))
    method = getattr(self.http_client, verb.lower(), None)
    if method is None:
        raise ValueError(f"verb '{verb}' not supported by http_client")
    reponse = method(HttpClientData(url=route.route_key, data=request.body, headers=request.headers))
    return convert_to_json_response(reponse)
