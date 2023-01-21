from sqlalchemy import create_engine, inspect, text, MetaData, select, Table
from datetime import datetime
from constants import *
import json


db = create_engine(
    "postgresql://alumnodb:alumnodb@localhost:5432/lastfm_db", client_encoding="UTF-8")


def table(name) -> Table:
    return metadata.tables[name]


def table_exists(engine, name):
    ins = inspect(engine)
    return ins.dialect.has_table(engine.connect(), name)


def is_table_empty(table):
    return False if db.execute(table.select().limit(1)).all() else True


def setup_db(engine):
    with engine.connect() as conn:
        with open(f"{SQL_FOLDER}/LastFM_DB.sql") as f:
            query = text(f.read())
            conn.execute(query)


def insert_items(engine, filename, insert_fun, **kwargs):
    with open(f"{DATA_FOLDER}/{filename}", encoding='utf-8') as f:
        if filename.endswith('.json'):
            items = json.load(f)
        else:
            items = [item.strip() for item in f.readlines()]

    with engine.connect() as conn:
        if kwargs:
            insert_fun(items, conn, kwargs=kwargs)
        else:
            insert_fun(items, conn)


def tag_insert(tag_vads, conn):
    stmts = list()
    for tag, vads in tag_vads.items():
        stmts.append({'name': tag, 'vad': vads})
    conn.execute(table('tag').insert(), stmts)


def artist_insert(item_vads, conn):
    stmts = list()
    inserted = set()
    artist_vads = item_vads["Artists"]
    for artist, vads in artist_vads.items():
        if artist.lower() not in inserted:
            inserted.add(artist.lower())
            stmts.append({'name': artist, 'vad': vads})
    conn.execute(table('artist').insert(), stmts)


def album_insert(item_vads, conn):
    stmts = list()
    inserted = set()
    album_vads = item_vads["Albums"]
    for album, vads in album_vads.items():
        if album.lower() not in inserted:
            inserted.add(album.lower())
            album_name, artist_name = album.split(SEPARATOR)
            artist_id = artist_ids[artist_name.lower()]
            stmts.append(
                {'name': album_name, 'artist_id': artist_id, 'vad': vads})
    conn.execute(table('album').insert(), stmts)


def track_insert(item_vads, conn):
    stmts = list()
    inserted = set()
    track_vads = item_vads["Tracks"]
    for track, vads in track_vads.items():
        if track.lower() not in inserted:
            inserted.add(track.lower())
            track_name, artist_name, album_name = track.split(SEPARATOR)
            artist_id = artist_ids[artist_name.lower()]
            if album_name:
                album_id = album_ids[SEPARATOR.join(
                    (album_name.lower(), artist_name.lower()))]
            else:
                album_id = None
            stmts.append({'name': track_name, 'artist_id': artist_id,
                          'album_id': album_id, 'vad': vads})
    conn.execute(table('track').insert(), stmts)


def user_insert(users, conn):
    stmts = list()
    for user in users:
        stmts.append({'username': user})
    conn.execute(table('user_').insert(), stmts)


def item_tag_insert(item_tags, conn):
    map_items = {"Albums": (album_ids, "albumtoptags"),
                 "Artists": (artist_ids, "artisttoptags"),
                 "Tracks": (track_ids, "tracktoptags")}

    for item_type, item_dict in item_tags.items():
        stmts = list()
        table_id = None
        inserted = set()
        for item, tags in item_dict.items():
            item_split = item.split(SEPARATOR)
            if len(item_split) > 1:
                key = SEPARATOR.join(
                    (item_split[0].lower(), item_split[1].lower()))
            else:
                key = item_split[0].lower()

            if key not in inserted:
                inserted.add(key)
                id_dict, table_id = map_items[item_type]
                id_key = item_type.lower()[:-1] + "_id"
                tags = {tag.lower() for tag in tags}
                for tag in tags:
                    stmts.append(
                        {id_key: id_dict[key], 'tag_id': tag_ids[tag.lower()]})
        conn.execute(table(table_id).insert(), stmts)


def top_item_insert(top_items, conn, kwargs):
    stmts = list()
    table_name = kwargs['table_name']
    id_dict = kwargs['id_dict']
    id_key = kwargs['id_key']
    for user, items in top_items.items():
        user_id = user_ids[user.lower()]
        inserted = set()
        for item in items:
            item_key = item.lower()
            if item_key not in inserted and item_key in id_dict:
                inserted.add(item_key)
                stmts.append({'user_id': user_id, id_key: id_dict[item_key]})
    conn.execute(table(table_name).insert(), stmts)


