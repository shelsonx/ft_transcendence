from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.defaults import page_not_found

def index(request: HttpRequest):
    return render(request, 'index.html')

def error_404(request: HttpRequest, exception):
    return page_not_found(request, exception=exception , template_name='404.html')

def profile(request: HttpRequest):
    return render(request, 'profile.html')
