from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
TYPES = [
    ('Letter', 'Letter'),
    ('Numbers', 'Numbers'),
    ('Both' , 'Both')
    
]

LETTERS = [
    ('Uppercase', 'Uppercase'),
    ('LowerCase', 'LowerCase'),
    ('Both', 'Both')

]
class Choices(forms.Form):
    
    key_type = forms.CharField(widget=forms.RadioSelect(choices=TYPES))
    chara_type = forms.CharField(widget=forms.RadioSelect(choices=LETTERS))
