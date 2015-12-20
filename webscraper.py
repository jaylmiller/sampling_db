from bs4 import BeautifulSoup
import urllib2
import Queue
import sys
from time import sleep
from db_interface import *

BASE_URL = "http://www.whosampled.com"
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def crawl(cnx, url, crawl_to, seen=[], samplers_seen=[]):
    """ This function populates our database on the fly.
    It does a breadth-first crawl of whosampled.com where the pages
    to crawl to next are determined by the get_trackpage_info function, and the
    info to populate the database is determined by the trackpage_info
    combined with calls to the echonest API (see get_echonest_data.py).

    Note that this function will go on for an extremely long time, the only way
    to stop it is by hitting control c in the terminal.

    Args:
        cnx - connection to mysql server (see db_interface.py)
        url - the current url being searched
        crawl_to - a queue of the links to search
        seen - an array of urls already seen (just to help some functions
            work faster)
        samplers_seen - another array of urls already seen (just to help some
            functions work faster)
    """

    print url.strip()
    print crawl_to.qsize()
    seen.append(url)
    try:
        artist, title, sample_info, links = get_trackpage_info(url,
                                                               samplers_seen)
        sleep(5)

    except KeyboardInterrupt:
        cnx.close()
        sys.exit(0)
    except:
        link = crawl_to.get()
        crawl(cnx, link, crawl_to, seen, samplers_seen)
        return
    try:
        add_song_and_its_samples(cnx, (artist, title), sample_info)
    except:
        print artist, title
        print sample_info
        cnx.close()
        sys.exit(0)
    for i in links:
        if i in seen:
            continue
        crawl_to.put(i)
    if not crawl_to.empty():
        link = crawl_to.get()
        crawl(cnx, link, crawl_to, seen, samplers_seen)


def get_trackpage_info(url, samplers_seen):
    """ Given a trackpage, i.e. a page for a track
    listing all it's samples. Get the info, artist name, song name,
    for that track, as well as all the tracks it samples, and also return
    a list of links to crawl to, which are all other tracks that also sample
    atleast 1 of the tracks the one on this page samples. """
    req = urllib2.Request(url, None, HEADERS)
    html = urllib2.urlopen(req).read()
    parse = BeautifulSoup(html, "html.parser")

    track_info = parse("div", "trackInfo")[0]
    title = track_info("h1")[0].contents[0].strip()
    artist = track_info("h2")[0]
    artist = artist("a")[0].contents[0].strip()

    samples = parse("ul", "list bordered-list")[0]
    samples = samples("li", "listEntry sampleEntry")
    sample_info = []
    links_out = []

    for sample in samples:
        track_name = sample("a", "trackName playIcon")[0]
        links_out.append(track_name["href"])
        name = track_name.contents[0].strip()
        sample_artist = sample("span", "trackArtist")[0]
        sample_artist = sample_artist("a")[0].contents[0].strip()
        sample_info.append((sample_artist, name))

    track_links = []
    for link in links_out:
        link2 = trackpage_from_samplepage(BASE_URL + link.strip())
        if link2 in samplers_seen:
            continue
        else:
            samplers_seen.append(link2)

        req = urllib2.Request(link2, None, HEADERS)
        html = urllib2.urlopen(req).read()
        parse = BeautifulSoup(html, "html.parser")
        section_header = parse("div", "sectionHeader")
        second_sec = False
        if len(section_header) == 1:
            section_header = section_header[0]
        else:
            section_header = section_header[1]
            second_sec = True

        if len(section_header.contents) == 5:
            req = urllib2.Request(link2 + "sampled", None, HEADERS)
            html = urllib2.urlopen(req).read()
            parse = BeautifulSoup(html, "html.parser")
            second_sec = False

        if second_sec:
            songs_list = parse("ul", "list bordered-list")[1]
        else:
            songs_list = parse("ul", "list bordered-list")[0]

        songs_list = songs_list("li", "listEntry sampleEntry")

        for songs in songs_list:
            sublink = songs("a")[0]
            sublink = sublink["href"]
            track_links.append(trackpage_from_samplepage(BASE_URL+sublink,
                                                         get_sampled=False))

    return artist, title, sample_info, list(set(track_links))


def trackpage_from_samplepage(url, get_sampled=True):
    """ Helper function just to get to the trackpage url from the
    page describing a specific sample. If get_sampled is true, the trackpage
    returned is the one for the song being sampled, and if false it returns
    the url for the song that is doing the sampling.
    """
    req = urllib2.Request(url, None, HEADERS)
    html = urllib2.urlopen(req).read()
    parse = BeautifulSoup(html, "html.parser")
    if get_sampled:
        trackinfo = parse("div", "sampleEntryBox")[1]
    else:
        trackinfo = parse("div", "sampleEntryBox")[0]

    track_name = trackinfo("a", "trackName")[0]
    link2 = track_name["href"]
    return BASE_URL + link2.strip()




if __name__ == "__main__":
    q = Queue.Queue()
    cnx = get_connection()
    crawl(cnx, 'http://www.whosampled.com/Kanye-West/Runaway/',
          q, [], [])
