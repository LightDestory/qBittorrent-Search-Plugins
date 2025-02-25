# VERSION: 1.0
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
from datetime import datetime
from urllib.parse import quote, unquote

from helpers import retrieve_url
from novaprinter import prettyPrinter


class bitsearch(object):
    url = 'https://bitsearch.to/'
    name = 'BitSearch'
    supported_categories = {'all': '',
                            'movies': '&category=1&subcat=2',
                            'music': '&category=7',
                            'games': '&category=6&subcat=1',
                            'software': '&category=5&subcat=1'
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
                r'<li class=\"card search-result my-2\">.+?</li>', html)
            for tr in trs:
                url_titles = re.search(
                    r'.+?href=\"(.+?)\".+?token.+?>(.+?)<.+?Size.+?>([0-9\,\.]+ (TB|GB|MB|KB)).+?color.+?>([0-9,]+).+?color.+?>([0-9,]+).+?Date.+?>(.+?)<.+?(magnet.+?)\"',
                    tr)
                if url_titles:
                    timestamp = int(datetime.strptime(url_titles.group(7), "%b %d, %Y").timestamp())
                    generic_url = '{0}{1}'.format(self.url[:-1], url_titles.group(1))
                    torrent_data = [
                        quote(url_titles.group(8)),
                        url_titles.group(2),
                        url_titles.group(3),
                        url_titles.group(5),
                        url_titles.group(6),
                        generic_url,
                        timestamp
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, download_url):
        unquoted_magnet = unquote(download_url)
        print(unquoted_magnet + " " + unquoted_magnet)

    def search(self, what, cat='all'):
        parser = self.HTMLParser(self.url)
        current_page = 1
        while True:
            url = '{0}search?q={1}&page={2}{3}'.format(self.url, what, current_page, self.supported_categories[cat])
            # Some replacements to format the html source
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            current_page += 1
