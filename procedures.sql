/*
Trevor Aron
Jay Miller
*/
USE final

DELIMITER //

/* Returns info of all songs who sample songs made by artist_name 
   DEPRECATED --- WAY TO SLOW*/
DROP PROCEDURE IF EXISTS GetSongsWhoSample //
CREATE PROCEDURE GetSongsWhoSample(IN artist_name VARCHAR(30))
BEGIN
  SELECT a1.artist_id, a1.location, s1.title, a2.location, a2.name, s2.title, s2.year
  FROM song as s1, song as s2, artist as a1, artist as a2, sampled as samp
  WHERE a1.name LIKE artist_name 
        AND s1.artist_id LIKE a1.artist_id
        AND s1.audio_md5 LIKE samp.sampled_md5
        AND s2.audio_md5 LIKE samp.song_md5
        AND s2.artist_id LIKE a2.artist_id; 
END;
//

/* Returns info of all songs who sample songs made by artist_name*/
DROP PROCEDURE IF EXISTS FGetSongsWhoSample //
CREATE PROCEDURE FGetSongsWhoSample(IN artist_name VARCHAR(30))
BEGIN
  SELECT q1.title, a2.location, a2.name, s2.title
  FROM (SELECT s.title, samp.song_md5
        FROM song as s, artist as a, sampled as samp
        WHERE a.name LIKE artist_name
              AND s.artist_id = a.artist_id
              AND samp.sampled_md5 = s.audio_md5) as q1, song as s2, artist as a2
  WHERE q1.song_md5 LIKE s2.audio_md5
        AND s2.artist_id LIKE a2.artist_id;
END;
//

/* Returns info of all songs sampled by artist_name
   DEPRECATED --- To Slow!!! */
DROP PROCEDURE IF EXISTS GetSongsSampled //
CREATE PROCEDURE GetSongsSampled(IN artist_name VARCHAR(30))
BEGIN
  SELECT a1.artist_id, a1.location, s1.title, a2.location, a2.name, s2.title, s2.year
  FROM song as s1, song as s2, artist as a1, artist as a2, sampled as samp
  WHERE a1.name LIKE artist_name 
        AND s1.artist_id LIKE a1.artist_id
        AND s1.audio_md5 LIKE samp.song_md5
        AND s2.audio_md5 LIKE samp.sampled_md5
        AND s2.artist_id LIKE a2.artist_id; 
END;
//


/* Returns info of all songs sampled by artist_name*/
DROP PROCEDURE IF EXISTS FGetSongsSampled //
CREATE PROCEDURE FGetSongsSampled(IN artist_name VARCHAR(30))
BEGIN
  SELECT q1.title, a2.location, a2.name, s2.title
  FROM (SELECT s.title, samp.sampled_md5
        FROM song as s, artist as a, sampled as samp
        WHERE a.name LIKE artist_name
              AND s.artist_id = a.artist_id
              AND samp.song_md5 = s.audio_md5) as q1, song as s2, artist as a2
  WHERE q1.sampled_md5 LIKE s2.audio_md5
        AND s2.artist_id LIKE a2.artist_id;
END;
//

/* Returns average danceability of songs who sample those by artist name */
DROP PROCEDURE IF EXISTS WhoSampleAvgDance //
CREATE PROCEDURE WhoSampleAvgDance(IN artist_name VARCHAR(30))
BEGIN
  SELECT a1.artist_id, AVG(s2.danceability)
  FROM song as s1, song as s2, artist as a1, sampled as samp
  WHERE a1.name LIKE artist_name
        AND s1.artist_id LIKE a1.artist_id
        AND s1.audio_md5 LIKE samp.sampled_md5
        AND s2.audio_md5 LIKE samp.song_md5
  GROUP BY a1.artist_id;
END;
//

/* Returns average danceability of songs sampled by artist name */
DROP PROCEDURE IF EXISTS SampledAvgDance //
CREATE PROCEDURE SampledAvgDance(IN artist_name VARCHAR(30))
BEGIN
  SELECT a1.artist_id, AVG(s2.danceability)
  FROM song as s1, song as s2, artist as a1, sampled as samp
  WHERE a1.name LIKE artist_name
        AND s1.artist_id LIKE a1.artist_id
        AND s1.audio_md5 LIKE samp.song_md5
        AND s2.audio_md5 LIKE samp.sampled_md5
  GROUP BY a1.artist_id;
END;
//

