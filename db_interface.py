import mysql.connector
from config import MYSQL_INFO
from get_echonest_data import *


def get_connection():
    return mysql.connector.connect(**MYSQL_INFO)


def add_song_and_its_samples(cnx, song_info, sample_info):
    try:
        artist_id, song_id = artist_and_song_id(song_info[0], song_info[1])
    except:
        return

    samplingsong_id = song_id
    if update_song_table(cnx, song_id, artist_id, song_info[1]) is False:
        return
    if update_artist_table(cnx, artist_id, song_info[0]) is False:
        return

    samples = [True for i in sample_info]
    for i, sample in enumerate(sample_info):
        try:
            artist_id, song_id = artist_and_song_id(sample[0], sample[1])
            samples[i] = song_id
        except:
            samples[i] = False
            continue

        if update_song_table(cnx, song_id, artist_id, sample[1]) is False:
            samples[i] = False
            continue
        if update_artist_table(cnx, artist_id, sample[0]) is False:
            samples[i] = False
            continue

    for s in samples:
        if s is False:
            continue
        update_sampled_table(cnx, samplingsong_id, s)


def update_song_table(cnx, song_id, artist_id, title):
    if check_in_db_with_pk(cnx, song_id, "audio_md5", "song"):
        return
    try:
        info = tuple(song_info(song_id))
    except:
        return False
    info = list(info)
    if info[-1] is None:
        info[-1] = 'NULL'
    cursor = cnx.cursor()
    info = tuple((song_id, title, artist_id))+tuple(info)

    add_song = ("INSERT INTO song "
                "(audio_md5, title, artist_id, tempo, s_key, mode, danceability, year) "
                "VALUES (\"%s\", \"%s\", \"%s\", %s, \"%s\", \"%s\", %s, %s)") % info
    cursor.execute(add_song)
    cnx.commit()
    cursor.close()


def update_sampled_table(cnx, song_id, sampled_id):
    cursor = cnx.cursor()
    add_sampled = ("INSERT INTO sampled(song_md5, sampled_md5) "
                   "VALUES (\"%s\", \"%s\" )") % (song_id, sampled_id)
    cursor.execute(add_sampled)
    cnx.commit()
    cursor.close()


def update_genre_table(cnx, artist_id, genre):
    cursor = cnx.cursor()
    add_genre = ("INSERT INTO genre(artist_id, genre) "
                 "VALUES (\"%s\", \"%s\" )") % (artist_id, genre)
    cursor.execute(add_genre)
    cnx.commit()
    cursor.close()

def update_artist_table(cnx, artist_id, name):
    if check_in_db_with_pk(cnx, artist_id, "artist_id", "artist"):
        return
    try:
        location, year_start, year_end, genres_strings = artist_info(artist_id)
    except:
        return False

    cursor = cnx.cursor()
    if year_end is None:
        year_end = 'NULL'

    info = (artist_id, name, location, year_start, year_end)

    add_song = ("INSERT INTO artist "
                "(artist_id, name, location, year_start, year_end) "
                "VALUES (\"%s\", \"%s\", \"%s\", %s, %s)") % info

    cursor.execute(add_song)
    cnx.commit()
    cursor.close()

    for g in genres_strings:
        update_genre_table(cnx, artist_id, g)


def check_in_db_with_pk(cnx, pk_value, pk_name, table):
    cursor = cnx.cursor()
    query = ("SELECT %s pk FROM %s having pk like \"%s\" ") % (pk_name,
                                                               table,
                                                               pk_value)
    cursor.execute(query)
    rows = cursor.fetchall()
    if len(rows) > 0:
        cursor.close()
        return True
    else:
        cursor.close()
        return False


if __name__ == "__main__":
    cnx = get_connection()
    add_song_and_its_samples(cnx, ('Kendrick Lamar', 'Money Trees'),
                             [('Beach House', 'Silver Soul'),
                             ('Kendrick Lamar', 'Cartoon and Cereal')])
