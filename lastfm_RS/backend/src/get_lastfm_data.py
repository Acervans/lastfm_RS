from lyricsgenius import Genius
# from nrc_vad_analysis import analyze_string, analyze_text
from bs4 import BeautifulSoup
from datetime import date
import sqlalchemy
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

network.enable_rate_limit()
network.enable_caching()

payload = {"username_or_email": "Test_EPS", "password": "Tfg.EPS2022"}

DATA_FOLDER = '../data/lastfm_data'
LOGIN_URL = "https://www.last.fm/login"

SEPARATOR = '\u254E'
MAX_PLAYCOUNT_PER_DAY = 2000
MAX_ATTEMPTS = 50

CHART_LIMIT = 50
TRACK_LIMIT = 20
ARTIST_LIMIT = 10
ALBUM_LIMIT = 10
TAG_LIMIT = 5


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
    if top_listeners_div:
        # Check top listeners
        if not top_listeners_div.find("p", {"class": "no-data-message"}):
            # Get top listeners
            top_listeners_list = top_listeners_div.find_all(
                "a", {"class": "link-block-target"})
            top_listeners = [listener.get_text()
                             for listener in top_listeners_list]

    return top_listeners


def get_tag_top_artists(tags):
    tag_top_artists = set()
    for tag in tags:
        tag_top_artists.update(
            [artist[0].get_name() for artist in tag.get_top_artists()]
        )
    return tag_top_artists


def get_track_info(track: pylast.Track):
    artist = track.get_artist().get_name()
    try:
        album = track.get_album()
    except pylast.WSError as e:
        if str(e) == "Track not found":
            return None
        else:
            raise e
    except Exception:
        album = None

    if album:
        album = album.get_name()
    else:
        album = ''
    unique_track = (track.get_name(), artist, album)

    return unique_track


def get_tags_list(tagged_item, limit, names_only=False):
    top_tags = tagged_item.get_top_tags(limit=limit)
    if names_only:
        return [tag[0].name for tag in top_tags]
    else:
        return [tag[0] for tag in top_tags]


