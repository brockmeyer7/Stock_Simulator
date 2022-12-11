from django.shortcuts import render
from django.http import HttpResponse as response, HttpRequest
from django.contrib.auth import authenticate, login

def index(request):
    user = ""
    return render(request, 'register.html', {'user': user})