#VERSION: 1.1
# AUTHORS: LightDestory (https://github.com/LightDestory)

from helpers import retrieve_url
from novaprinter import prettyPrinter
import re, urllib.parse


class ettv(object):
    url = 'https://www.ettvcentral.com/'
    name = 'ETTV'
    # TLDR; It is safer to force an 'all' research.
    # IlCorsaroNero's categories are very specific, qBittorent does not provide enought categories to implement a good filtering.
    # For example, qBittorrent provides only a generic 'games' category meanwhile the website uses: pc, xbox and playstation.
    supported_categories = {'all': '0'}
    # ETTV's search divided into pages, so we are going to set a limit on how many pages to read
    max_pages = 8

    class HTMLParser():

        def __init__(self, url):
            self.url = url
            self.pageResSize = 0

        def formatTemplate(self):
            return {'link': '-1', 'name': '-1', 'size': '-1', 'seeds': '-1', 'leech': '-1', 'engine_url': self.url, 'desc_link': '-1'}

        def feed(self, html):
            self.pageResSize = 0
            torrents = self.findTorrents(html)
            resultSize = len(torrents)
            if(resultSize == 0):
                return
            else:
                self.pageResSize = resultSize
            for torrent in range(resultSize):
                data = self.formatTemplate()
                data['link'] = torrents[torrent][0]
                data['name'] = torrents[torrent][1]
                data['size'] = torrents[torrent][2]
                data['seeds'] = torrents[torrent][3]
                data['leech'] = torrents[torrent][4]
                prettyPrinter(data)

        def findTorrents(self, html):
            torrents = []
            # Find all TR nodes with class odd or odd2
            trs = re.findall(r'<tr class=\'\'>.*?</tr>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'<tr class=\'\'>.+?torrent\" href=\"/(.+?)\".+?<b>(.+?)</b></a>.+?([0-9\.\,]+ (TB|GB|MB|KB)).+?green\'><b>([0-9,]+).+?a50707\'><b>([0-9,]+)', tr)
                if url_titles:
                    torrents.append([urllib.parse.quote('{0}{1}'.format(self.url, url_titles.group(1))), url_titles.group(
                        2), url_titles.group(3).replace(",",""), url_titles.group(5), url_titles.group(6)])
            return torrents

    def download_torrent(self, info):
        torrent_page = retrieve_url(urllib.parse.unquote(info))
        magnet_match = re.search(
            r'a href=\"(.?magnet:.*?)\"', torrent_page)
        if magnet_match and magnet_match.groups():
            print('{0} {1}'.format(magnet_match.groups()[0], info))
        else:
            raise Exception('Error, please fill a bug report!')

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        what = what.replace('%20', '+')
        parser = self.HTMLParser(self.url)
        for currPage in range(0, self.max_pages):
            url = '{0}torrents-search.php?search={1}&sort=seeders&cat=0&order=desc&lang=0&page={2}'.format(
                self.url, what, currPage)
            html = retrieve_url(url).replace(
                "	", "").replace("\n", "").replace("\r", "")
            parser.feed(html)
            # if there are no results exit
            if parser.pageResSize <= 0:
                break
