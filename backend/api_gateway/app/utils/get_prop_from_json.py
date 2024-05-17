from django.http import JsonResponse
import json

def get_prop_from_json(json_response: JsonResponse):
   content = json_response.content.decode('utf-8')
   data = json.loads(content)
   return data['data']
