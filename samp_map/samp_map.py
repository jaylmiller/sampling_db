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
    loc = geocoder.google('USA').latlng
    mymap = Map(
        identifier="map",
        lat=loc[0],
        lng=loc[1],
        zoom='4',
        maptype="TERRAIN",
        style="height:600px;width:100%;position:absolute;z-index:200;",
        markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png':[loc]}
    )
    return render_template('temp.html', mymap=mymap)

@app.route("/about")
def about():
    return render_template('about.html')

#@app.route('/stuff', optional--methods=['POST'])
#to do website:
#return render_template('template_name.html', optional--template_obj=var)
#to redirect
#return redirect(url_for(function))

if __name__ == '__main__':
    app.run()
