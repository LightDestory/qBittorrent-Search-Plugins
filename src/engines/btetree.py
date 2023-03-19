# VERSION: 1.3
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
import urllib.parse
from helpers import retrieve_url
from novaprinter import prettyPrinter


class btetree(object):
    url = "https://bt.etree.org/"
    name = "bt.etree"
    supported_categories = {'all': '0'}

    class HTMLParser:

        def __init__(self, url):
            self.url = url
            self.noTorrents = False

        def feed(self, html):
            self.noTorrents = False
            torrents = self.__findTorrents(html)
            if len(torrents) == 0:
                self.noTorrents = True
                return
            for torrent in range(len(torrents)):
                data = {
                    'link': torrents[torrent][0],
                    'name': torrents[torrent][1],
                    'size': torrents[torrent][2],
                    'seeds': torrents[torrent][3],
                    'leech': torrents[torrent][4],
                    'engine_url': self.url,
                    'desc_link': torrents[torrent][5],
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            trs = re.findall(
                r'<tr align=\"right\" bgcolor=\"#ffffff\">.+?</tr>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'<tr.+?details_link.+?href=\"(.+?)\".+?<b>(.+?)</b>.+?href=\"(.+?)\".+?([0-9\,\.]+ (TB|GB|MB|KB)).+?seeders\">([0-9,]+).+?leechers\">([0-9,]+)',
                    tr)
                if url_titles:
                    torrents.append([
                        '{0}{1}'.format(self.url, urllib.parse.quote(url_titles.group(3))),
                        url_titles.group(2),
                        url_titles.group(4).replace(",", ""),
                        url_titles.group(6).replace(",", ""),
                        url_titles.group(7).replace(",", ""),
                        '{0}{1}'.format(self.url, url_titles.group(1))
                    ])
            return torrents

    def search(self, what, cat='all'):
        what = what.replace('%20', '+')
        parser = self.HTMLParser(self.url)
        counter = 0
        while True:
            url = '{0}index.php?searchzzzz={1}&cat=0&page={2}'.format(self.url, what, 50 * counter)
            html = retrieve_url(url).replace("	", "").replace("\n", "").replace("\r", "")
            parser.feed(html)
            if parser.noTorrents:
                break
            counter += 1
