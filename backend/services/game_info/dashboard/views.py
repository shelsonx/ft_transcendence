from django.shortcuts import render
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