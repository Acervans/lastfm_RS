import pylast
from lyricsgenius import Genius

genius = Genius(
    'wub8JMLwasqRZWGFM-JwSDrfT1YCFLah7T1tDvC6km3BhadU1D4vT1IsOfHNuOIq')
network = pylast.LastFMNetwork(
    '23ff8e4c454cbb8ae4a13440bc0fa745', 'a5efd0d4bbeed8c37b0c4bd7672edf58')

kb = pylast.Artist('Kudasaibeats', network)
for x in kb.get_top_tags():
    print(x.item.get_name())
print(kb.get_bio_summary())

# Maybe use some tags + bio summary to evaluate VAD of an artist

print(genius.search_song('lone digger', 'caravan palace').lyrics)
