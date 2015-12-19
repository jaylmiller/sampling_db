from bs4 import BeautifulSoup
import urllib
import Queue
import sys
from time import sleep

BASE_URL = "http://www.whosampled.com"


def get_trackpage_info(url, samplers_seen):
    html = urllib.urlopen(str(url)).read()
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
        print link2
        if link2 in samplers_seen:
            continue
        else:
            samplers_seen.append(link2)

        html = urllib.urlopen(link2)
        parse = BeautifulSoup(html, "html.parser")
        section_header = parse("div", "sectionHeader")
        second_sec = False
        if len(section_header) == 1:
            section_header = section_header[0]
        else:
            section_header = section_header[1]
            second_sec = True

        if len(section_header.contents) == 5:
            html = urllib.urlopen(link2 + "sampled")
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

    return title, artist, sample_info, list(set(track_links))


def trackpage_from_samplepage(url, get_sampled=True):
    html = urllib.urlopen(url.strip())
    parse = BeautifulSoup(html, "html.parser")
    if get_sampled:
        trackinfo = parse("div", "sampleEntryBox")[1]
    else:
        trackinfo = parse("div", "sampleEntryBox")[0]

    track_name = trackinfo("a", "trackName")[0]
    link2 = track_name["href"]
    return BASE_URL + link2.strip()

def crawl(url, crawl_to, seen, samplers_seen):
    print url.strip()
    print crawl_to.qsize()
    seen.append(url)
    try:
        info = get_trackpage_info(url, samplers_seen)
        sleep(2)

    except KeyboardInterrupt:
        sys.exit(0)
    except:
        link = crawl_to.get()
        crawl(link, crawl_to, seen, samplers_seen)
        return

    for i in info[3]:
        if i in seen:
            continue
        crawl_to.put(i)
    if not crawl_to.empty():
        link = crawl_to.get()
        crawl(link, crawl_to, seen, samplers_seen)

if __name__ == "__main__":
    q = Queue.Queue()
    crawl('http://www.whosampled.com/Drake/Pound-CakeParis-Morton-Music-2/',
          q, [], [])
