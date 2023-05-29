from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PreviewTrackForm(forms.Form):
    artist = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)
    lyrics = forms.BooleanField(required=False, label='Lyrics from Genius')


class VADAnalysisForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 40, 'style': 'resize: both;'}))
    mode = forms.ChoiceField(label='VAD Compute Mode', choices=[(
        'mean', 'Mean'), ('median', 'Median')], widget=forms.RadioSelect, initial='mean')
    method = forms.ChoiceField(label='Analysis Method', choices=[(
        'text', 'Whole Text'), ('sentences', 'By Sentences')], widget=forms.RadioSelect, initial='text')
    lang_check = forms.BooleanField(required=False, label='Check Language')

class RecommendationsForm(forms.Form):
    model = forms.ChoiceField(label='Model Selection', choices=[
        ('random', 'Random'),
        ('pop', 'Pop (item popularity)'),
        ('itemknn', 'ItemKNN'),
        ('cosine', 'Cosine Similarities (Tag-based)'),
        ('dcnv2', 'DCN V2'),
        ('dcnv2vad', 'DCN V2 (With VADSt)'),
        ('xdeepfm', 'xDeepFM'),
        ('xdeepfmvad', 'xDeepFM (With VADSt)')
    ], widget=forms.RadioSelect, initial='random')
    username = forms.CharField(label='Username', max_length=100, required=False)
    username.widget.attrs['list'] = 'usernames'
    scrape = forms.BooleanField(label='Scrape Last.FM Data', required=False, help_text="Only Random Recommender & Cosine Similarities")
    cutoff = forms.IntegerField(label='Cutoff', min_value=1, initial=10)

class RandomRecommenderForm(forms.Form):
    seed = forms.IntegerField(label="Random Seed", required=False)

class CosineRecommenderForm(forms.Form):
    tags = forms.CharField(label='Tags', required=False)
    binary = forms.BooleanField(label='Binary Frequencies', required=False)
    weighted = forms.BooleanField(label='Weighted Average', required=False)
    topk = forms.IntegerField(label='Top-K Average', required=False)