/* Returns most common genre of songs who sample those by artist name
   DEPRECATED --- don't use this takes too long
                  also just plain doesn't work lol */
DROP PROCEDURE IF EXISTS WhoSampledGenre //
CREATE PROCEDURE WhoSampledGenre(IN artist_name VARCHAR(30))
BEGIN
  SELECT count.artist_id, count.genre, MAX(oc)
  FROM (SELECT a1.artist_id, g.genre, COUNT(*) as oc
        FROM genre as g, artist as a1, artist as a2, song as s1, song as s2, sampled as samp
        WHERE a1.name LIKE artist_name
              AND s1.artist_id LIKE a1.artist_id
              AND s1.audio_md5 LIKE samp.sampled_md5
              AND s2.audio_md5 LIKE samp.song_md5
              AND s2.artist_id LIKE a2.artist_id
              AND g.artist_id LIKE a2.artist_id
        GROUP BY a1.artist_id, g.genre) as count
  GROUP BY count.artist_id;
END;
//

/* Returns most common genre of songs who sample those by artist name
   420BlazinFast version */
DROP PROCEDURE IF EXISTS FWhoSampledGenre //
CREATE PROCEDURE FWhoSampledGenre(IN artist_name VARCHAR(30))
BEGIN
  SELECT count.genre, count.count
  FROM (SELECT g.genre, count(*) as count
        FROM (SELECT samp.song_md5
              FROM song as s, artist as a, sampled as samp
              WHERE a.name LIKE artist_name
              AND s.artist_id = a.artist_id
              AND s.audio_md5 = samp.sampled_md5) as q1, song as s1, artist as a1, genre as g
        WHERE q1.song_md5 = s1.audio_md5
        AND   a1.artist_id = s1.artist_id
        AND   g.artist_id = a1.artist_id
        GROUP BY g.genre) as count
  WHERE count.count in  (
  SELECT max(count.count)
  FROM (SELECT g.genre, count(*) as count
        FROM (SELECT samp.song_md5
              FROM song as s, artist as a, sampled as samp
              WHERE a.name LIKE artist_name
              AND s.artist_id = a.artist_id
              AND s.audio_md5 = samp.sampled_md5) as q1, song as s1, artist as a1, genre as g
        WHERE q1.song_md5 = s1.audio_md5
        AND   a1.artist_id = s1.artist_id
        AND   g.artist_id = a1.artist_id
        GROUP BY g.genre) as count);
END;
//

/* Returns most common genre of songs that are sampled by artist name
   DEPRECATED --- TO SLOW!!!
                  also gives incorrect answer */
DROP PROCEDURE IF EXISTS SampledGenre //
CREATE PROCEDURE SampledGenre(IN artist_name VARCHAR(30))
BEGIN
  SELECT count.artist_id, count.genre, MAX(oc)
  FROM (SELECT a1.artist_id, g.genre, COUNT(*) as oc
        FROM genre as g, artist as a1, artist as a2, song as s1, song as s2, sampled as samp
        WHERE a1.name LIKE artist_name
              AND s1.artist_id LIKE a1.artist_id
              AND s1.audio_md5 LIKE samp.song_md5
              AND s2.audio_md5 LIKE samp.sampled_md5
              AND s2.artist_id LIKE a2.artist_id
              AND g.artist_id LIKE a2.artist_id
        GROUP BY a1.artist_id, g.genre) as count
  GROUP BY count.artist_id;
END;
//


/* Returns most common genre of songs that are sampled by artist_name
   420BlazinFast version */
DROP PROCEDURE IF EXISTS FSampledGenre //
CREATE PROCEDURE FSampledGenre(IN artist_name VARCHAR(30))
BEGIN
  SELECT count.genre, count.count
  FROM (SELECT g.genre, count(*) as count
        FROM (SELECT samp.sampled_md5
              FROM song as s, artist as a, sampled as samp
              WHERE a.name LIKE artist_name
              AND s.artist_id = a.artist_id
              AND s.audio_md5 = samp.song_md5) as q1, song as s1, artist as a1, genre as g
        WHERE q1.sampled_md5 = s1.audio_md5
        AND   a1.artist_id = s1.artist_id
        AND   g.artist_id = a1.artist_id
        GROUP BY g.genre) as count
  WHERE count.count in  (
  SELECT max(count.count)
  FROM (SELECT g.genre, count(*) as count
        FROM (SELECT samp.sampled_md5
              FROM song as s, artist as a, sampled as samp
              WHERE a.name LIKE artist_name
              AND s.artist_id = a.artist_id
              AND s.audio_md5 = samp.song_md5) as q1, song as s1, artist as a1, genre as g
        WHERE q1.sampled_md5 = s1.audio_md5
        AND   a1.artist_id = s1.artist_id
        AND   g.artist_id = a1.artist_id
        GROUP BY g.genre) as count);
