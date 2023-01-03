DATA = ../data/lastfm_data

LISTENERS = $(DATA)/all_unique_listeners.dat $(DATA)/top_listeners_by_artist.json
LISTENER_DATA = $(DATA)/top_tracks.json $(DATA)/loved_tracks.json $(DATA)/recent_tracks.json $(DATA)/top_albums.json $(DATA)/top_artists.json\
				$(DATA)/item_tags.json $(DATA)/unique_albums.dat $(DATA)/unique_artists.dat $(DATA)/unique_tags.dat $(DATA)/unique_tracks.dat
TAG_DATA = $(DATA)/unique_tags.dat $(DATA)/item_tags.json
VAD_DATA = $(DATA)/item_vads.json $(DATA)/tag_vads.json

all:

reset_db:
	make -C ../.. $@

clean_listeners:
	rm -f $(LISTENERS)

clean_data:
	rm -f $(LISTENER_DATA)

clean_tags:
	rm -f $(TAG_DATA)

clean_vads:
	rm -f $(VAD_DATA)

clean_all:
	rm -f $(LISTENERS) $(LISTENER_DATA) $(TAG_DATA) $(VAD_DATA)