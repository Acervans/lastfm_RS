from collections import Counter
import pandas as pd
import numpy as np
import json

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
USER_TAGS = table('usertoptags')  # Empty, use most frequent?

USER_TOP_ALBUMS = table('usertopalbums')
USER_TOP_ARTISTS = table('usertopartists')
USER_TOP_TRACKS = table('usertoptracks')

USER_RECENT_TRACKS = table('userrecenttracks')
USER_LOVED_TRACKS = table('userlovedtracks')

TABLES = [
    TAG, ALBUM, ARTIST, TRACK, USER,
    ALBUM_TAGS, ARTIST_TAGS, TRACK_TAGS, USER_TAGS,
    USER_TOP_ALBUMS, USER_TOP_ARTISTS, USER_TOP_TRACKS,
    USER_RECENT_TRACKS, USER_LOVED_TRACKS
]

session = sessionmaker(db)


def normalize(col, kind: str = 'minmax', usecol: pd.Series = None):
    if usecol is None:
        usecol = col
    if kind == 'minmax':
        return (col - usecol.min()) / (usecol.max() - usecol.min())
    else:
        return (col - usecol.mean()) / usecol.std()


################################
###### TABLE AS DATAFRAME ######
################################

def get_table_df(table_name: str):
    return pd.read_sql_table(table_name, db.connect())


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


def merge_tracks(track_dfs: list, min_playcount: int = None) -> pd.DataFrame:
    """ Merges DataFrames with format [user, track, rating, timestamp<Optional>]

    Args:
        track_dfs (list): List of track DataFrames to merge
        min_playcount (int | None): Minimum playcount for a track to be added.

    Returns:
        DataFrame: Merged tracks
    """
    merged_track_ratings = pd.concat(track_dfs, ignore_index=True)
    merged_track_ratings['rating'] = merged_track_ratings['rating'].astype(
        np.float32)

    # Discard tracks with less than min_playcount total listens
    if min_playcount is not None:
        listen_count = merged_track_ratings['track_id'].value_counts()
        discard_ids = listen_count[listen_count < min_playcount].index
        merged_track_ratings = merged_track_ratings.loc[~merged_track_ratings.track_id.isin(
            discard_ids)]

    # Sort by desc. rating and drop duplicates while keeping highest rating
    final_ratings = merged_track_ratings.sort_values('rating', ascending=False).drop_duplicates(
        ['user_id', 'track_id'], keep='first').sort_values(['user_id', 'track_id']).reset_index(drop=True)

    return final_ratings


###########################
###### USER'S ITEMS ######
###########################

def get_user_id(username):
    stmt = (select(USER.c.id)
            .filter(USER.c.username == username))

    with session.begin() as s:
        q = s.execute(stmt).first()
    return q[0] if q else None


def user_recent_tracks(username, id_only=False):
    stmt = (select(USER_RECENT_TRACKS.c.track_id, USER_RECENT_TRACKS.c.listen_at)
            .join(USER, USER.c.id == USER_RECENT_TRACKS.c.user_id)
            .filter(USER.c.username == username)
            .order_by(USER_RECENT_TRACKS.c.listen_at))

    with session.begin() as s:
        q = s.execute(stmt).all()
    df = pd.DataFrame(q, columns=['track_id', 'listen_at'])
    return df['track_id'] if id_only else df


def user_top_tracks(username, id_only=False):
    stmt = (select(USER_TOP_TRACKS.c.track_id, USER_TOP_TRACKS.c.rank)
            .join(USER, USER.c.id == USER_TOP_TRACKS.c.user_id)
            .filter(USER.c.username == username).
            order_by(USER_TOP_TRACKS.c.rank))

    with session.begin() as s:
        q = s.execute(stmt).all()
    df = pd.DataFrame(q, columns=['track_id', 'rank'])
    return df['track_id'] if id_only else df


def user_loved_tracks(username, id_only=False):
    stmt = (select(USER_LOVED_TRACKS.c.track_id, USER_LOVED_TRACKS.c.love_at)
            .join(USER, USER.c.id == USER_LOVED_TRACKS.c.user_id)
            .filter(USER.c.username == username)
            .order_by(USER_LOVED_TRACKS.c.love_at))

    with session.begin() as s:
        q = s.execute(stmt).all()
    df = pd.DataFrame(q, columns=['track_id', 'love_at'])
    return df['track_id'] if id_only else df


