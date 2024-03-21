from django.http import JsonResponse
from ..entities.api_data_response import ApiDataResponse

def to_json_response(data: ApiDataResponse, status=200) -> JsonResponse:
    return JsonResponse(status=status, data=data.to_dict(), safe=False)