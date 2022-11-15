import json
DATA_FOLDER = '../data/lastfm_data'
with open(f'{DATA_FOLDER}/top_albums.json', 'r', encoding='utf-8') as f:
    t1 = json.load(f)
with open(f'{DATA_FOLDER}/top_artists.json', 'r', encoding='utf-8') as f:
    t2 = json.load(f)
with open(f'{DATA_FOLDER}/top_tracks.json', 'r', encoding='utf-8') as f:
    t3 = json.load(f)
with open(f'{DATA_FOLDER}/loved_tracks.json', 'r', encoding='utf-8') as f:
    t4 = json.load(f)
with open(f'{DATA_FOLDER}/recent_tracks.json', 'r', encoding='utf-8') as f:
    t5 = json.load(f)

with open(f'{DATA_FOLDER}/unique_tracks.dat', 'r', encoding='utf-8') as f:
    num_tracks = len(f.readlines())

with open(f'{DATA_FOLDER}/unique_listeners.dat', 'r', encoding='utf-8') as f:
    num_users = len(f.readlines())

with open(f'{DATA_FOLDER}/unique_artists.dat', 'r', encoding='utf-8') as f:
    num_artists = len(f.readlines())

with open(f'{DATA_FOLDER}/unique_albums.dat', 'r', encoding='utf-8') as f:
    num_albums = len(f.readlines())

users = t1.keys()
c_exclude_loved = 0
c_all_items = 0
c_albums = 0
c_artists = 0
c_ltracks = 0
c_ttracks = 0
c_rtracks = 0
for u in users:
    if t1[u] and t2[u] and t3[u] and t5[u]:
        c_exclude_loved += 1
        if t4[u]:
            c_all_items += 1

    if t1[u]:
        c_albums += 1
    if t2[u]:
        c_artists += 1
    if t3[u]:
        c_ttracks += 1
    if t4[u]:
        c_ltracks += 1
    if t5[u]:
        c_rtracks += 1

print(f"Unique tracks: {num_tracks}")
print(f"Unique artists: {num_artists}")
print(f"Unique albums: {num_albums}")
print(f"Unique listeners (valid/total): {len(t1)}/{num_users}\n")

print(f"Users with top tracks: {c_ttracks}")
print(f"Users with recent tracks: {c_rtracks}")
print(f"Users with loved tracks: {c_ltracks}")
print(f"Users with top albums: {c_albums}")
print(f"Users with top artists: {c_artists}\n")

print(f"Users with data of all types: {c_all_items}")
print(f"Users with data of all types except loved tracks: {c_exclude_loved}")
