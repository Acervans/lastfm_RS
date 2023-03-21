import pandas as pd
import numpy as np

from sqlalchemy import create_engine, select, MetaData, Table, func
from sqlalchemy.orm import sessionmaker

db = create_engine(
    "postgresql://alumnodb:alumnodb@localhost:5432/lastfm_db", client_encoding="UTF-8")

metadata = MetaData()
metadata.reflect(bind=db)

def table(name) -> Table:
    return metadata.tables[name]

TAG = table('tag')
ALBUM = table('album')
ARTIST = table('artist')
TRACK = table('track')
USER = table('user_')

ALBUM_TAGS = table('albumtoptags')
ARTIST_TAGS = table('artisttoptags')
TRACK_TAGS = table('tracktoptags')
USER_TAGS = table('usertoptags') # Empty, use most frequent?

USER_TOP_ALBUMS = table('usertopalbums')
USER_TOP_ARTISTS = table('usertopartists')
USER_TOP_TRACKS = table('usertoptracks')

USER_RECENT_TRACKS = table('userrecenttracks')
USER_LOVED_TRACKS = table('userlovedtracks')

session = sessionmaker(db)

def normalize(col, kind: str = 'minmax', usecol: pd.Series = None):
    if usecol is None:
        usecol = col
    if kind == 'minmax':
        return (col - usecol.min()) / (usecol.max() - usecol.min())
    else:
        return (col - usecol.mean()) / usecol.std()


##########################################
###### ALL USER-TRACK RELATIONSHIPS ######
##########################################

def all_top_tracks():
    stmt = (select(USER.c.id, USER_TOP_TRACKS.c.track_id, USER_TOP_TRACKS.c.rank)
            .join(USER_TOP_TRACKS, USER.c.id == USER_TOP_TRACKS.c.user_id)
            .order_by(USER.c.id, USER_TOP_TRACKS.c.rank))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return pd.DataFrame(q, columns=['user_id', 'track_id', 'rank'])


def all_recent_tracks():
    stmt = (select(USER.c.id, USER_RECENT_TRACKS.c.track_id, USER_RECENT_TRACKS.c.listen_at)
            .join(USER_RECENT_TRACKS, USER.c.id == USER_RECENT_TRACKS.c.user_id)
            .order_by(USER.c.id, USER_RECENT_TRACKS.c.listen_at))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return pd.DataFrame(q, columns=['user_id', 'track_id', 'listen_at'])


def all_loved_tracks():
    stmt = (select(USER.c.id, USER_LOVED_TRACKS.c.track_id, USER_LOVED_TRACKS.c.love_at)
            .join(USER_LOVED_TRACKS, USER.c.id == USER_LOVED_TRACKS.c.user_id)
            .order_by(USER.c.id, USER_LOVED_TRACKS.c.love_at))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return pd.DataFrame(q, columns=['user_id', 'track_id', 'love_at'])


###########################
###### USER'S TRACKS ######
###########################

def user_recent_tracks(username):
    stmt = (select(USER_RECENT_TRACKS.c.track_id)
            .join(USER, USER.c.id == USER_RECENT_TRACKS.c.user_id)
            .filter(USER.c.username == username)
            .order_by(USER_RECENT_TRACKS.c.listen_at))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return pd.DataFrame(q, columns=['track_id'])['track_id']


def user_top_tracks(username):
    stmt = (select(USER_TOP_TRACKS.c.track_id)
            .join(USER, USER.c.id == USER_TOP_TRACKS.c.user_id)
            .filter(USER.c.username == username).
            order_by(USER_TOP_TRACKS.c.rank))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return pd.DataFrame(q, columns=['track_id'])['track_id']


def user_loved_tracks(username):
    stmt = (select(USER_LOVED_TRACKS.c.track_id)
            .join(USER, USER.c.id == USER_LOVED_TRACKS.c.user_id)
            .filter(USER.c.username == username)
            .order_by(USER_LOVED_TRACKS.c.love_at))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return pd.DataFrame(q, columns=['track_id'])['track_id']


###################################
###### TRACK'S NAME & ARTIST ######
###################################

def get_track_name(id):
    stmt = (select(TRACK.c.name, ARTIST.c.name)
            .join(ARTIST, ARTIST.c.id == TRACK.c.artist_id)
            .filter(TRACK.c.id == id))

    with session.begin() as s:
        q = s.execute(stmt).all()[0]
    return ' - '.join(q)


#####################################
###### TRACK + TRACK-ITEM TAGS ######
#####################################

