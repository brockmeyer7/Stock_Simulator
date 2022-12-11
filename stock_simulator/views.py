from django.shortcuts import render
from django.http import HttpResponse as response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from . helpers import apology
import django.forms as forms


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    confirmation = forms.CharField()


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data['confirmation']

            if not username:
                return apology("Input valid username")
            elif not password or not confirmation:
                return apology("Input password and confirmation")
            elif password != confirmation:
                return apology("Passwords do not match")
            
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return response()
    return render(request, 'register.html')