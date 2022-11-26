import sqlalchemy as sa

DATA_FOLDER = '../data/lastfm_data'
SQL_FOLDER = '../sql'

db = sa.create_engine("postgresql://alumnodb:alumnodb@localhost:5432/lastfm_db", echo=True)

def table_exists(engine, name):
    ins = sa.inspect(engine)
    return ins.dialect.has_table(engine.connect(), name)

def setup_db(engine):
    with engine.connect() as conn:
        with open(f"{SQL_FOLDER}/LastFM_DB.sql") as f:
            query = sa.text(f.read())
            conn.execute(query)

def insert_tags():
    pass

def insert_artists():
    pass

def insert_albums():
    pass

def insert_tracks():
    pass

def insert_users():
    pass

if __name__ == "__main__":
    # Create tables and relations using SQL script
    if not table_exists(db, 'track'):
        setup_db(db)
        
    insert_tags()