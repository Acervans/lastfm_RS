import sqlalchemy

db = sqlalchemy.create_engine("postgresql://alumnodb:alumnodb@localhost:5432/lastfm_db")
conn = db.connect()

def insert_tags():
    pass