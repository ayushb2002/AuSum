from dataclasses import field
from pyexpat import model
from django.forms import Form, FileField, ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UploadForm(Form):
    file = FileField()
    

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']