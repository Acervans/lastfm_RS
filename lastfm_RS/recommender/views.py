from django.shortcuts import render
from django.contrib.auth import authenticate
from .forms import PreviewTrackForm, RegisterForm, VADAnalysisForm
from bs4 import BeautifulSoup
from backend.src.nrc_vad_analysis import FIELDNAMES, analyze_string, analyze_text
import requests
import pylast
import lyricsgenius

# Create your views here.

genius = lyricsgenius.Genius(
    'wub8JMLwasqRZWGFM-JwSDrfT1YCFLah7T1tDvC6km3BhadU1D4vT1IsOfHNuOIq', verbose=False)
network = pylast.LastFMNetwork(
    '23ff8e4c454cbb8ae4a13440bc0fa745', 'a5efd0d4bbeed8c37b0c4bd7672edf58')


def index(request):
    """View function for home page of site."""

    """ EJEMPLOS DE locallibrary
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available copies of books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    """

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_visits': num_visits},
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

# Mejor idea sería que se recomiende una playlist, y al lado un botón de Preview solo cuando tenga link de youtube (o como pagina aparte)


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
    track = pylast.Track(artist, title, network)

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
        soup = BeautifulSoup(requests.get(
            track_url).content, "html.parser")
        artist_url = 'https://www.last.fm' + \
            soup.find('a', {'class': 'header-new-crumb'}).get('href')
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
            gsong = genius.search_song(title, artist, get_full_info=False)
            if gsong:
                lyrics = gsong.lyrics[gsong.lyrics.find('['):-5]

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

            if method == 'text':
                fun = analyze_string
                fieldnames = FIELDNAMES[1:]
                fieldnames[0] = 'Text'
            else:
                fun = analyze_text
                fieldnames = FIELDNAMES

            return render(
                request,
                'vad_analysis.html',
                {'fieldnames': fieldnames,
                 'results': fun(text, mode, True),
                 'method': method},
            )
    else:
        form = VADAnalysisForm()

    return render(request, 'vad_analysis_form.html', context={'form': form})
