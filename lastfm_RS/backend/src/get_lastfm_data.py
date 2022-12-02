from lyricsgenius import Genius
from nrc_vad_analysis import analyze_string
from bs4 import BeautifulSoup
from datetime import date
from requests.exceptions import ConnectionError, ReadTimeout
from wikipedia.exceptions import WikipediaException, PageError, DisambiguationError
import pylast
import wikipedia
import requests
import json
import sys
import numpy as np

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
TAG_LIMIT = 10

TAG_VAD_THRESHOLD = 10
WEIGHT_RATIO = 1/1.2  # Must be between 0.5 and 1


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
    session.post(LOGIN_URL, data=payload, headers=dict(Referer=LOGIN_URL))


def get_top_listeners(session, artist):
    artist_url = "https://www.last.fm/music/" + \
        artist.replace(" ", "+") + "/+listeners"
    soup = BeautifulSoup(session.get(
        artist_url).content, "html.parser")
    top_listeners_div = soup.find("div", {"class": "buffer-standard"})

    top_listeners = list()
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


def get_pylast_item(item, item_type):
    if item_type == "Artists":
        return network.get_artist(item)
    if item_type == "Albums":
        album_name, artist = item.split(SEPARATOR)
        return network.get_album(artist, album_name)
    if item_type == "Tracks":
        track_name, artist, _ = item.split(SEPARATOR)
        return network.get_track(artist, track_name)


def is_music_page(page: wikipedia.WikipediaPage):
    return any(['music' in cat.lower() for cat in page.categories])


def search_wikipedia_music_page(title, music_suffix=False):
    if music_suffix:
        title += " music"
    pages = wikipedia.search(title)
    page = None
    if pages:
        try:
            page = wikipedia.page(pages[0], auto_suggest=False)
        except DisambiguationError as e:
            # Use disambiguation suggestion
            for suggestion in str(e).split('\n')[1:]:
                # Avoid disambiguations
                if not suggestion.endswith("(disambiguation)"):
                    try:
                        page = wikipedia.page(suggestion, auto_suggest=False)
                    # Check next suggestion if non-existent
                    except (PageError, DisambiguationError):
                        continue

    # Page non-existent or not music-related
    if not music_suffix and (not page or (page and not is_music_page(page))):
        # Check page with music topic
        music_page = search_wikipedia_music_page(title, music_suffix=True)
        if music_page:
            page = music_page

    return page


def get_vad_average(tags, tag_vads, weighted=True):
    vadst = list()
    for tag in tags:
        if tag_vads[tag]:
            vadst.append([float(val)
                         for val in tag_vads[tag]])
    if vadst:
        if weighted:
            weights = [(WEIGHT_RATIO)**i for i in range(1, len(vadst)+1)]
        else:
            weights = None
        vadst = np.average(vadst, weights=weights, axis=0).tolist()
    return vadst


