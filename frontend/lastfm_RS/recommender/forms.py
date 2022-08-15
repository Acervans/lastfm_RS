from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class PreviewTrackForm(forms.Form):
    artist = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)