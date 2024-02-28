from django.core.exceptions import ObjectDoesNotExist
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import User


@csrf_exempt
# This is just for the sake of the example. Must be resolved with a proper CSRF token.
def create_user(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
        data = json.loads(request.body.decode('utf-8'))
        form = UserForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'User created successfully'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@csrf_exempt
def get_all_users(request):
    try:
        users = User.objects.all()
        users_json = [user.as_json() for user in users]
        return JsonResponse({'status': 'success', 'users': users_json}, status=200, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse({'status': 'success', 'user': user.as_json()}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)


@csrf_exempt
def delete_user(request, user_id):
    try:
        if request.method != 'DELETE':
            return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'User deleted successfully'}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
    except Exception as e:
        print("Error: ", e, flush=True)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def update_user_status(request, user_id):
    try:
        if request.method != 'PATCH':
            return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
        user = User.objects.get(pk=user_id)
        data = json.loads(request.body.decode('utf-8'))
        user.status = data['status']
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User updated successfully'}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def update_user_avatar(request, user_id):
    try:
        if request.method != 'PATCH':
            return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
        user = User.objects.get(pk=user_id)
        data = json.loads(request.body.decode('utf-8'))
        user.avatar = data['avatar']
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User updated successfully'}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def update_user_nickname(request, user_id):
    try:
        if request.method != 'PATCH':
            return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
        user = User.objects.get(pk=user_id)
        data = json.loads(request.body.decode('utf-8'))
        user.nickname = data['nickname']
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User updated successfully'}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def update_user_two_factor_enabled(request, user_id):
    try:
        if request.method != 'PATCH':
            return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
        user = User.objects.get(pk=user_id)
        data = json.loads(request.body.decode('utf-8'))
        user.two_factor_enabled = data['two_factor_enabled']
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User updated successfully'}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def update_user_email(request, user_id):
    try:
        if request.method != 'PATCH':
            return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
        user = User.objects.get(pk=user_id)
        data = json.loads(request.body.decode('utf-8'))
        user.email = data['email']
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User updated successfully'}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def index(request):
    return JsonResponse({'status': 'success', 'message': 'Welcome to the Users Django API!'}, status=200)

