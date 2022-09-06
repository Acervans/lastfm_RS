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


class VADAnalysisForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 40, 'style': 'resize: both;'}))
    mode = forms.ChoiceField(label='VAD Compute Mode', choices=[(
        'mean', 'Mean'), ('median', 'Median')], widget=forms.RadioSelect, initial='mean')
    method = forms.ChoiceField(label='Analysis Method', choices=[(
        'text', 'Whole Text'), ('sentences', 'By Sentences')], widget=forms.RadioSelect, initial='text')
