from .constants import *
from .nrc_vad_analysis import analyze_string
from bs4 import BeautifulSoup
from datetime import date
from collections import Counter
from requests.exceptions import ConnectionError, ReadTimeout
from wikipedia.exceptions import WikipediaException, PageError, DisambiguationError
import numpy as np
import pylast
import wikipedia
import requests
import json
import sys


payload = {"username_or_email": "Test_EPS", "password": "Tfg.EPS2022"}


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
    artist = track.get_artist().get_name(properly_capitalized=True)
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
        album = album.get_name(properly_capitalized=True)
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


def get_pylast_item(item, item_type, split=True):
    if item_type == "Artists":
        return PYLAST.get_artist(item)
    if item_type == "Albums":
        album_name, artist = item.split(SEPARATOR)
        return PYLAST.get_album(artist, album_name)
    if item_type == "Tracks":
        track_name, artist, _ = item.split(SEPARATOR)
        return PYLAST.get_track(artist, track_name)


def is_music_page(page: wikipedia.WikipediaPage):
    return any(['music' in cat.lower() for cat in page.categories])


def search_wikipedia_music_page(title, music_suffix=False):
    if music_suffix:
        title = title[:MAX_WIKIPEDIA_REQUEST - 6] + " music"
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
            chart_tags = get_tags_list(PYLAST, limit=CHART_LIMIT)
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
                user = PYLAST.get_user(listener)

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
                            artist_name = album.get_artist().get_name(properly_capitalized=True)
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

        # Get VAD + StR for each unique tag
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
                        page = search_wikipedia_music_page(
                            tag[:MAX_WIKIPEDIA_REQUEST])
                        if page:
                            # Get Wikipedia summary for tag
                            text = page.summary
                            # Analyze summary and extract VAD and StR
                            vad = analyze_string(text, detailed=True)

                            if 'N/A' not in vad:
                                vadsr = vad[1], vad[4], vad[5], vad[3]
                                # Assign VAD and StR to current tag
                                tag_vads[tag] = vadsr

                        print_load_percentage(i+1, total_tags)
                        break

                    except (ConnectionError, AssertionError, ReadTimeout):
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


######################### GET SINGLE USER DATA #########################

