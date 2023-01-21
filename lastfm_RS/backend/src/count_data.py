from constants import *
import json

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
with open(f'{DATA_FOLDER}/tag_vads.json', 'r', encoding='utf-8') as f:
    tag_vads = json.load(f)
with open(f'{DATA_FOLDER}/item_tags.json', 'r', encoding='utf-8') as f:
    item_tags = json.load(f)
with open(f'{DATA_FOLDER}/item_vads.json', 'r', encoding='utf-8') as f:
    item_vads = json.load(f)

with open(f'{DATA_FOLDER}/unique_tracks.dat', 'r', encoding='utf-8') as f:
    num_tracks = len(f.readlines())

with open(f'{DATA_FOLDER}/unique_listeners.dat', 'r', encoding='utf-8') as f:
    num_users = len(f.readlines())

with open(f'{DATA_FOLDER}/unique_artists.dat', 'r', encoding='utf-8') as f:
    num_artists = len(f.readlines())

with open(f'{DATA_FOLDER}/unique_albums.dat', 'r', encoding='utf-8') as f:
    num_albums = len(f.readlines())
    
with open(f'{DATA_FOLDER}/unique_tags.dat', 'r', encoding='utf-8') as f:
    num_tags = len(f.readlines())

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
       
c_tagw_vad = 0 
for tag, vads in tag_vads.items():
    if vads:
        c_tagw_vad += 1

c_itemw_tag = dict()
c_itemw_vad = dict()
for item_type in item_tags.keys():
    c_itemw_tag[item_type] = 0
    for item, tags in item_tags[item_type].items():
        if tags:
            c_itemw_tag[item_type] += 1
            
    c_itemw_vad[item_type] = 0
    for item, vads in item_vads[item_type].items():
        if vads:
            c_itemw_vad[item_type] += 1

print(f"Unique tracks: {num_tracks}")
print(f"Unique artists: {num_artists}")
print(f"Unique albums: {num_albums}")
print(f"Unique tags: {num_tags}")
print(f"Unique listeners (valid/total): {len(t1)}/{num_users}\n")

print(f"Users with top tracks: {c_ttracks}")
print(f"Users with recent tracks: {c_rtracks}")
print(f"Users with loved tracks: {c_ltracks}")
print(f"Users with top albums: {c_albums}")
print(f"Users with top artists: {c_artists}\n")

print(f"Users with data of all types: {c_all_items}")
print(f"Users with data of all types except loved tracks: {c_exclude_loved}\n")

print(f"Tags with VAD: {c_tagw_vad}/{num_tags}")
for item_type in c_itemw_tag.keys():
    print(f"{item_type} with tags: {c_itemw_tag[item_type]}/{len(item_tags[item_type])}")
    print(f"{item_type} with VADSc: {c_itemw_vad[item_type]}/{len(item_tags[item_type])}")