from lyricsgenius import Genius
from bs4 import BeautifulSoup
import pylast
import requests
import time
import json

genius = Genius(
    "wub8JMLwasqRZWGFM-JwSDrfT1YCFLah7T1tDvC6km3BhadU1D4vT1IsOfHNuOIq")
network = pylast.LastFMNetwork(
    "23ff8e4c454cbb8ae4a13440bc0fa745", "a5efd0d4bbeed8c37b0c4bd7672edf58"
)

payload = {"username_or_email": "Acervans", "password": "computer1A."}

LOGIN_URL = "https://www.last.fm/login"

# kb = pylast.Artist('Kudasaibeats', network)
# for x in kb.get_top_tags():
#     print(x.item.get_name())
# print(kb.get_bio_summary())

# # Maybe use some tags + bio summary to evaluate VAD of an artist
# print(genius.search_song('lone digger', 'caravan palace').lyrics)


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


def get_top_tags(limit):
    return [tag[0] for tag in network.get_top_tags(limit=limit)]


def get_tag_top_artists(tags):
    top_tag_artists = set()
    for tag in tags:
        top_tag_artists.update(
            [artist[0].get_name() for artist in tag.get_top_artists()]
        )
    return top_tag_artists


if __name__ == "__main__":

    with requests.Session() as s:

        print('Logging in...')
        login_lastfm(s)

        print('Getting top 10 tags...')
        # Get top 10 tags
        chart_tags = get_top_tags(limit=10)
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
        with open('top_listeners_by_artist.json', 'w') as f:
            f.write(json.dumps(artist_listeners, indent=4))

        # Save all unique listeners
        with open('all_unique_listeners.dat', 'w') as f:
            for l in unique_listeners:
                f.write(f"{l}\n")

        for artist, listeners in artist_listeners.items():
            # Get loved/recent/top songs, top tags, top artists
            pass
