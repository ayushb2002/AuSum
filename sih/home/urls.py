from django.urls import path
from home.views import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transcribe', views.transcribe, name='transcribe'),
    path('summarize', views.summarize, name='summarize'),
    path('loadSummary', views.loadSummary, name='loadSummary'),
    path('notes', views.notes, name="notes"),
    path('loadNotes', views.loadNotes, name="loadNotes")
]