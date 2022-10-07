import pylast
from lyricsgenius import Genius

genius = Genius(
    'wub8JMLwasqRZWGFM-JwSDrfT1YCFLah7T1tDvC6km3BhadU1D4vT1IsOfHNuOIq')
network = pylast.LastFMNetwork(
    '23ff8e4c454cbb8ae4a13440bc0fa745', 'a5efd0d4bbeed8c37b0c4bd7672edf58')

# kb = pylast.Artist('Kudasaibeats', network)
# for x in kb.get_top_tags():
#     print(x.item.get_name())
# print(kb.get_bio_summary())

# # Maybe use some tags + bio summary to evaluate VAD of an artist

# print(genius.search_song('lone digger', 'caravan palace').lyrics)

if __name__ == '__main__':

    # usa_top = network.get_geo_top_artists('United States')
    # uk_top = network.get_geo_top_artists('United Kingdom')

    chart_tags = [tag[0] for tag in network.get_top_tags(limit=10)]

    top_tag_artists = set()
    for tag in chart_tags:
        top_tag_artists.update([artist[0].get_name() for artist in tag.get_top_artists()])

    print(top_tag_artists)