from constants import *
import json


def duplicate_tracks_without_album():
    """ Removes tracks WITHOUT album that have a duplicate WITH album """

    with open(f'{DATA_FOLDER}/unique_tracks.dat', 'r', encoding='utf-8') as f:
        tracks = f.readlines()
    with open(f'{DATA_FOLDER}/item_tags.json', 'r', encoding='utf-8') as f:
        item_tags = json.load(f)

    print(len(tracks))
    inserted = list()
    repeated = set()
    noalbum = set()
    for t in tracks:
        t = t[:-1]
        if SEPARATOR in t:
            name, artist, album = t.split(SEPARATOR)
            track_artist = SEPARATOR.join((name, artist, ''))
            if track_artist.lower() not in repeated:
                repeated.add(track_artist.lower())
                inserted.append(t)
                if not album:
                    noalbum.add(t)
            elif album and track_artist in noalbum:
                inserted.remove(track_artist)
                inserted.append(t)

    print(len(inserted))
    with open(f'{DATA_FOLDER}/unique_tracks.dat', 'w', encoding='utf-8') as f:
        for t in inserted:
            f.write(f"{t}\n")

    inserted = set(inserted)
    deleted = list()
    for t in item_tags['Tracks']:
        if t not in inserted:
            deleted.append(t)
    for dt in deleted:
        del item_tags['Tracks'][dt]

    with open(f'{DATA_FOLDER}/item_tags.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(item_tags, indent=4, ensure_ascii=False))


duplicate_tracks_without_album()
