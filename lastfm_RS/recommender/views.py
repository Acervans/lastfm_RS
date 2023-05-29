from django.shortcuts import render
from django.contrib.auth import authenticate
from .forms import *
from bs4 import BeautifulSoup
from backend.src.nrc_vad_analysis import FIELDNAMES, FIELDNAMES_LANG, analyze_string, analyze_text
from backend.src.constants import GENIUS, PYLAST
from backend.src.get_lastfm_data import get_user_data
from backend.research.db_utils import *
import requests
import pylast

RECSYS_DATA = '../backend/data/rescys_data'

# Create your views here.


def index(request):
    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    tables_count = get_tables_count()
    tables_count['useralltracks'] = tables_count['usertoptracks'] + \
        tables_count['userrecenttracks'] + tables_count['userlovedtracks']

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={
            'num_visits': num_visits,
            'stats': tables_count,
        },
    )


def register(request):
    """View function for registration form."""

    if request.method == 'POST':
        # Registration form instance
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                return render(request, 'registration/registration_complete.html')

    else:
        form = RegisterForm()
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'registration/registration_form.html',
        context={'form': form},
    )

def lastfm_preview(request):

    if request.method == 'GET' and 'artist' in request.GET:
        form = PreviewTrackForm(request.GET)
        if form.is_valid():
            artist = form.cleaned_data.get('artist')
            title = form.cleaned_data.get('title')
            do_lyrics = form.cleaned_data.get('lyrics')

            return render(
                request,
                'lastfm_preview.html',
                get_track_context(artist, title, do_lyrics),
            )
    else:
        form = PreviewTrackForm()
        return render(request, 'lastfm_preview_form.html', context={'form': form})


def get_track_context(artist, title, do_lyrics):
    """
    Gets the information from a track required for the lastFM Previewer.
    :param artist: string with artist of the track
    :param title: string with title of the track
    :param do_lyrics: determines whether the lyrics should be searched using the Genius API
    :return context: dict with context of the track
    """
    track = pylast.Track(artist, title, PYLAST)

    yt_id = sp_id = mbid = track_url = artist_url = lyrics = None
    found = False
    try:
        mbid = track.get_mbid()
    except pylast.WSError:
        track = None

    if track:
        found = True
        title = track.get_correction()
        track_url = track.get_url()
        artist = track.get_artist().get_correction()
        artist_url = 'https://www.last.fm/music/' + artist.replace(' ', '+')

        soup = BeautifulSoup(requests.get(
            track_url).content, "lxml")
        plinks = soup.find('ul', {'class': 'play-this-track-playlinks'})

        # get playlinks for youtube and spotify embeds
        if plinks:
            yt_tag = plinks.find(
                'a', {'class': 'play-this-track-playlink--youtube'})
            if yt_tag:
                yt_id = yt_tag.get('data-youtube-id')

            sp_tag = plinks.find(
                'a', {'class': 'play-this-track-playlink--spotify'})
            if sp_tag:
                sp_id = sp_tag.get('href').rsplit('track/')[1]

        # get lyrics from Genius API
        if do_lyrics:
            gsong = GENIUS.search_song(title, artist, get_full_info=False)
            if gsong:
                lyrics = gsong.lyrics

    context = {
        'found': found,
        'title': title,
        'track_url': track_url,
        'artist': artist,
        'artist_url': artist_url,
        'id': mbid,
        'yt_id': yt_id,
        'sp_id': sp_id,
        'do_lyrics': do_lyrics,
        'lyrics': lyrics,
    }
    return context


def vad_analysis(request):
    if request.method == 'POST':
        form = VADAnalysisForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            mode = form.cleaned_data.get('mode')
            method = form.cleaned_data.get('method')
            lang_check = form.cleaned_data.get('lang_check')

            if lang_check:
                fieldnames = FIELDNAMES_LANG
            else:
                fieldnames = FIELDNAMES

            if method == 'text':
                fun = analyze_string
                fieldnames = fieldnames[1:]
                fieldnames[0] = 'Text'
            else:
                fun = analyze_text

            return render(
                request,
                'vad_analysis.html',
                {'fieldnames': fieldnames,
                 'results': fun(text, mode, True, lang_check),
                 'method': method},
            )
    else:
        form = VADAnalysisForm()

    return render(request, 'vad_analysis_form.html', context={'form': form})


# Mejor idea sería que se recomiende una playlist, 
# y al lado un desplegable con todos los datos y link de youtube (o como pagina aparte)

def recommendations(request):

    if request.method == 'GET' and 'recommend-model' in request.GET:
        rec_form = RecommendationsForm(request.GET, prefix='recommend')
        if rec_form.is_valid():
            recsys = rec_form.cleaned_data.get('model')
            username = rec_form.cleaned_data.get('username')
            scrape = rec_form.cleaned_data.get('scrape')
            cutoff = rec_form.cleaned_data.get('cutoff')
            print(recsys)
            match recsys:
                case 'random':
                    recsys_form = RandomRecommenderForm(request.GET, prefix='random')
                case 'cosine':
                    recsys_form = CosineRecommenderForm(request.GET, prefix='cosine')
                    if recsys_form.is_valid():
                        tags = recsys_form.cleaned_data.get('tags')
            
            if scrape:
                user_data = get_processed_user_data(username)
                from pprint import pprint
                pprint(user_data)

            return render(request, 'lastfm_recommend.html', context={
                recommendations: [(1, 'track1context'),(2, 'track2context')], #placeholder, trackcontext would be dicts
            })
    else:
        rec_form = RecommendationsForm(prefix="recommend")
        random = RandomRecommenderForm(prefix="random")
        cosine = CosineRecommenderForm(prefix="cosine")

        usernames = get_table_df('user_')['username']
        return render(request, 'lastfm_recommend_form.html', context={
            'rec_form': rec_form,
            'random': random,
            'cosine': cosine,
            'usernames': usernames,
        })

def get_processed_user_data(username):
    user_data = get_user_data(username)
    # TODO preprocess, give ratings, concatenate to dataset, etc
    
    return user_data

def get_recommendations(username):
    pass