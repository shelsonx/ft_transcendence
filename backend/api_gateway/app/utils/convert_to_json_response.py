
from django.http import JsonResponse
import json
from http.client import HTTPResponse

def convert_to_json_response(http_response: HTTPResponse):
    response_str = http_response.read().decode()
    
    if response_str:
        response_data = json.loads(response_str)
    else:
        response_data = {}

    if 300 <= http_response.status < 400:
        location = http_response.getheader('Location')
        if location is not None:
            response_data['redirect'] = location

    json_response = JsonResponse(status=http_response.status, data=response_data, safe=False)
    return json_response