def get_user_data(username: str | pylast.User,
                  filepath: str = None,
                  use_items: dict = None,
                  include_tracks=False,
                  include_artists=False,
                  include_albums=False,
                  include_tags=False,
                  tracks_limit=TRACK_LIMIT,
                  artists_limit=ARTIST_LIMIT,
                  albums_limit=ALBUM_LIMIT,
                  tags_limit=TAG_LIMIT,
                  verbose=True) -> dict:
    """ Gets relevant last.fm data of a user into a dictionary

    Args:
        username (str | pylast.User): User to scrape data from
        filepath (str, optional): File to save data as pickle object
        use_items (dict, optional): Dict of pre-scraped items
        include_tracks (boolean, optional): Whether to include tracks
        include_artists (boolean, optional): Whether to include artists
        include_albums (boolean, optional): Whether to include albums
        include_tags (boolean, optional): Whether to include tags
        tracks_limit (int, optional): Track scrape limit
        artists_limit (int, optional): Artist scrape limit
        albums_limit (int, optional): Album scrape limit
        tags_limit (int, optional): Tag scrape limit
        verbose (boolean, optional): Print each step

    Returns:
        dict: Dictionary with all data retrieved
    """
    query = []
    if include_tracks:
        query.append('tracks')
    if include_artists:
        query.append('artists')
    if include_albums:
        query.append('albums')
    if include_tags:
        query.append('tags')
    query = ', '.join(query)

    if verbose:
        print(f"Querying {query} from user '{username}':", flush=True)

    data = use_items or dict()
    item_tags = data.get('ITEM_TAGS') or {
        'Artists': dict(),
        'Albums': dict(),
        'Tracks': dict()
    }

    if isinstance(username, str):
        user = PYLAST.get_user(username)

        # Check if user still exists
        try:
            user.get_registered()
        except pylast.WSError as e:
            if str(e) == "User not found":
                print(f"\t- User '{user}' not found :(")
                return {'ERROR': f'User {username} does not exist in Last.FM'}

        data['USER'] = username
    else:
        user = username

    # ---------------------- Tracks ----------------------

    if include_tracks:

        # ----------- Loved Tracks -----------

        if verbose:
            print('\t- Getting loved tracks...', end=' ', flush=True)

        loved_tracks = list()
        try:
            for t in user.get_loved_tracks(limit=tracks_limit or TRACK_LIMIT):
                track = t[0]
                unique_track = get_track_info(track)
                if not unique_track:
                    continue
                track_name, artist, album = unique_track

                # Name Artist Album Timestamp
                loved_tracks.append((track_name, artist, album, str(t[-1])))
                item_tags['Tracks'][unique_track] = list()

        except pylast.PyLastError as e:
            print(f"API Error -> Loved tracks for {username}: {e}")

        if verbose:
            print('OK')

        data['LOVED_TRACKS'] = loved_tracks

        # ----------- Recent Tracks -----------

        if verbose:
            print('\t- Getting recent tracks...', end=' ', flush=True)

        recent_tracks = list()
        try:
            for t in user.get_recent_tracks(limit=tracks_limit or TRACK_LIMIT):
                track = t[0]
                unique_track = get_track_info(track)
                if not unique_track:
                    continue
                track_name, artist, album = unique_track

                # Name Artist Album Timestamp
                recent_tracks.append((track_name, artist, album, str(t[-1])))
                item_tags['Tracks'][unique_track] = list()

        except (pylast.WSError, pylast.NetworkError) as e:
            print(f"Network Error -> Recent tracks for {username}: {e}")
        # Recent tracks hidden by user
        except pylast.PyLastError as e:
            if e.__cause__ and str(e.__cause__) == "Login: User required to be logged in":
                pass
            else:
                print(f"API Error -> Recent tracks for {username}: {e}")

        if verbose:
            print('OK')

        data['RECENT_TRACKS'] = recent_tracks

        # ----------- Top Tracks -----------

        if verbose:
            print('\t- Getting top tracks...', end=' ', flush=True)

        top_tracks = list()
        try:
            for t in user.get_top_tracks(limit=tracks_limit or TRACK_LIMIT):
                track = t[0]
                unique_track = get_track_info(track)
                if not unique_track:
                    continue
                track_name, artist, album = unique_track

                # Name Artist Album
                top_tracks.append((track_name, artist, album))
                item_tags['Tracks'][unique_track] = list()

        except pylast.PyLastError as e:
            print(f"API Error -> Top tracks for {username}: {e}")

        if verbose:
            print('OK')

        data['TOP_TRACKS'] = top_tracks

    # ---------------------- Artists ----------------------

    if include_artists:

        if verbose:
            print('\t- Getting top artists...', end=' ', flush=True)

        top_artists = list()
        try:
            for artist in user.get_top_artists(limit=artists_limit or ARTIST_LIMIT):
                artist = artist[0]
                artist_name = artist.get_name()

                top_artists.append(artist_name)
                item_tags['Artists'][artist_name] = list()

        except pylast.PyLastError as e:
            print(f"API Error -> Top artists for {username}: {e}")

        if verbose:
            print('OK')

        data['TOP_ARTISTS'] = top_artists

    # ---------------------- Albums ----------------------

    if include_albums:

        if verbose:
            print('\t- Getting top albums...', end=' ', flush=True)

        top_albums = list()
        try:
            for album in user.get_top_albums(limit=albums_limit or ALBUM_LIMIT):
                album = album[0]
                artist_name = album.get_artist().get_name(properly_capitalized=True)
                album_name = (album.get_name(), artist_name)

                top_albums.append(album_name)
                item_tags['Albums'][album_name] = list()

        except pylast.PyLastError as e:
            print(f"API Error -> Top albums for {username}: {e}")

        if verbose:
            print('OK')

        data['TOP_ALBUMS'] = top_albums

    # ---------------------- Tags ----------------------

    if include_tags:
        tags_count = Counter()

        if verbose:
            print('\t- Getting top tags for all items...', end=' ', flush=True)

        for item_type in item_tags:
            for item in item_tags[item_type]:
                try:
                    # Obtain tags as lowercase strings
                    unique_item = SEPARATOR.join(
                        item) if not isinstance(item, str) else item
                    pylast_item = get_pylast_item(unique_item, item_type)
                    tags = get_tags_list(
                        pylast_item, limit=tags_limit or TAG_LIMIT, names_only=True)

                    # Assign tags to current item
                    item_tags[item_type][item] = tags
                    # Update unique Tags counts
                    tags_count.update(tags)

                except pylast.PyLastError as e:
                    if e.__cause__ and str(e.__cause__) == f"{item_type[:-1]} not found":
                        continue
                    else:
                        print(
                            f"API Error -> {item} top tags for {username}: {e}")
                        continue

        for item_type in item_tags.keys():
            item_tags[item_type] = list(item_tags[item_type].items())

        if verbose:
            print('OK')

        data['TAGS_COUNT'] = tags_count.most_common(None)

    data['ITEM_TAGS'] = item_tags

    if filepath:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return data
