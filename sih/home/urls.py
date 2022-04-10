from django.urls import path
from home.views import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transcribe', views.transcribe, name='transcribe'),
    path('register/', views.registerPage,name="register"),
    path('login/', views.loginPage,name="login"),
    path('logout/', views.loginPage,name="logout"),

]