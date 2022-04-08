from django.urls import path
from home.views import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]