from django.http import JsonResponse
import json

def get_prop_from_json(json_response: JsonResponse, prop="data"):
   content = json_response.content.decode('utf-8')
   data = json.loads(content)
   return data[prop]


def get_data_from_json_response(json_response: JsonResponse):
   content = json_response.content.decode('utf-8')
   data = json.loads(content)
   return data
