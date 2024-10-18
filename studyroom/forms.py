from django.forms import ModelForm
from .models import Room,Message,User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUser(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic','name','description']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','first_name','last_name','username','email','bio']

class MessageForm(ModelForm):
    class Meta:
        model= Message
        fields=['body']