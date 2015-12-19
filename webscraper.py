from bs4 import BeautifulSoup
import urllib


def get_trackpage_info(url):
    html = urllib.urlopen(str(url)).read()
    parse = BeautifulSoup(html, "html.parser")



if __name__ = "__main__":
    get_trackpage_info('http://www.whosampled.com/A$AP-Rocky/Peso/')
