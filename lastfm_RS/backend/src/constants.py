import lyricsgenius
import pylast

# General
DATA_FOLDER = '../data/lastfm_data'
SQL_FOLDER = '../sql'
SEPARATOR = '\u254E'

# Genius API Interface
GENIUS = lyricsgenius.Genius(
    'wub8JMLwasqRZWGFM-JwSDrfT1YCFLah7T1tDvC6km3BhadU1D4vT1IsOfHNuOIq', verbose=False)
# LastFM API Interface
PYLAST = pylast.LastFMNetwork(
    '23ff8e4c454cbb8ae4a13440bc0fa745', 'a5efd0d4bbeed8c37b0c4bd7672edf58')

# Constants from get_lastfm_data.py
LOGIN_URL = "https://www.last.fm/login"

MAX_PLAYCOUNT_PER_DAY = 2000
MAX_ATTEMPTS = 50

CHART_LIMIT = 50
TRACK_LIMIT = 20
ARTIST_LIMIT = 10
ALBUM_LIMIT = 10
TAG_LIMIT = 10

MAX_WIKIPEDIA_REQUEST = 300
TAG_VAD_THRESHOLD = 10
WEIGHT_RATIO = 1/1.2  # Must be between 0.5 and 1
