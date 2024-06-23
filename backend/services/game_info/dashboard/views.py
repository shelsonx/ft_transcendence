from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.db.models import UUIDField
from django.http import HttpResponse, HttpRequest
from django.db import IntegrityError
from django.core.serializers import serialize
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import uuid

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

@require_POST
@csrf_exempt
def register_user(request: HttpRequest) -> HttpResponse:
    try:
        payload = json.loads(request.body)
        print(payload)
        id_msc = payload.get('id_msc')
        full_name = payload.get('full_name')
        nickname = payload.get('nickname')

        user = UserInfo.objects.create(id_msc=id_msc, full_name=full_name, nickname=nickname)
        return HttpResponse("OK", status=200)
    except IntegrityError:
        return HttpResponse("Error: Failed to register user", status=400)

@require_POST
@csrf_exempt
def set_status_user(request: HttpRequest) -> HttpResponse:
    try:
        payload = json.loads(request.body)
        id_msc = payload.get('id_msc')
        status = payload.get('status')
        user = get_object_or_404(UserInfo, id_msc=id_msc)
        print(f'user: {user}')
        user.status = status
        user.save()
        return HttpResponse("OK", status=200)
    except Http404:
        return HttpResponse("Error: Failed to set status", status=400)

@require_POST
@csrf_exempt
def set_playing_user(request: HttpRequest) -> HttpResponse:
    try:
        payload = json.loads(request.body)
        id_msc = payload.get('id_msc')
        playing = payload.get('playing')
        user = get_object_or_404(UserInfo, id_msc=id_msc)
        user.playing = playing
        user.save()
        return HttpResponse("OK", status=200)
    except Http404:
        return HttpResponse("Error: Failed to set playing", status=400)

@require_POST
@csrf_exempt
def update_scores_user(request: HttpRequest) -> HttpResponse:
    try:
        payload = json.loads(request.body)
        id_msc = payload.get('id_msc')
        score = payload.get('score')
        winnings = payload.get('winnings')
        losses = payload.get('losses')
        user = get_object_or_404(UserInfo, id_msc=id_msc)
        if score:
            user.scores = score
        if winnings:
            user.winnings = winnings
        if losses:
            user.losses = losses
        user.save()
        return HttpResponse("OK", status=200)
    except Http404:
        return HttpResponse("Error: Failed to update scores", status=400)

@csrf_exempt
def update_user(request: HttpRequest) -> HttpResponse:
    try:
        payload = json.loads(request.body)
        id_msc = payload.get('id_msc')
        user = get_object_or_404(UserInfo, id_msc=id_msc)
        user.nickname = payload.get('nickname')
        user.full_name = user.nickname
        user.photo = payload.get('avatar')
        user.save()
        return HttpResponse("OK", status=200)
    except Http404:
        return HttpResponse("Error: Failed to update user", status=400)

@csrf_exempt
def delete_user(request: HttpRequest) -> HttpResponse:
    try:
        payload = json.loads(request.body)
        id_msc = payload.get('id_msc')
        user = get_object_or_404(UserInfo, id_msc=id_msc)
        user.delete()
        return HttpResponse("OK", status=200)
    except Http404:
        return HttpResponse("Error: Failed to delete user", status=400)
