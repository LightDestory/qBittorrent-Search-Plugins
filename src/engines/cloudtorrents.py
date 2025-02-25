# VERSION: 1.0
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
from datetime import datetime
from urllib.parse import quote, unquote

from helpers import retrieve_url
from novaprinter import prettyPrinter


class cloudtorrents(object):
    url = 'https://cloudtorrents.com/'
    name = 'CloudTorrents'

    supported_categories = {
        'all': '0',
        'anime': '1',
        'books': '3',
        'games': '4',
        'movies': '5',
        'music': '6',
        'software': '2',
        'tv': '8'
    }
    class HTMLParser:

        def __init__(self, url):
            self.url = url
            self.noTorrents = False

        def feed(self, html):
            self.noTorrents = False
            torrents = self.__findTorrents(html)
            resultSize = len(torrents)
            if resultSize == 0:
                self.noTorrents = True
                return
            for torrent in range(resultSize):
                data = {
                    'link': torrents[torrent][0],
                    'name': torrents[torrent][1],
                    'size': torrents[torrent][2],
                    'seeds': torrents[torrent][3],
                    'leech': torrents[torrent][4],
                    'engine_url': self.url,
                    'desc_link': torrents[torrent][5],
                    'pub_date': torrents[torrent][6]
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            trs = re.findall(
                r'<tr>.+?</tr>', html)[1:]
            for tr in trs:
                url_titles = re.search(
                    r'.+?href=\"(.+?)\".+?data-discover=\".+?b>(.+?)</b.+?(magnet:\?.+?)\".+?([0-9\,\.]+ (TB|GB|MB|KB)).+?Uploaded.+?=\"(.+?)\".+?Se\">([0-9,]+).+?Le\">([0-9,]+)',
                    tr)
                if url_titles:
                    timestamp = int(datetime.strptime(url_titles.group(6), "%d %b, %Y %H:%M").timestamp())
                    generic_url = '{0}{1}'.format(self.url[:-1], url_titles.group(1))
                    torrent_data = [
                        quote(url_titles.group(3)),
                        url_titles.group(2),
                        url_titles.group(4),
                        url_titles.group(7),
                        url_titles.group(8),
                        generic_url,
                        timestamp
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, info):
        unquoted_magnet = unquote(info)
        print(unquoted_magnet + " " + unquoted_magnet)

    def search(self, what, cat='all'):
        what = what.replace('%20', '+')
        parser = self.HTMLParser(self.url)
        cat = "" if cat == "all" else "&torrent_type={0}".format(self.supported_categories[cat])
        current_page = 0
        while True:
            url = '{0}search?offset={1}&query={2}{3}'.format(self.url, current_page*25, what, cat)
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            current_page += 1
