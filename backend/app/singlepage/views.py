from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, Http404

def index(request):
    return render(request, "singlepage/index.html")


projects = ['Inception', 'Webserv', 'Transcendence']

def section(request, section_id):
    if 1 <= section_id <= 3:
        return HttpResponse(projects[section_id - 1])
    else:
        raise Http404("Section does not exist")