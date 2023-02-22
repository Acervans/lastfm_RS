CREATE TABLE IF NOT EXISTS Album (
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
  name varchar NOT NULL,
  artist_id integer NOT NULL,
  VAD float8 [],
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS AlbumTopTags (
  album_id integer NOT NULL,
  tag_id integer NOT NULL,
  rank integer NOT NULL,
  PRIMARY KEY (album_id, tag_id)
);

CREATE TABLE IF NOT EXISTS Artist (
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
  name varchar NOT NULL UNIQUE,
  VAD float8 [],
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ArtistTopTags (
  artist_id integer NOT NULL,
  tag_id integer NOT NULL,
  rank integer NOT NULL,
  PRIMARY KEY (artist_id, tag_id)
);

CREATE TABLE IF NOT EXISTS Tag (
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
  name varchar NOT NULL UNIQUE,
  VAD float8 [],
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Track (
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
  name varchar NOT NULL,
  artist_id integer NOT NULL,
  album_id integer,
  VAD float8 [],
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS TrackTopTags (
  track_id integer NOT NULL,
  tag_id integer NOT NULL,
  rank integer NOT NULL,
  PRIMARY KEY (track_id, tag_id)
);

CREATE TABLE IF NOT EXISTS User_ (
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
  username varchar NOT NULL UNIQUE,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS UserLovedTracks (
  user_id integer NOT NULL,
  track_id integer NOT NULL,
  love_at timestamp,
  PRIMARY KEY (user_id, track_id, love_at)
);

CREATE TABLE IF NOT EXISTS UserRecentTracks (
  user_id integer NOT NULL,
  track_id integer NOT NULL,
  listen_at timestamp,
  PRIMARY KEY (user_id, track_id, listen_at)
);

CREATE TABLE IF NOT EXISTS UserTopAlbums (
  user_id integer NOT NULL,
  album_id integer NOT NULL,
  rank integer NOT NULL,
  PRIMARY KEY (user_id, album_id)
);

CREATE TABLE IF NOT EXISTS UserTopArtists (
  user_id integer NOT NULL,
  artist_id integer NOT NULL,
  rank integer NOT NULL,
  PRIMARY KEY (user_id, artist_id)
);

CREATE TABLE IF NOT EXISTS UserTopTags (
  user_id integer NOT NULL,
  tag_id integer NOT NULL,
  rank integer NOT NULL,
  PRIMARY KEY (user_id, tag_id)
);

CREATE TABLE IF NOT EXISTS UserTopTracks (
  user_id integer NOT NULL,
  track_id integer NOT NULL,
  rank integer NOT NULL,
  PRIMARY KEY (user_id, track_id)
);

ALTER TABLE
  UserLovedTracks
ADD
  CONSTRAINT FK_User_TO_UserLovedTracks FOREIGN KEY (user_id) REFERENCES User_ (id),
ADD
  CONSTRAINT FK_Track_TO_UserLovedTracks FOREIGN KEY (track_id) REFERENCES Track (id);

ALTER TABLE
  UserTopArtists
ADD
  CONSTRAINT FK_User_TO_UserTopArtists FOREIGN KEY (user_id) REFERENCES User_ (id),
ADD
  CONSTRAINT FK_Artist_TO_UserTopArtists FOREIGN KEY (artist_id) REFERENCES Artist (id);

ALTER TABLE
  UserTopAlbums
ADD
  CONSTRAINT FK_User_TO_UserTopAlbums FOREIGN KEY (user_id) REFERENCES User_ (id),
ADD
  CONSTRAINT FK_Album_TO_UserTopAlbums FOREIGN KEY (album_id) REFERENCES Album (id);

ALTER TABLE
  UserTopTags
ADD
  CONSTRAINT FK_User_TO_UserTopTags FOREIGN KEY (user_id) REFERENCES User_ (id),
ADD
  CONSTRAINT FK_Tag_TO_UserTopTags FOREIGN KEY (tag_id) REFERENCES Tag (id);

ALTER TABLE
  UserRecentTracks
ADD
  CONSTRAINT FK_User_TO_UserRecentTracks FOREIGN KEY (user_id) REFERENCES User_ (id),
ADD
  CONSTRAINT FK_Track_TO_UserRecentTracks FOREIGN KEY (track_id) REFERENCES Track (id);

ALTER TABLE
  UserTopTracks
ADD
  CONSTRAINT FK_User_TO_UserTopTracks FOREIGN KEY (user_id) REFERENCES User_ (id),
ADD
  CONSTRAINT FK_Track_TO_UserTopTracks FOREIGN KEY (track_id) REFERENCES Track (id);

ALTER TABLE
  Album
ADD
  CONSTRAINT FK_Artist_TO_Album FOREIGN KEY (artist_id) REFERENCES Artist (id),
ADD
  CONSTRAINT UQ_Album_Artist UNIQUE (name, artist_id);

ALTER TABLE
  Track
ADD
  CONSTRAINT FK_Artist_TO_Track FOREIGN KEY (artist_id) REFERENCES Artist (id),
ADD
  CONSTRAINT FK_Album_TO_Track FOREIGN KEY (album_id) REFERENCES Album (id),
ADD
  CONSTRAINT UQ_Track_Artist UNIQUE (name, artist_id);

ALTER TABLE
  ArtistTopTags
ADD
  CONSTRAINT FK_Artist_TO_ArtistTopTags FOREIGN KEY (artist_id) REFERENCES Artist (id),
ADD
  CONSTRAINT FK_Tag_TO_ArtistTopTags FOREIGN KEY (tag_id) REFERENCES Tag (id);

ALTER TABLE
  TrackTopTags
ADD
  CONSTRAINT FK_Tag_TO_TrackTopTags FOREIGN KEY (tag_id) REFERENCES Tag (id),
ADD
  CONSTRAINT FK_Track_TO_TrackTopTags FOREIGN KEY (track_id) REFERENCES Track (id);

ALTER TABLE
  AlbumTopTags
ADD
  CONSTRAINT FK_Tag_TO_AlbumTopTags FOREIGN KEY (tag_id) REFERENCES Tag (id),
ADD
  CONSTRAINT FK_Album_TO_AlbumTopTags FOREIGN KEY (album_id) REFERENCES Album (id);