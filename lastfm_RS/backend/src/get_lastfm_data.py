from lyricsgenius import Genius
# from nrc_vad_analysis import analyze_string, analyze_text
from bs4 import BeautifulSoup
import pylast
import requests
import time
import json
import sys

genius = Genius(
    "wub8JMLwasqRZWGFM-JwSDrfT1YCFLah7T1tDvC6km3BhadU1D4vT1IsOfHNuOIq")
network = pylast.LastFMNetwork(
    "23ff8e4c454cbb8ae4a13440bc0fa745", "a5efd0d4bbeed8c37b0c4bd7672edf58"
)

payload = {"username_or_email": "Test_EPS", "password": "Tfg.EPS2022"}

DATA_FOLDER = '../data'
LOGIN_URL = "https://www.last.fm/login"

TRACK_LIMIT = 1
ARTIST_LIMIT = 1
ALBUM_LIMIT = 1
TAG_LIMIT = 1


def login_lastfm(session):
    # Retrieve the CSRF token first
    session.get(LOGIN_URL)  # sets cookie
    if "csrftoken" in session.cookies:
        # Django 1.6 and up
        csrftoken = session.cookies["csrftoken"]
    else:
        # older versions
        csrftoken = session.cookies["csrf"]

    # Include CSRF token in request payload
    payload["csrfmiddlewaretoken"] = csrftoken

    # Log into Last FM (necessary to view listeners)
    s.post(LOGIN_URL, data=payload, headers=dict(Referer=LOGIN_URL))


def get_top_listeners(session, artist):
    artist_url = "https://www.last.fm/music/" + \
        artist.replace(" ", "+") + "/+listeners"
    soup = BeautifulSoup(session.get(
        artist_url).content, "html.parser")
    top_listeners_div = soup.find("div", {"class": "buffer-standard"})

    top_listeners = []
    # Check top listeners
    if not top_listeners_div.find("p", {"class": "no-data-message"}):
        # Get top listeners
        top_listeners_list = top_listeners_div.find_all(
            "a", {"class": "link-block-target"})
        top_listeners = [listener.get_text()
                         for listener in top_listeners_list]

    return top_listeners


def get_chart_top_tags(limit):
    return [tag[0] for tag in network.get_top_tags(limit=limit)]


def get_tag_top_artists(tags):
    tag_top_artists = set()
    for tag in tags:
        tag_top_artists.update(
            [artist[0].get_name() for artist in tag.get_top_artists()]
        )
    return tag_top_artists


def get_track_info(track: pylast.Track):
    artist = track.get_artist().get_name()
    album = track.get_album()
    if album:
        album = album.get_name()
    else:
        album = ''
    unique_track = (track.get_name(), artist, album)

    # TODO get VAD?

    return unique_track


