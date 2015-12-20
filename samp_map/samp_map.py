#imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map
import mysql.connector
import geocoder

#configuration
DEBUG       = True
SECRET_KEY  = '13aront'

#create app
app = Flask(__name__)
app.config.from_object(__name__)
GoogleMaps(app)

def connect_db():
    return mysql.connector.connect(user='trevoraron', password='dinn3r$12',\
            host='db-final-project.cqpqwl7k3umb.us-west-2.rds.amazonaws.com', \
            database='final')

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/", methods=['GET', 'POST'])
def mapview():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        cursor = g.db.cursor()
        #Check if artist name exists
        name = request.form['artist-name']
        cursor.callproc('GetArtist', [name])
        for result in cursor.stored_results():
            num = result.fetchall()
        if len(num) < 1:
            cursor.close()
            return render_template('bad_artist.html', name=name)

        loc = geocoder.google('USA').latlng
        #Get info
        if request.form['option'] == 'whosamples':
            cursor.callproc('GetSongsWhoSample', [name])
            for result in cursor.stored_results():
                songs = result.fetchall()
            locs, info = get_markers_and_info(songs, True)
        else:
            cursor.callproc('GetSongsSampled', [name])
            for result in cursor.stored_results():
                songs = result.fetchall()
            locs, info = get_markers_and_info(songs, False)
        cursor.close()
        #make map
        mymap = Map(
            identifier="map",
            lat=loc[0],
            lng=loc[1],
            zoom='4',
            maptype="TERRAIN",
            style="height:600px;width:100%;position:absolute;z-index:200;",
            infobox=info,
            markers={ 'http://maps.google.com/mapfiles/ms/icons/green-dot.png':locs}
        )
        return render_template('main.html', mymap=mymap)

def get_markers_and_info(songs, who_sampled):
    print 'get_markers_and_info'
    info = []
    locs = []
    for a1_id, a1_loc, s1_title, a2_loc, a2_name, s2_title, s2_year in songs:
        if who_sampled:
            temp_str = "<p> " + str(s2_title) + " by " + str(a2_name) + "</p>"\
                       "<p>Sampled: " + str(s1_title) + "</p>"
        else:
            temp_str = "<p> " + str(s2_title) + " by " + str(a2_name) + "</p>"\
                       "<p>Was Sampled In: " + str(s1_title) + "</p>"
        print temp_str
        loc = geocoder.google(str(a2_loc)).latlng
        print loc
        info.append(temp_str)
        locs.append(loc)
    return locs, info

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/stats")
def stats():
    cursor = g.db.cursor()
    #Call all the stored procedures
    cursor.callproc('GenreMostSampled')
    for result in cursor.stored_results():
        g_most_sampled = result.fetchall()
    cursor.callproc('GenreMostSamples')
    for result in cursor.stored_results():
        g_most_samples = result.fetchall()
    cursor.callproc('ArtistMostSamples')
    for result in cursor.stored_results():
        a_most_samples = result.fetchall()
    cursor.callproc('ArtistMostSampled')
    for result in cursor.stored_results():
        a_most_sampled = result.fetchall()
    cursor.callproc('SongMostSamples')
    for result in cursor.stored_results():
        s_most_samples = result.fetchall()
    cursor.callproc('SongMostSampled')
    for result in cursor.stored_results():
        s_most_sampled = result.fetchall()
    cursor.callproc('MostDance')
    for result in cursor.stored_results():
        most_dance = result.fetchall()
    cursor.close()
    return render_template('stats.html', g_most_sampled = str(g_most_sampled[0][0]), \
                                         g_most_samples = str(g_most_samples[0][0]), \
                                         a_most_samples = str(a_most_samples[0][0]), \
                                         a_most_sampled = str(a_most_sampled[0][0]), \
                                         s_most_samples = str(s_most_samples[0][0]), \
                                         s_most_sampled = str(s_most_sampled[0][0]), \
                                         most_dance_s   = str(most_dance[0][0]),  \
                                         most_dance_a   = str(most_dance[0][1]),  \
                                         most_dance_d   = str(most_dance[0][2]))
#@app.route('/stuff', optional--methods=['POST'])
#to do website:
#return render_template('template_name.html', optional--template_obj=var)
#to redirect
#return redirect(url_for(function))

if __name__ == '__main__':
    app.run()
