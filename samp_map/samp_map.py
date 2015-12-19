#imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import mysql.connector

#configuration
DEBUG       = True
SECRET_KEY  = '13aront'
USERNAME    = 'admin'
PASSWORD    = 'default'

#create app
app = Flask(__name__)
app.config.from_object(__name__)

if __name__ == '__main__':
    app.run()

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

#@app.route('/stuff', optional--methods=['POST'])
#to do website:
#return render_template('template_name.html', optional--template_obj=var)
#to redirect
#return redirect(url_for(function))