if __name__ == "__main__":

    available_opts = ('-l', '-d', '-t', '-a')

    if len(sys.argv) != 2 or sys.argv[1] not in available_opts:
        print(f'Usage: python3 {sys.argv[0]} [Option]')
        print('Options:')
        print('\t-l => Scrapes listeners from top listeners, obtained from top tags')
        print('\t-d => Obtains data from listeners saved with -l')
        print('\t-t => Obtains top tags for all the items stored with -d')
        print('\t-a => Does everything. Scrapes listeners and obtains data and tags')
        sys.exit()

    if sys.argv[1] in ('-l', '-a'):
        with requests.Session() as s:

            print('Logging in...')
            login_lastfm(s)

            print('Getting top 10 tags...')
            # Get top 10 tags
            chart_tags = get_chart_top_tags(limit=10)
            print(f"Tags: {[tag.name for tag in chart_tags]}", end='\n\n')

            print('Getting top artists...')
            # Get unique top artists for each tag
            tag_top_artists = get_tag_top_artists(chart_tags)
            print(f"{len(tag_top_artists)} artists in total", end='\n\n')

            unique_listeners = set()

            print('Getting top listeners for each artist...')
            # Get top 30 listeners for each artist
            artist_listeners = dict()  # Key:Item = Artist:Listeners
            all_listeners_count = 0
            for i, artist in enumerate(tag_top_artists):
                print(f"\t[{i+1}] {artist}")
                top_listeners = get_top_listeners(s, artist)
                unique_listeners.update(top_listeners)

                artist_listeners[artist] = top_listeners
                all_listeners_count += len(top_listeners)

                time.sleep(1)

            print(f'# Unique listeners: {len(unique_listeners)}')
            print(f'# All listeners: {all_listeners_count}')

            # Save listeners by artist
            artist_listeners = dict(sorted(artist_listeners.items()))
            with open(f'{DATA_FOLDER}/top_listeners_by_artist.json', 'w') as f:
                f.write(json.dumps(artist_listeners,
                        indent=4, ensure_ascii=False))

            # Save all unique listeners
            unique_listeners = sorted(unique_listeners)
            with open(f'{DATA_FOLDER}/all_unique_listeners.dat', 'w') as f:
                for l in unique_listeners:
                    f.write(f"{l}\n")

    if sys.argv[1] in ('-d', '-a'):

        # Get loved/recent/top tracks, top artists, top albums
        # NOTE: Search tags of each item AFTER storing everything
        # tags = [tag[0].get_name()
        #     for tag in x.get_top_tags(limit=TAG_LIMIT)]

        # unique_tags.update(tags)
        #             item_tags[unique_track] = tags
        # TODO: VAD
        # kb = pylast.Artist('Kudasaibeats', network)
        # for x in kb.get_top_tags():
        #     print(x.item.get_name())
        # print(kb.get_bio_summary())

        # # Maybe use some tags + bio summary to evaluate VAD of an artist
        # print(genius.search_song('lone digger', 'caravan palace').lyrics)

        unique_artists = set()
        unique_albums = set()
        unique_tracks = set()
        loved_tracks = dict()
        recent_tracks = dict()
        top_tracks = dict()
        top_artists = dict()
        top_albums = dict()

        with open(f'{DATA_FOLDER}/all_unique_listeners.dat', 'r') as f:
            print('Getting data from all unique listeners...')
            for i, listener in enumerate(f.readlines()[:1]):
                listener = listener.strip()

                print(f'[{i}] {listener}')
                user = network.get_user(listener)

                # ---------------------- Loved Tracks ----------------------
                print('\t- Getting loved tracks...')
                lt = user.get_loved_tracks(limit=TRACK_LIMIT)
                loved_tracks[listener] = list()
                for t in lt:
                    track = t[0]
                    unique_track = get_track_info(track)
                    track_name, artist, album = unique_track

                    if album:
                        unique_albums.add('\u254E'.join([album, artist]))
                    unique_artists.add(artist)
                    unique_tracks.add('\u254E'.join(unique_track))

                    loved_tracks[listener].append(
                        '\u254E'.join([track_name, str(t[-1])]))

                # ---------------------- Recent Tracks ----------------------
                print('\t- Getting recent tracks...')
                rt = user.get_recent_tracks(limit=TRACK_LIMIT)
                recent_tracks[listener] = list()
                for t in rt:
                    track = t[0]
                    unique_track = get_track_info(track)
                    track_name, artist, album = unique_track

                    if album:
                        unique_albums.add('\u254E'.join([album, artist]))
                    unique_artists.add(artist)
                    unique_tracks.add('\u254E'.join(unique_track))

                    recent_tracks[listener].append(
                        '\u254E'.join([track_name, str(t[-1])]))

                # ---------------------- Top Tracks ----------------------
                print('\t- Getting top tracks...')
                tt = user.get_top_tracks(limit=TRACK_LIMIT)
                top_tracks[listener] = list()
                for t in tt:
                    track = t[0]
                    unique_track = get_track_info(track)
                    track_name, artist, album = unique_track

                    if album:
                        unique_albums.add('\u254E'.join([album, artist]))
                    unique_artists.add(artist)
                    unique_tracks.add('\u254E'.join(unique_track))

                    top_tracks[listener].append(track_name)

                # ---------------------- Artists ----------------------
                print('\t- Getting top artists...')
                top_artists[listener] = list()
                for artist in user.get_top_artists(limit=ARTIST_LIMIT):
                    artist = artist[0]
                    artist_name = artist.get_name()
                    unique_artists.add(artist_name)
                    top_artists[listener].append(artist_name)
                    # TODO get VAD?

                # ---------------------- Albums ----------------------
                print('\t- Getting top albums...')
                top_albums[listener] = list()
                for album in user.get_top_albums(limit=ALBUM_LIMIT):
                    album = album[0]
                    artist_name = album.get_artist().get_name()
                    album_name = album.get_name()
                    unique_albums.add('\u254E'.join([album_name, artist_name]))
                    top_albums[listener].append(
                        '\u254E'.join([album_name, artist_name]))
                    # TODO get VAD?

        with open(f'{DATA_FOLDER}/loved_tracks.json', 'w') as f:
            f.write(json.dumps(loved_tracks,
                    indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/recent_tracks.json', 'w') as f:
            f.write(json.dumps(recent_tracks,
                    indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/top_tracks.json', 'w') as f:
            f.write(json.dumps(top_tracks, indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/top_artists.json', 'w') as f:
            f.write(json.dumps(top_artists, indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/top_albums.json', 'w') as f:
            f.write(json.dumps(top_albums, indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/unique_tracks.dat', 'w') as f:
            for track in unique_tracks:
                f.write(f"{track}\n")

        with open(f'{DATA_FOLDER}/unique_artists.dat', 'w') as f:
            for artist in unique_artists:
                f.write(f"{artist}\n")

        with open(f'{DATA_FOLDER}/unique_albums.dat', 'w') as f:
            for album in unique_albums:
                f.write(f"{album}\n")

    if sys.argv[1] in ('-t', '-a'):
        # Get top tags for items (artists, albums, tracks)
        item_tags = dict()
        unique_tags = set()

        with open(f'{DATA_FOLDER}/item_tags.json', 'w') as f:
            f.write(json.dumps(item_tags, indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/unique_tags.dat', 'w') as f:
            for tag in unique_tags:
                f.write(f"{tag}\n")