def print_load_percentage(item_num, total_items):
    perc = item_num*100//total_items
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %d%% (%d/%d)" %
                     ('='*(perc//2), perc, item_num, total_items))
    sys.stdout.flush()


if __name__ == "__main__":

    available_opts = ('-l', '-d', '-t', '-v', '-s', '-a')

    if len(sys.argv) != 2 or sys.argv[1] not in available_opts:
        print(f'Usage: python3 {sys.argv[0]} [Option]')
        print('Options:')
        print('\t-l => Scrapes listeners from top listeners, obtained from chart tags')
        print('\t-d => Obtains data from listeners saved with -l')
        print('\t-t => Obtains top tags for all items stored with -d')
        print('\t-v => Obtains the VAD value of each unique tag obtained with -t')
        print('\t-s => Obtains the mean VAD sentiment values for all items stored with -d')
        print(
            '\t-a => Does everything. Scrapes listeners, obtains data, tags and VAD values')
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
                            unique_artists.add(artist_name)
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

        # Get top tags for items (artists, albums, tracks)
        item_tags = dict()
        unique_pylast_tags = set()

        item_tags['Artists'] = dict()
        item_tags['Albums'] = dict()
        item_tags['Tracks'] = dict()

        # Get tags for each type of item
        for item_name, item_dict in item_tags.items():
            with open(f'{DATA_FOLDER}/unique_{item_name.lower()}.dat', 'r', encoding='utf-8') as f:
                unique_items = f.readlines()
                total_items = len(unique_items)
                print(
                    f'Getting tags for all {total_items} unique {item_name}: ')

                for i, item in enumerate(unique_items):
                    item = item.strip()
                    item_dict[item] = list()
                    attempts = 0
                    while attempts < MAX_ATTEMPTS:
                        try:
                            # Obtain instance of pylast object
                            item_pylast = get_pylast_item(item, item_name)
                            # Obtain pylast tags
                            tags_pylast = get_tags_list(item_pylast, TAG_LIMIT)
                            # Get tags as strings
                            tags = [tag.name for tag in tags_pylast if tag.name]
                            # Assign tags to current item
                            item_dict[item] = tags
                            # Update unique pylast Tags
                            unique_pylast_tags.update(tags_pylast)
                            # NOTE For Tracks, use lyrics to get additional VAD values

                            print_load_percentage(i+1, total_items)
                            break

                        except pylast.PyLastError as e:
                            if e.__cause__ and str(e.__cause__) == f"{item_name[:-1]} not found":
                                break
                            else:
                                attempts += 1
                print('\n')

        print('Saving unique tags and items\' tag data... ', end='')
        with open(f'{DATA_FOLDER}/item_tags.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(item_tags, indent=4, ensure_ascii=False))

        # Use pylast objects to ensure unique tags
        unique_tags = sorted([ptag.name for ptag in unique_pylast_tags])
        with open(f'{DATA_FOLDER}/unique_tags.dat', 'w', encoding='utf-8') as f:
            for tag in unique_tags:
                f.write(f"{tag}\n")
        print('SUCCESS\n')

    if sys.argv[1] in ('-v', '-a'):

        # Get VAD + StSc for each unique tag
        tag_vads = dict()

        # English Wikipedia
        wikipedia.set_lang('en')
        # Enable rate limiting
        wikipedia.set_rate_limiting(True)

        with open(f'{DATA_FOLDER}/unique_tags.dat', 'r', encoding='utf-8') as f:
            unique_tags = f.readlines()
            total_tags = len(unique_tags)
            print(
                f'Getting VAD values for all {total_tags} unique Tags: ')
            # Get VAD for each unique tag
            for i, tag in enumerate(unique_tags):
                tag = tag.strip()
                tag_vads[tag] = list()
                attempts = 0
                while attempts < MAX_ATTEMPTS:
                    try:
                        # Get Wikipedia page for tag
                        page = search_wikipedia_music_page(tag)
                        if page:
                            # Get Wikipedia summary for tag
                            text = page.summary
                            # Analyze summary and extract VAD and StSc
                            vad = analyze_string(text, detailed=True)

                            if 'N/A' not in vad:
                                vadsc = vad[1], vad[4], vad[5], vad[3]
                                # Assign VAD and StSc to current tag
                                tag_vads[tag] = vadsc

                        print_load_percentage(i+1, total_tags)
                        break

                    except (ConnectionError, ReadTimeout):
                        attempts += 1
                    except WikipediaException:
                        continue
                    except KeyError:
                        break
            print('\n')

        print('Saving tags\' VAD values... ', end='')
        with open(f'{DATA_FOLDER}/tag_vads.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(tag_vads, indent=4, ensure_ascii=False))
        print('SUCCESS')

    if sys.argv[1] in ('-s', '-a'):

        # Get VAD values for items (artists, albums, tracks)
        item_vads = dict()

        with open(f'{DATA_FOLDER}/item_tags.json', 'r', encoding='utf-8') as f:
            item_tags = json.load(f)
        with open(f'{DATA_FOLDER}/tag_vads.json', 'r', encoding='utf-8') as f:
            tag_vads = json.load(f)

        # Lowercase tag keys in tag_vads
        tag_vads = dict([(k.lower(), v) for k, v in tag_vads.items()])

        for item_name, item_dict in item_tags.items():
            item_vads[item_name] = dict()
            total_items = len(item_tags[item_name])
            print(
                f'Getting VAD values for all {total_items} unique {item_name}: ')
            for i, (item, tags) in enumerate(item_dict.items()):
                # NOTE Try different weights for averages

                # Lowercase tags for each item
                tags = [t.lower() for t in tags]
                vadst_mean = get_vad_average(
                    tags[:TAG_VAD_THRESHOLD], tag_vads, weighted=True)
                item_vads[item_name][item] = vadst_mean

                print_load_percentage(i+1, total_items)
            print('\n')

        print('Saving items\' VAD data... ', end='')
        with open(f'{DATA_FOLDER}/item_vads.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(item_vads, indent=4, ensure_ascii=False))
        print('SUCCESS')