END;
//


/* Returns song that has the highest average danceability in songs
   that sample it */
DROP PROCEDURE IF EXISTS MostDance //
CREATE PROCEDURE MostDance()
BEGIN
  SELECT av.title, av.name, MAX(av.av_dance)
  FROM (SELECT a1.name, s1.title, AVG(s2.danceability) as av_dance
        FROM song as s1, song as s2, artist as a1, sampled as samp
        WHERE s1.artist_id = a1.artist_id
              AND s1.audio_md5 = samp.sampled_md5
              AND s2.audio_md5 = samp.song_md5
        GROUP BY a1.name, s1.title) as av;
END;
//

/* Returns genre that samples the most */
DROP PROCEDURE IF EXISTS GenreMostSamples //
CREATE PROCEDURE GenreMostSamples()
BEGIN
  SELECT mx.genre
  FROM (SELECT count.genre, MAX(count.n_samps)
        FROM (SELECT g.genre, COUNT(*) as n_samps
              FROM genre as g, song as s, sampled as samp
              WHERE g.artist_id = s.artist_id
                    AND s.audio_md5 = samp.song_md5
              GROUP BY g.genre) as count) as mx;
END;
//

/* Returns genre that is sampled the most */
DROP PROCEDURE IF EXISTS GenreMostSampled //
CREATE PROCEDURE GenreMostSampled()
BEGIN
  SELECT mx.genre
  FROM (SELECT count.genre, MAX(count.n_samps)
        FROM (SELECT g.genre, COUNT(*) as n_samps
              FROM genre as g, song as s, sampled as samp
              WHERE g.artist_id = s.artist_id
                    AND s.audio_md5 = samp.sampled_md5
              GROUP BY g.genre) as count) as mx;
END;
//


/* Returns artist that is sampled the most */
DROP PROCEDURE IF EXISTS ArtistMostSampled //
CREATE PROCEDURE ArtistMostSampled()
BEGIN
  SELECT mx.name
  FROM (SELECT count.name, MAX(count.n_samps)
        FROM (SELECT a.name, COUNT(*) as n_samps
              FROM artist as a, song as s, sampled as samp
              WHERE a.artist_id = s.artist_id
                    AND s.audio_md5 = samp.sampled_md5
              GROUP BY a.name) as count) as mx;
END;
//


/* Returns artist that samples the most */
DROP PROCEDURE IF EXISTS ArtistMostSamples //
CREATE PROCEDURE ArtistMostSamples()
BEGIN
  SELECT mx.name
  FROM (SELECT count.name, MAX(count.n_samps)
        FROM (SELECT a.name, COUNT(*) as n_samps
              FROM artist as a, song as s, sampled as samp
              WHERE a.artist_id = s.artist_id
                    AND s.audio_md5 = samp.song_md5
              GROUP BY a.name) as count) as mx;
END;
//

/* Returns song with the most samples */
DROP PROCEDURE IF EXISTS SongMostSamples //
CREATE PROCEDURE SongMostSamples()
BEGIN
  SELECT mx.title
  FROM (SELECT count.title, MAX(count.n_samps)
        FROM (SELECT s.title, COUNT(*) as n_samps
              FROM song as s, sampled as samp
              WHERE s.audio_md5 = samp.song_md5
              GROUP BY s.title) as count) as mx;
END;
//


/* Returns song that is sampled the most */
DROP PROCEDURE IF EXISTS SongMostSampled //
CREATE PROCEDURE SongMostSampled()
BEGIN
  SELECT mx.title
  FROM (SELECT count.title, MAX(count.n_samps)
        FROM (SELECT s.title, COUNT(*) as n_samps
              FROM song as s, sampled as samp
              WHERE s.audio_md5 = samp.sampled_md5
              GROUP BY s.title) as count) as mx;
END;
//

DROP PROCEDURE IF EXISTS GetArtist //
CREATE PROCEDURE GetArtist(IN artist_name VARCHAR(30))
BEGIN
  SELECT *
  FROM artist
  WHERE name LIKE artist_name;
END;
//
DELIMITER ;
