from django.forms import ModelForm
from .models import Room,Message
from django.contrib.auth.models import User
from django import forms


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic','name','description']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class MessageForm(ModelForm):
    class Meta:
        model= Message
        fields=['body']