def user_top_artists(username):
    stmt = (select(USER_TOP_ARTISTS.c.artist_id)
            .join(USER, USER.c.id == USER_TOP_ARTISTS.c.user_id)
            .filter(USER.c.username == username)
            .order_by(USER_TOP_ARTISTS.c.rank))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return pd.DataFrame(q, columns=['artist_id'])['artist_id']


def user_top_albums(username):
    stmt = (select(USER_TOP_ALBUMS.c.album_id)
            .join(USER, USER.c.id == USER_TOP_ALBUMS.c.user_id)
            .filter(USER.c.username == username)
            .order_by(USER_TOP_ALBUMS.c.rank))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return pd.DataFrame(q, columns=['album_id'])['album_id']

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
####### DATABASE STATISTICS #######
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


def get_tables_count() -> dict:
    with session.begin() as s:
        tables_counts = [
            (table.name, s.execute(
                select([func.count()]).select_from(table)).first()[0])
            for table in TABLES
        ]

    return dict(tables_counts)

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

###################################
########## GENERAL UTILS ##########
###################################

def get_username(id):
    stmt = (select(USER.c.username)
            .filter(USER.c.id == id))

    with session.begin() as s:
        return s.execute(stmt).one()[0]

def get_track_name(id):
    stmt = (select(TRACK.c.name, ARTIST.c.name)
            .join(ARTIST, ARTIST.c.id == TRACK.c.artist_id)
            .filter(TRACK.c.id == id))

    with session.begin() as s:
        q = s.execute(stmt).all()[0]
    return ' - '.join(q)


def get_item(table, id):
    stmt = (select(['*']).filter(table.c.id == str(id)))

    try:
        with session.begin() as s:
            return s.execute(stmt).one()
    except Exception as e:
        return None


def get_track(id):
    return get_item(TRACK, id)


def get_artist(id):
    return get_item(ARTIST, id)


def get_album(id):
    return get_item(ALBUM, id)


def get_track_tags(id):
    stmt = (select(TAG.c.name)
            .join(TRACK_TAGS, TRACK_TAGS.c.tag_id == TAG.c.id)
            .join(TRACK, TRACK.c.id == TRACK_TAGS.c.track_id)
            .filter(TRACK.c.id == id)
            .order_by(TRACK_TAGS.c.rank))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return np.array(q).flatten().tolist()


def get_artist_tags(id):
    stmt = (select(TAG.c.name)
            .join(ARTIST_TAGS, ARTIST_TAGS.c.tag_id == TAG.c.id)
            .join(ARTIST, ARTIST.c.id == ARTIST_TAGS.c.artist_id)
            .filter(ARTIST.c.id == id)
            .order_by(ARTIST_TAGS.c.rank))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return np.array(q).flatten().tolist()


def get_album_tags(id):
    stmt = (select(TAG.c.name)
            .join(ALBUM_TAGS, ALBUM_TAGS.c.tag_id == TAG.c.id)
            .join(ALBUM, ALBUM.c.id == ALBUM_TAGS.c.album_id)
            .filter(ALBUM.c.id == id)
            .order_by(ALBUM_TAGS.c.rank))

    with session.begin() as s:
        q = s.execute(stmt).all()
    return np.array(q).flatten().tolist()


def search_tracks(track_query='', artist_query='', album_query='', cutoff=10):
    stmt = select(TRACK.c.id)

    if track_query:
        stmt = stmt.filter(TRACK.c.name.ilike(f'%{track_query}%'))
    if artist_query:
        stmt = (stmt.join(ARTIST, ARTIST.c.id == TRACK.c.artist_id)
                .filter(ARTIST.c.name.ilike(f'%{artist_query}%')))
    if album_query:
        stmt = (stmt.join(ALBUM, ALBUM.c.id == TRACK.c.album_id)
                .filter(ALBUM.c.name.ilike(f'%{album_query}%')))
    stmt = stmt.limit(cutoff)

    with session.begin() as s:
        q = s.execute(stmt).all()
    return np.array(q).flatten().tolist()


