from django.shortcuts import render
from django.contrib.auth import authenticate
from .forms import PreviewTrackForm, RegisterForm
from bs4 import BeautifulSoup
import requests
import pylast
# Create your views here.

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
        # context={'num_books': num_books, 'num_instances': num_instances,
        #          'num_instances_available': num_instances_available, 'num_authors': num_authors,
        #          'num_visits': num_visits},
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

            return render(
                request,
                'lastfm_preview.html',
                get_track_context(artist, title),
            )
    else:
        form = PreviewTrackForm()
        return render(request, 'lastfm_preview_form.html', context={'form': form})


def get_track_context(artist, title):
    track = pylast.Track(artist, title, network)

    yt_id = sp_id = mbid = track_url = artist_url = None
    found = False
    try:
        mbid = track.get_mbid()
    except pylast.WSError:
        track = None

    if track:
        found = True
        title = track.get_correction()
        track_url = track.get_url()
        artist = track.get_artist()
        artist_url = artist.get_url()
        soup = BeautifulSoup(requests.get(
            track_url).content, "html.parser")
        plinks = soup.find('ul', {'class': 'play-this-track-playlinks'})

        if plinks:
            yt_tag = plinks.find(
                'a', {'class': 'play-this-track-playlink--youtube'})
            if yt_tag:
                yt_id = yt_tag.get('data-youtube-id')

            sp_tag = plinks.find(
                'a', {'class': 'play-this-track-playlink--spotify'})
            if sp_tag:
                sp_id = sp_tag.get('href').rsplit('track/')[1]

    context = {
        'found': found,
        'title': title,
        'track_url': track_url,
        'artist': artist.get_correction(),
        'artist_url': artist_url,
        'id': mbid,
        'yt_id': yt_id,
        'sp_id': sp_id,
    }
    return context
