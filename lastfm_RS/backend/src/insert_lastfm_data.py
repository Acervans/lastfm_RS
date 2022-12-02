from sqlalchemy import create_engine, inspect, text, MetaData, select
import json

DATA_FOLDER = '../data/lastfm_data'
SQL_FOLDER = '../sql'
SEPARATOR = '\u254E'

db = create_engine(
    "postgresql://alumnodb:alumnodb@localhost:5432/lastfm_db", client_encoding="UTF-8")


def table(name):
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


def insert_items(engine, filename, insert_fun):
    with open(f"{DATA_FOLDER}/{filename}", encoding='utf-8') as f:
        if filename.endswith('.json'):
            items = json.load(f)
        else:
            items = [item.strip() for item in f.readlines()]

    with engine.connect() as conn:
        insert_fun(items, conn)


def format_vads(vads_float: list[float]):
    return "{" + ','.join([str(s) for s in vads_float]) + "}"


def tag_insert(tag_vads, conn):
    stmts = list()
    for tag, vads in tag_vads.items():
        vads = format_vads(vads)
        stmts.append({'name': tag, 'vad': vads})
    conn.execute(table('tag').insert(), stmts)


def artist_insert(item_vads, conn):
    stmts = list()
    artist_vads = item_vads["Artists"]
    for artist, vads in artist_vads.items():
        vads = format_vads(vads)
        stmts.append({'name': artist, 'vad': vads})
    conn.execute(table('artist').insert(), stmts)


def album_insert(item_vads, conn):
    stmts = list()
    album_vads = item_vads["Albums"]
    for album, vads in album_vads.items():
        vads = format_vads(vads)
        album_name, artist_name = album.split(SEPARATOR)
        # Query artist.id
        artist_id = conn.execute(select(table('artist').c.id).where(
            table('artist').c.name == artist_name)).one()[0]
        stmts.append({'name': album_name, 'artist_id': artist_id, 'vad': vads})
    conn.execute(table('album').insert(), stmts)


if __name__ == "__main__":
    global metadata

    # Create tables and relations using SQL script
    if not table_exists(db, 'track'):
        print('Creating tables... ', end='')
        setup_db(db)
        print('SUCCESS')

    # Load table definitions from lastfm_db
    metadata = MetaData()
    metadata.reflect(bind=db)

    # Insert tags if empty
    print('Inserting tags... ', end='')
    if is_table_empty(table('tag')):
        insert_items(db, 'tag_vads.json', tag_insert)
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    # Insert artists if empty
    print('Inserting artists... ', end='')
    if is_table_empty(table('artist')):
        insert_items(db, 'item_vads.json', artist_insert)
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')

    # Insert albums if empty
    print('Inserting albums... ', end='')
    if is_table_empty(table('album')):
        insert_items(db, 'item_vads.json', album_insert)
        print('SUCCESS')
    else:
        print('ALREADY_EXECUTED')
