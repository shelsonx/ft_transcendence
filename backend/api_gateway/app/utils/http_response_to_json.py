from http.client import HTTPResponse
from .convert_to_json_response import convert_to_json_response
from .get_prop_from_json import get_prop_from_json

def http_response_to_json(http_response: HTTPResponse):
  json_response = convert_to_json_response(http_response)
  json_data = get_prop_from_json(json_response)
  return json_data
