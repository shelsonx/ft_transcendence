from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import UUIDField
from django.http import HttpResponse, HttpRequest
from django.db import IntegrityError
from django.core.serializers import serialize
import json

from .models import UserInfo

def home(request):
    users = UserInfo.objects.all()
    data = list(users.values())
    return JsonResponse(data, safe=False)

def total_infos(request):
    users = UserInfo.objects.all()
    total_scores = sum([user.scores for user in users])
    total_players = len(users)
    return JsonResponse(
        {'total_scores': total_scores,
        'total_players': total_players}, 
        safe=False)

def get_user(request, id):
    user = get_object_or_404(UserInfo, id=id)
    serialized_data = serialize('json', [user])
    user_dict = json.loads(serialized_data)[0]['fields']
    return JsonResponse({'user': user_dict}, safe=False)

def register_user(request: HttpRequest) -> HttpResponse:
    try:
        payload = json.loads(request.body)
        id_msc = payload.get('id_msc')
        full_name = payload.get('full_name')
        nickname = payload.get('nickname')

        user = UserInfo.objects.create(id_msc=id_msc, full_name=full_name, nickname=nickname)
        return HttpResponse("OK", status=200)
    except IntegrityError:
        return HttpResponse("Error: Failed to register user", status=400)