def print_load_percentage(item_num, total_items):
    perc = item_num*100//total_items
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*(perc//5), perc))
    sys.stdout.flush()


if __name__ == "__main__":

    available_opts = ('-l', '-d', '-t', '-a')

    if len(sys.argv) != 2 or sys.argv[1] not in available_opts:
        print(f'Usage: python3 {sys.argv[0]} [Option]')
        print('Options:')
        print('\t-l => Scrapes listeners from top listeners, obtained from chart tags')
        print('\t-d => Obtains data from listeners saved with -l')
        print('\t-t => Obtains top tags and VAD values for all the items stored with -d')
        print('\t-a => Does everything. Scrapes listeners and obtains data and tags')
        sys.exit()

    if sys.argv[1] in ('-l', '-a'):
        with requests.Session() as s:

            print('Logging in...')
            login_lastfm(s)

            print(f'Getting top {CHART_LIMIT} tags...')
            # Get top chart tags
            chart_tags = get_tags_list(network, limit=CHART_LIMIT)
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

            print('Saving listeners... ', end='')
            # Save listeners by artist
            artist_listeners = dict(sorted(artist_listeners.items()))
            with open(f'{DATA_FOLDER}/top_listeners_by_artist.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(artist_listeners,
                        indent=4, ensure_ascii=False))

            # Save all unique listeners
            unique_listeners = sorted(unique_listeners)
            with open(f'{DATA_FOLDER}/unique_listeners.dat', 'w', encoding='utf-8') as f:
                for l in unique_listeners:
                    f.write(f"{l}\n")
            print('SUCCESS')

    if sys.argv[1] in ('-d', '-a'):

        # Get loved/recent/top tracks, top artists, top albums
        unique_artists = set()
        unique_albums = set()
        unique_tracks = set()
        loved_tracks = dict()
        recent_tracks = dict()
        top_tracks = dict()
        top_artists = dict()
        top_albums = dict()

        with open(f'{DATA_FOLDER}/unique_listeners.dat', 'r') as f:
            unique_listeners = f.read().splitlines()
            print(
                f'Getting data from all {len(unique_listeners)} unique listeners...')
            for i, listener in enumerate(unique_listeners):

                print(f'[{i+1}] {listener}')
                user = network.get_user(listener)

                # Check if user still exists
                try:
                    registered = int(user.get_registered())
                except pylast.WSError as e:
                    if str(e) == "User not found":
                        print(f"\t- User '{listener}' not found :(")
                        continue
                    else:
                        pass
                except pylast.NetworkError:
                    pass

                delta = date.today() - date.fromtimestamp(registered)
                isbot = False
                attempts = 0
                while attempts < MAX_ATTEMPTS:
                    try:
                        # More than 2000 scrobbles per day, probably a bot
                        isbot = user.get_playcount() > delta.days*MAX_PLAYCOUNT_PER_DAY
                        break
                    except pylast.WSError:
                        attempts += 1
                if isbot:
                    print(f"\t- User '{listener}' is a bot :(")
                    continue

                # ---------------------- Loved Tracks ----------------------
                print('\t- Getting loved tracks...')
                loved_tracks[listener] = list()
                attempts = 0
                while attempts < MAX_ATTEMPTS:
                    try:
                        for t in user.get_loved_tracks(limit=TRACK_LIMIT):
                            track = t[0]
                            unique_track = get_track_info(track)
                            if not unique_track:
                                continue
                            track_name, artist, album = unique_track

                            if album:
                                unique_albums.add(
                                    SEPARATOR.join([album, artist]))
                            unique_artists.add(artist)
                            unique_tracks.add(SEPARATOR.join(unique_track))

                            loved_tracks[listener].append(
                                SEPARATOR.join([track_name, artist, str(t[-1])]))
                        break

                    except pylast.PyLastError:
                        attempts += 1

                # ---------------------- Recent Tracks ----------------------
                print('\t- Getting recent tracks...')
                recent_tracks[listener] = list()
                attempts = 0
                while attempts < MAX_ATTEMPTS:
                    try:
                        for t in user.get_recent_tracks(limit=TRACK_LIMIT):
                            track = t[0]
                            unique_track = get_track_info(track)
                            if not unique_track:
                                continue
                            track_name, artist, album = unique_track

                            if album:
                                unique_albums.add(
                                    SEPARATOR.join([album, artist]))
                            unique_artists.add(artist)
                            unique_tracks.add(SEPARATOR.join(unique_track))

                            recent_tracks[listener].append(
                                SEPARATOR.join([track_name, artist, str(t[-1])]))
                        break

                    except (pylast.WSError, pylast.NetworkError):
                        attempts += 1
                    # Recent tracks hidden by user
                    except pylast.PyLastError as e:
                        if e.__cause__ and str(e.__cause__) == "Login: User required to be logged in":
                            break
                        else:
                            attempts += 1

                # ---------------------- Top Tracks ----------------------
                print('\t- Getting top tracks...')
                top_tracks[listener] = list()
                attempts = 0
                while attempts < MAX_ATTEMPTS:
                    try:
                        for t in user.get_top_tracks(limit=TRACK_LIMIT):
                            track = t[0]
                            unique_track = get_track_info(track)
                            if not unique_track:
                                continue
                            track_name, artist, album = unique_track

                            if album:
                                unique_albums.add(
                                    SEPARATOR.join([album, artist]))
                            unique_artists.add(artist)
                            unique_tracks.add(SEPARATOR.join(unique_track))

                            top_tracks[listener].append(
                                SEPARATOR.join([track_name, artist]))
                        break

                    except pylast.PyLastError:
                        attempts += 1

                # ---------------------- Artists ----------------------
                print('\t- Getting top artists...')
                top_artists[listener] = list()
                attempts = 0
                while attempts < MAX_ATTEMPTS:
                    try:
                        for artist in user.get_top_artists(limit=ARTIST_LIMIT):
                            artist = artist[0]
                            artist_name = artist.get_name()
                            unique_artists.add(artist_name)
                            top_artists[listener].append(artist_name)
                        break

                    except pylast.PyLastError:
                        attempts += 1

                # ---------------------- Albums ----------------------
                print('\t- Getting top albums...')
                top_albums[listener] = list()
                attempts = 0
                while attempts < MAX_ATTEMPTS:
                    try:
                        for album in user.get_top_albums(limit=ALBUM_LIMIT):
                            album = album[0]
                            artist_name = album.get_artist().get_name()
                            album_name = album.get_name()
                            unique_albums.add(SEPARATOR.join(
                                [album_name, artist_name]))
                            top_albums[listener].append(
                                SEPARATOR.join([album_name, artist_name]))
                        break

                    except pylast.PyLastError:
                        attempts += 1

        print('Saving track, artist and album data... ', end='')
        with open(f'{DATA_FOLDER}/loved_tracks.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(loved_tracks,
                    indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/recent_tracks.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(recent_tracks,
                    indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/top_tracks.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(top_tracks, indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/top_artists.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(top_artists, indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/top_albums.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(top_albums, indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/unique_tracks.dat', 'w', encoding='utf-8') as f:
            for track in unique_tracks:
                f.write(f"{track}\n")

        with open(f'{DATA_FOLDER}/unique_artists.dat', 'w', encoding='utf-8') as f:
            for artist in unique_artists:
                f.write(f"{artist}\n")

        with open(f'{DATA_FOLDER}/unique_albums.dat', 'w', encoding='utf-8') as f:
            for album in unique_albums:
                f.write(f"{album}\n")
        print('SUCCESS')

    if sys.argv[1] in ('-t', '-a'):
        # TODO: VAD
        # kb = pylast.Artist('Kudasaibeats', network)
        # for x in kb.get_top_tags():
        #     print(x.item.get_name())
        # print(kb.get_bio_summary())

        # Also get tracks per album or tracks per artist?

        # # Maybe use some tags + bio summary to evaluate VAD of an artist
        # print(genius.search_song('lone digger', 'caravan palace').lyrics)

        # Get top tags for items (artists, albums, tracks)
        item_tags = dict()
        unique_tags = set()
        item_vad = dict()

        item_tags['Artists'] = dict()
        item_vad['Artists'] = dict()
        with open(f'{DATA_FOLDER}/unique_artists.dat', 'r') as f:
            unique_artists = f.read().splitlines()
            total_artists = len(unique_artists)
            print(
                f'Getting tags and VAD for all {total_artists} unique artists: ')
            for i, artist in enumerate(unique_artists):
                artist_pylast = network.get_artist(artist)
                tags_pylast = get_tags_list(artist_pylast, TAG_LIMIT)
                tags = [tag.name for tag in tags_pylast]
                item_tags['Artists'][artist] = tags
                unique_tags.update(tags)
                # TODO get VAD
                # TODO get tags VAD

                print_load_percentage(i+1, total_artists)
            print('\n')

        item_tags['Albums'] = dict()
        item_vad['Albums'] = dict()
        with open(f'{DATA_FOLDER}/unique_albums.dat', 'r') as f:
            unique_albums = f.read().splitlines()
            total_albums = len(unique_albums)
            print(
                f'Getting tags and VAD for all {total_albums} unique albums: ')
            for i, album in enumerate(unique_albums):
                album_name, artist = album.split(SEPARATOR)
                album_pylast = network.get_album(artist, album_name)
                tags_pylast = get_tags_list(album_pylast, TAG_LIMIT)
                tags = [tag.name for tag in tags_pylast]
                item_tags['Albums'][album] = tags
                unique_tags.update(tags)
                # TODO get VAD
                # TODO get tags VAD

                print_load_percentage(i+1, total_albums)
            print('\n')

        item_tags['Tracks'] = dict()
        item_vad['Tracks'] = dict()
        with open(f'{DATA_FOLDER}/unique_tracks.dat', 'r') as f:
            unique_tracks = f.read().splitlines()
            total_tracks = len(unique_tracks)
            print(
                f'Getting tags and VAD for all {total_tracks} unique tracks: ')
            for i, track in enumerate(unique_tracks):
                track_name, artist, _ = track.split(SEPARATOR)
                track_pylast = network.get_track(artist, track_name)
                tags_pylast = get_tags_list(track_pylast, TAG_LIMIT)
                tags = [tag.name for tag in tags_pylast]
                item_tags['Tracks'][track] = tags
                unique_tags.update(tags)
                # TODO get VAD
                # TODO get tags VAD

                print_load_percentage(i+1, total_tracks)
            print()

        print('Saving tag and VAD data... ', end='')
        with open(f'{DATA_FOLDER}/item_tags.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(item_tags, indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/item_vad.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(item_vad, indent=4, ensure_ascii=False))

        with open(f'{DATA_FOLDER}/unique_tags.dat', 'w', encoding='utf-8') as f:
            for tag in unique_tags:
                f.write(f"{tag}\n")
        print('SUCCESS')

# db = sqlalchemy.create_engine("postgresql://alumnodb:alumnodb@localhost:5432/lastfm_db")
# conn = db.connect()
