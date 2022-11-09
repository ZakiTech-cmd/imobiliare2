from django.forms import ModelForm
from .models import Announce
from .models import PostImage
from django import forms
from django.db import models
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AnnounceForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)

    class Meta:
        model = Announce
        exclude = ['creator']


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