def get_track_context(track_id):
    unique_track = get_track(track_id)[:-1]
    if not unique_track:
        return None
    track_id, track_name, artist_id, album_id = unique_track
    _, artist, _ = get_artist(artist_id)
    album = ''
    if album_id:
        _, album, _, _ = get_album(album_id)
    return track_id, track_name, artist, album


def get_db_user_data(username: str,
                     filepath: str = None,
                     use_items: dict = None,
                     include_tracks=False,
                     include_artists=False,
                     include_albums=False,
                     include_tags=False,
                     tracks_limit=None,
                     artists_limit=None,
                     albums_limit=None,
                     tags_limit=None) -> dict:

    data = use_items or dict()
    item_tags = data.get('ITEM_TAGS') or {
        'Artists': dict(),
        'Albums': dict(),
        'Tracks': dict()
    }

    # Check if user still exists
    if not get_user_id(username):
        return {'ERROR': f'User {username} does not exist in database'}

    data['USER'] = username

    # ---------------------- Tracks ----------------------

    if include_tracks:

        # ----------- Loved Tracks -----------

        loved_tracks = list()
        for t, love_at in user_loved_tracks(username).values[:tracks_limit]:
            unique_track = get_track_context(t)
            if not unique_track:
                continue
            _, track, artist, album = unique_track

            # Name Artist Album Timestamp
            loved_tracks.append(
                (track, artist, album, str(love_at.timestamp())))
            item_tags['Tracks'][unique_track] = list()

        data['LOVED_TRACKS'] = loved_tracks

        # ----------- Recent Tracks -----------

        recent_tracks = list()
        for t, listen_at in user_recent_tracks(username).values[:tracks_limit]:
            unique_track = get_track_context(t)
            if not unique_track:
                continue
            _, track, artist, album = unique_track

            # Name Artist Album Timestamp
            recent_tracks.append(
                (track, artist, album, str(listen_at.timestamp())))
            item_tags['Tracks'][unique_track] = list()

        data['RECENT_TRACKS'] = recent_tracks

        # ----------- Top Tracks -----------

        top_tracks = list()
        for t in user_top_tracks(username, id_only=True).values[:tracks_limit]:
            unique_track = get_track_context(t)
            if not unique_track:
                continue
            _, track, artist, album = unique_track

            # Name Artist Album
            top_tracks.append((track, artist, album))
            item_tags['Tracks'][unique_track] = list()

        data['TOP_TRACKS'] = top_tracks

    # ---------------------- Artists ----------------------

    if include_artists:

        top_artists = list()
        for artist_id in user_top_artists(username)[:artists_limit]:
            artist = get_artist(artist_id)

            top_artists.append(artist[1])
            item_tags['Artists'][artist[:-1]] = list()

        data['TOP_ARTISTS'] = top_artists

    # ---------------------- Albums ----------------------

    if include_albums:

        top_albums = list()
        for album_id in user_top_albums(username)[:albums_limit]:
            album = get_album(album_id)
            artist_name = get_artist(album[2])[1]
            album_name = (album[1], artist_name)

            top_albums.append(album_name)
            item_tags['Albums'][(album[0],) + album_name] = list()

        data['TOP_ALBUMS'] = top_albums

    # ---------------------- Tags ----------------------

    if include_tags:
        tags_count = Counter()

        for item_type in item_tags:
            for item in list(item_tags[item_type].keys()):
                match item_type:
                    case 'Tracks':
                        fun = get_track_tags
                    case 'Artists':
                        fun = get_artist_tags
                    case 'Albums':
                        fun = get_album_tags
                tags = fun(item[0])[:tags_limit]

                # Assign tags to current item
                item_tags[item_type][item[1:]] = tags
                del item_tags[item_type][item]
                # Update unique Tags counts
                tags_count.update(tags)

        for item_type in item_tags.keys():
            item_tags[item_type] = list(item_tags[item_type].items())

        data['TAGS_COUNT'] = tags_count.most_common(None)

    data['ITEM_TAGS'] = item_tags

    if filepath:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return data
