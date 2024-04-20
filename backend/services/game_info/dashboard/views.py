from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def home(request):
    return JsonResponse({'message': 'Retornando dinamico!'})
    #return render(request, 'index.html')