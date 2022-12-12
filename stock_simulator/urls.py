from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.index, name='index'),
    path('buy', views.buy, name='buy'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout')
]