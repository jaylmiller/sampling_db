DROP DATABASE IF EXISTS final;
CREATE DATABASE final;

USE final;

DROP TABLE IF EXISTS song;
CREATE TABLE song(
    audio_md5       VARCHAR(50) NOT NULL,
    title           VARCHAR(30),
    artist_id       VARCHAR(30),
    tempo           FLOAT,
    s_key           VARCHAR(10),
    mode            VARCHAR(10),
    danceability    FLOAT,
    year            INT,
    PRIMARY KEY (audio_md5)
);

DROP TABLE IF EXISTS artist;
CREATE TABLE artist(
    artist_id       VARCHAR(30) NOT NULL,
    name            VARCHAR(30),
    location        VARCHAR(100),
    year_start      INT,
    year_end        INT,
    PRIMARY KEY (artist_id)
);

DROP TABLE IF EXISTS sampled;
CREATE TABLE sampled(
    song_md5        VARCHAR(50) NOT NULL,
    sampled_md5     VARCHAR(50) NOT NULL
);

DROP TABLE IF EXISTS genre;
CREATE TABLE genre(
    artist_id       VARCHAR(30) NOT NULL,
    genre           VARCHAR(30)
);
