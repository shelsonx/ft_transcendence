from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

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

from django.core.serializers import serialize
import json
def get_user(request, id):
    user = get_object_or_404(UserInfo, id=id)
    serialized_data = serialize('json', [user])
    user_dict = json.loads(serialized_data)[0]['fields']
    return JsonResponse({'user': user_dict}, safe=False)