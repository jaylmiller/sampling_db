# Sample_Map (600.315/415 Final Project)

## Jay Miller (600.415), Trevor Aron (600.315)

**1** N/A

**2** For this project, we created a database that holds info on artists and their songs. The primary relation in this database is one called 'sampled' which maps a primary song, to other songs which are sampled (https://en.wikipedia.org/wiki/Sampling_(music)) by the primary song. Other info on artists and songs that are stored in the database are artist location, years active, and metrics on the song such as estimated tempo, and a 'danceability' scale. The main report produced is a map which when given an artist, will show that artist on the map as well as show the locations of all the artists that that artist sampled (or vice versa).

**3** N/A

**4** The database was populated by creating a webscraper that scraped the website www.whosampled.com to get information on which songs sampled others. Then for each sampling relation found, information on each song, and the song's artist, were collected using the API from www.echonest.com. The webscraper traverses www.whosampled.com by inspecting one song and its samples, and then adding any song that also sampled a song in the previous song's samples to a queue of links to look at next (so it is searching breadth-first).
The webscraper.py, db_interface.py, and get_echonest_data.py scripts are the 3 python modules used for information extraction/database population.

**5** N/A

**6** The website can be reached at http://52.32.119.97:5000/ 

To run the website, write a config.py file containing a dictionary called MYSQL_INFO, and put all your database information there. (We didn't wan't to upload our database password to github!). This should look like {'user': username, 'password': password, 'host': host name, 'database':final}. Put this in the samp_map folder. Also make sure you have created the db, ran procedures.sql, and have populated the db with some values. Then, install the following python packages: geocoder, mysql-connector-python, flask, flask-googlemaps. Then, run the command

$python samp_map/samp_map.py

Your flask app should be up and running!

**7** Our two major areas of specialization were extraction of real data from online sources and a specialized forms-based interface with sophisticated report generation.

**8** One limitation of our database is that it is fairly small, and only contains a small subset of data on artists songs and which songs sampled other songs. This is because we discovered that our webcrawler would get our IP's blocked from www.whosampled.com if it made too many requests, and thus we had to make our webcrawler work at a slower-than-optimal speed. If we had started the information extraction process earlier on, our database would have been larger and the information would have been more reflective of the real music world. Another limitation is that the web interface is fairly slow, because some of the queries being made are fairly complex. Given more time, this could have been improved by doing some query optimization.

**9** ![alt text](https://raw.githubusercontent.com/jaym910/sampling_db/master/preview1.png "Preview 1")

![alt text](https://raw.githubusercontent.com/jaym910/sampling_db/master/preview2.png "Preview 2")

**10** See database_def.sql for our database specification.

**11** Stored SQL procedures are in procedures.sql. The db_interface.py module has methods which interface with our database using the python-mysql-connector library. These methods are used to populate the database. *Add in where SQL stuff is called in the website?*
