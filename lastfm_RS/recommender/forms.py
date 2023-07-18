from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template import loader
from django.utils.safestring import mark_safe
from django import forms
from backend.src.constants import TRACK_LIMIT, ARTIST_LIMIT, ALBUM_LIMIT, TAG_LIMIT

MAX_LENGTH = 1000


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PreviewTrackForm(forms.Form):
    artist = forms.CharField(max_length=MAX_LENGTH)
    title = forms.CharField(max_length=MAX_LENGTH)
    lyrics = forms.BooleanField(required=False, label='Lyrics by Genius')


class VADAnalysisForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 40, 'style': 'resize: both;'}))
    mode = forms.ChoiceField(label='VAD Compute Mode', choices=[(
        'mean', 'Mean'), ('median', 'Median')], widget=forms.RadioSelect, initial='mean')
    method = forms.ChoiceField(label='Analysis Method', choices=[(
        'text', 'Whole Text'), ('sentences', 'By Sentences')], widget=forms.RadioSelect, initial='text')
    lang_check = forms.BooleanField(required=False, label='Check Language')


class TagsInput(forms.Widget):
    template_name = 'widgets/tags-input.html'

    def get_context(self, name: str, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class RecommendationsForm(forms.Form):
    model = forms.ChoiceField(label='Model Selection', choices=[
        ('random', 'Random'),
        ('pop', 'Pop'),
        ('cosine', 'Cosine Similarities'),
        ('itemknn', 'ItemKNN'),
        ('dcnv2', 'DCN V2'),
        ('pnn', 'PNN'),
        ('xdeepfm', 'xDeepFM'),
        ('search', 'Search'),
    ], widget=forms.RadioSelect, initial='random')
    username = forms.CharField(
        label='Username', max_length=MAX_LENGTH, required=False)
    username.widget.attrs['list'] = 'usernames'
    username.widget.attrs['placeholder'] = 'Random User'
    cutoff = forms.IntegerField(label='Cutoff', min_value=1, initial=10)
    limit = forms.IntegerField(
        label='Per Page', min_value=1, required=False, initial=10)


class RandomRecommenderForm(forms.Form):
    seed = forms.IntegerField(label="Random Seed", required=False, min_value=0)


class CosineRecommenderForm(forms.Form):
    tags = forms.CharField(label='Tags', widget=TagsInput(), required=False)
    binary = forms.BooleanField(
        label='Binary Frequencies', required=False, initial=True)
    weighted = forms.BooleanField(
        label='Weighted Average', required=False, initial=False)
    topk = forms.IntegerField(label='Top-K Averaging',
                              required=False, min_value=1)


def create_input(placeholder, hidden=True):
    input_type = forms.HiddenInput if hidden else forms.TextInput
    return forms.CharField(
        label='Query', required=False, strip=False, widget=input_type(attrs={
            'placeholder': placeholder,
            'class': 'form-control',
            'maxlength': MAX_LENGTH
        }))


class SearchForm(forms.Form):
    by = forms.ChoiceField(label='Search by', choices=[
        ('track', 'Track'),
        ('artist', 'Artist'),
        ('album', 'Album'),
    ], widget=forms.RadioSelect, initial='track')
    query_track = create_input('Track name', False)
    query_artist = create_input('Artist name')
    query_album = create_input('Album name')


class UserScraperForm(forms.Form):
    username = forms.CharField(
        label='Last.FM Username', max_length=MAX_LENGTH, required=True)
    use_database = forms.BooleanField(
        label='Use Database', required=False, initial=False)

    include_tracks = forms.BooleanField(
        label='Include Tracks', required=False, initial=True)
    include_artists = forms.BooleanField(
        label='Include Artists', required=False, initial=True)
    include_albums = forms.BooleanField(
        label='Include Albums', required=False, initial=True)
    include_tags = forms.BooleanField(
        label='Include Tags', required=False, initial=True)

    tracks_limit = forms.IntegerField(
        label='Tracks limit', required=False, initial=TRACK_LIMIT, min_value=1)
    artists_limit = forms.IntegerField(
        label='Artists limit', required=False, initial=ARTIST_LIMIT, min_value=1)
    albums_limit = forms.IntegerField(
        label='Albums limit', required=False, initial=ALBUM_LIMIT, min_value=1)
    tags_limit = forms.IntegerField(
        label='Tags limit', required=False, initial=TAG_LIMIT, min_value=1)

    anonymous = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput())

    item_fields = [(f'{i}_limit', f'include_{i}')
                   for i in ('tracks', 'artists', 'albums', 'tags')]