def get_track_own_tags():
    stmt = (select(TRACK.c.id, TAG.c.name, TRACK_TAGS.c.rank)
            .join(TRACK_TAGS, TRACK_TAGS.c.track_id == TRACK.c.id)
            .join(TAG, TAG.c.id == TRACK_TAGS.c.tag_id)
            .order_by(TRACK.c.id, TRACK_TAGS.c.rank))

    with session.begin() as s:
        raw_track_tags = s.execute(stmt).all()
    return pd.DataFrame(raw_track_tags, columns=['track_id', 'tag', 'rank'])


def get_track_artist_tags():
    stmt = (select(TRACK.c.id, TAG.c.name, ARTIST_TAGS.c.rank)
            .join(ARTIST_TAGS, ARTIST_TAGS.c.artist_id == TRACK.c.artist_id)
            .join(TAG, TAG.c.id == ARTIST_TAGS.c.tag_id)
            .order_by(TRACK.c.id, ARTIST_TAGS.c.rank))

    with session.begin() as s:
        raw_track_tags = s.execute(stmt).all()
    return pd.DataFrame(raw_track_tags, columns=['track_id', 'tag', 'rank'])


def get_track_album_tags():
    stmt = (select(TRACK.c.id, TAG.c.name, ALBUM_TAGS.c.rank)
            .join(ALBUM_TAGS, ALBUM_TAGS.c.album_id == TRACK.c.album_id)
            .join(TAG, TAG.c.id == ALBUM_TAGS.c.tag_id)
            .order_by(TRACK.c.id, ALBUM_TAGS.c.rank))

    with session.begin() as s:
        raw_track_tags = s.execute(stmt).all()
    return pd.DataFrame(raw_track_tags, columns=['track_id', 'tag', 'rank'])


###################################
###### OVERALL TAG FREQUENCY ######
###################################

def get_tags_frequency():
    stmt1 = (select(TAG.c.name, func.count())
             .join(TRACK_TAGS, TRACK_TAGS.c.tag_id == TAG.c.id)
             .group_by(TAG.c.name))

    stmt2 = (select(TAG.c.name, func.count())
             .join(ARTIST_TAGS, ARTIST_TAGS.c.tag_id == TAG.c.id)
             .group_by(TAG.c.name))

    stmt3 = (select(TAG.c.name, func.count())
             .join(ALBUM_TAGS, ALBUM_TAGS.c.tag_id == TAG.c.id)
             .group_by(TAG.c.name))

    with session.begin() as s:
        tags_freq = s.execute(stmt1).all() + \
            s.execute(stmt2).all() + s.execute(stmt3).all()

    return pd.DataFrame(tags_freq, columns=['Tag', 'Frequency']).groupby('Tag').sum().sort_values('Frequency', ascending=False).reset_index()


#########################
###### ITEM'S VADS ######
#########################

def split_vad_stsc(df):
    # Separate VAD & StSc into different columns
    df[['V', 'A', 'D', 'StSc']] = pd.DataFrame(
    df['VAD'].apply(lambda x: x if x else [np.nan] * 4).tolist())

    # Drop column of lists
    df.drop(columns='VAD', inplace=True)
    
    
def get_item_vad(item_table, col_name):
    stmt = (select(item_table.c.id, item_table.c.name, item_table.c.vad))

    with session.begin() as s:
        item_vads = s.execute(stmt).all()
        
    item_vads = pd.DataFrame(item_vads, columns=[col_name, 'Name', 'VAD'])

    split_vad_stsc(item_vads)

    return item_vads


#############################
###### TRACK-ITEM VADS ######
#############################
    
def get_track_artist_vads():
    stmt = (select(TRACK.c.id, ARTIST.c.vad)
            .join(ARTIST, ARTIST.c.id == TRACK.c.artist_id))

    with session.begin() as s:
        artist_vads = s.execute(stmt).all()

    artist_vads = pd.DataFrame(artist_vads, columns=['Track', 'VAD'])
    split_vad_stsc(artist_vads)

    return artist_vads


def get_track_album_vads():
    stmt = (select(TRACK.c.id, ALBUM.c.vad)
            .join(ALBUM, ALBUM.c.id == TRACK.c.album_id))

    with session.begin() as s:
        album_vads = s.execute(stmt).all()
    
    album_vads = pd.DataFrame(album_vads, columns=['Track', 'VAD'])
    split_vad_stsc(album_vads)

    return album_vads
