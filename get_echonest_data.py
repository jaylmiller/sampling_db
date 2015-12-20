from config import EN_API_KEY
import urllib
import simplejson as json


integer_to_string_key_mapping = ['C', 'C#', 'D', 'Eb',
                                 'E', 'F', 'F#', 'G',
                                 'Ab', 'A', 'Bb', 'B']

def artist_and_song_id(artist, title):
    base_url = 'http://developer.echonest.com/api/v4/song/search?api_key='
    url = base_url + EN_API_KEY + '&format=json&results=1&artist='
    artist = artist.replace(' ', '%20')
    title = title.replace(' ', '%20')
    url = url + artist + '&title=' + title
    j = urllib.urlopen(url).read()
    parsed_json = json.loads(j)
    msg = parsed_json['response']['status']['message']
    if msg != 'Success':
        return None
    song = parsed_json['response']['songs'][0]
    artist_id = song['artist_id']
    song_id = song['id']
    return artist_id, song_id


def artist_info(artist_id):
    base_url = 'http://developer.echonest.com/api/v4/artist/profile?api_key='
    url = base_url + EN_API_KEY + '&id=' + artist_id
    url = url + '&format=json&bucket=genre'
    url = url + '&bucket=artist_location&bucket=years_active'
    j = urllib.urlopen(url).read()
    parsed_json = json.loads(j)
    msg = parsed_json['response']['status']['message']
    if msg != 'Success':
        return None
    artist = parsed_json['response']['artist']
    name = artist['name']
    genres_json = artist['genres']
    genres_strings = []
    for g in genres_json:
        genres_strings.append(g['name'])
    location = artist['artist_location']['location']
    year_start = artist['years_active'][0]['start']
    if 'end' in artist['years_active'][-1]:
        year_end = artist['years_active'][-1]['end']
    else:
        year_end = None
    return location, year_start, year_end, genres_strings


def song_info(song_id):
    base_url = 'http://developer.echonest.com/api/v4/song/profile?api_key='
    url = base_url + EN_API_KEY + '&format=json&id='
    url = url + song_id
    url = url + '&bucket=audio_summary&bucket=id:spotify-WW&bucket=tracks'
    j = urllib.urlopen(url).read()
    parsed_json = json.loads(j)
    msg = parsed_json['response']['status']['message']
    if msg != 'Success':
        return None

    song = parsed_json['response']['songs'][0]

    audio_summary = song['audio_summary']
    s_key = audio_summary['key']
    s_key = integer_to_string_key_mapping[int(s_key)]
    tempo = audio_summary['tempo']
    mode = audio_summary['mode']
    if int(mode) == 1:
        mode = 'major'
    else:
        mode = 'minor'
    danceability = audio_summary['danceability']

    try:
        track = song['tracks'][0]
        year = track['album_date']
        year = year.split('-')[0]
    except:
        year = None

    return tempo, s_key, mode, danceability, year

if __name__ == '__main__':
    a_id, s_id = artist_and_song_id('Radiohead', 'Karma Police')
    print a_id, s_id
    print song_info(s_id)