def track_timestamp_insert(tracks, conn, kwargs):
    stmts = list()
    table_name = kwargs['table_name']
    timestamp_col = kwargs['timestamp_col']
    for user, items in tracks.items():
        user_id = user_ids[user.lower()]
        inserted = set()
        for item in items:
            if item.lower() not in inserted:
                inserted.add(item.lower())
                item_split = item.split(SEPARATOR)
                key = SEPARATOR.join(
                    (item_split[0].lower(), item_split[1].lower()))
                stmts.append({'user_id': user_id,
                              'track_id': track_ids[key],
                              timestamp_col: datetime.utcfromtimestamp(int(item_split[2]))})
    conn.execute(table(table_name).insert(), stmts)


if __name__ == "__main__":
    global metadata, tag_ids, artist_ids, album_ids, track_ids, user_ids

    # Create tables and relations using SQL script
    if not table_exists(db, 'track'):
        print('Creating tables... ', end='', flush=True)
        setup_db(db)
        print('SUCCESS')

    # Load table definitions from lastfm_db
    metadata = MetaData()
    metadata.reflect(bind=db)

    # Insert tags if empty
    print('Inserting tags... ', end='', flush=True)
    if is_table_empty(table('tag')):
        insert_items(db, 'tag_vads.json', tag_insert)
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    with db.connect() as conn:
        tag_ids = {tag.lower(): t_id for tag, t_id in conn.execute(
            select(table('tag').c.name, table('tag').c.id))}

    # Insert artists if empty
    print('Inserting artists... ', end='', flush=True)
    if is_table_empty(table('artist')):
        insert_items(db, 'item_vads.json', artist_insert)
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    with db.connect() as conn:
        artist_ids = {artist.lower(): a_id for artist, a_id in conn.execute(
            select(table('artist').c.name, table('artist').c.id))}
        artist_names = {v: k for k, v in artist_ids.items()}

    # Insert albums if empty
    print('Inserting albums... ', end='', flush=True)
    if is_table_empty(table('album')):
        insert_items(db, 'item_vads.json', album_insert)
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    with db.connect() as conn:
        album_ids = {SEPARATOR.join((album.lower(), artist_names[artist].lower())): a_id for album, artist, a_id in conn.execute(
            select(table('album').c.name, table('album').c.artist_id, table('album').c.id))}

    # Insert tracks if empty
    print('Inserting tracks... ', end='', flush=True)
    if is_table_empty(table('track')):
        insert_items(db, 'item_vads.json', track_insert)
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    with db.connect() as conn:
        track_ids = {SEPARATOR.join((track.lower(), artist_names[artist].lower())): t_id for track, artist, t_id in conn.execute(
            select(table('track').c.name, table('track').c.artist_id, table('track').c.id))}

    # Insert users if empty
    print('Inserting users... ', end='', flush=True)
    if is_table_empty(table('user_')):
        insert_items(db, 'unique_listeners.dat', user_insert)
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    with db.connect() as conn:
        user_ids = {user.lower(): u_id for user, u_id in conn.execute(
            select(table('user_').c.username, table('user_').c.id))}

    # Insert items tags if empty
    print('Inserting items tags... ', end='', flush=True)
    if is_table_empty(table('albumtoptags')) or is_table_empty(
            table('artisttoptags')) or is_table_empty(table('tracktoptags')):
        insert_items(db, 'item_tags.json', item_tag_insert)
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    # Insert users' top tracks if empty
    print('Inserting users top tracks... ', end='', flush=True)
    if is_table_empty(table('usertoptracks')):
        insert_items(db, 'top_tracks.json', top_item_insert,
                     table_name='usertoptracks', id_dict=track_ids, id_key='track_id')
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    # Insert users' top albums if empty
    print('Inserting users top albums... ', end='', flush=True)
    if is_table_empty(table('usertopalbums')):
        insert_items(db, 'top_albums.json', top_item_insert,
                     table_name='usertopalbums', id_dict=album_ids, id_key='album_id')
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    # Insert users' top artists if empty
    print('Inserting users top artists... ', end='', flush=True)
    if is_table_empty(table('usertopartists')):
        insert_items(db, 'top_artists.json', top_item_insert,
                     table_name='usertopartists', id_dict=artist_ids, id_key='artist_id')
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    # Insert users' recent tracks if empty
    print('Inserting users recent tracks... ', end='', flush=True)
    if is_table_empty(table('userrecenttracks')):
        insert_items(db, 'recent_tracks.json', track_timestamp_insert,
                     table_name='userrecenttracks', timestamp_col='listen_at')
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    # Insert users' loved tracks if empty
    print('Inserting users loved tracks... ', end='', flush=True)
    if is_table_empty(table('userlovedtracks')):
        insert_items(db, 'loved_tracks.json', track_timestamp_insert,
                     table_name='userlovedtracks', timestamp_col='love_at')
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')
