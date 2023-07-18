import sqlalchemy

db = sqlalchemy.create_engine("postgresql://alumnodb:alumnodb@localhost:5432/lastfm_db",
                              client_encoding="UTF-8")

# Load table definitions from DDBB
metadata = sqlalchemy.MetaData()
metadata.reflect(bind=db)

# Mapping for table 'user'
USER = metadata.tables['user']

def get_user_id(username: str):
    stmt = sqlalchemy.select(USER.c.id).filter(USER.c.username == username)
    result = db.execute(stmt).first()
    return result