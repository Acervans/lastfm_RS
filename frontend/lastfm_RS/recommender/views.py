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

    """
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

    yt_id = mbid = None
    found = False
    try:
        mbid = track.get_mbid()
    except pylast.WSError:
        track = None

    if track:
        found = True
        title = track.get_correction()
        artist = track.get_artist().get_correction()
        soup = BeautifulSoup(requests.get(
            track.get_url()).content, "html.parser")
        yt_tag = soup.find('a', {'id': 'track-page-video-playlink'})
        if yt_tag:
            yt_id = yt_tag.get('data-youtube-id')

    context = {
        'found': found,
        'title': title,
        'id': mbid,
        'artist': artist,
        'yt_id': yt_id,
    }
    return context