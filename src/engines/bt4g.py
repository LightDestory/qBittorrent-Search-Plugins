# VERSION: 1.0
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
from datetime import datetime

from helpers import retrieve_url
from novaprinter import prettyPrinter


class bt4g(object):
    url = 'https://bt4gprx.com/'
    name = 'BT4G'
    supported_categories = {'all': '',
                            'movies': 'movie',
                            'music': 'audio',
                            'books': 'doc',
                            'software': 'app'
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
                r'<div class=\"list-group-item result-item\">.+?</div>', html)
            for tr in trs:
                url_titles = re.search(
                    r'..+?title=\"(.+?)\" href=\"(.+?)\".+?Creation Time: (.+?)<.+?Total Size.+?>([0-9\,\.]+(TB|GB|MB|KB)).+?seeders\">([0-9,]+).+?leechers\">([0-9,]+)',
                    tr)
                if url_titles:
                    timestamp = int(datetime.strptime(url_titles.group(3), "%Y-%m-%d").timestamp())
                    generic_url = '{0}{1}'.format(self.url[:-1], url_titles.group(2))
                    torrent_data = [
                        generic_url,
                        url_titles.group(1),
                        url_titles.group(4),
                        url_titles.group(6),
                        url_titles.group(7),
                        generic_url,
                        timestamp
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, download_url):
        torrent_page = retrieve_url(download_url)
        magnet_match = re.search(r'\"(magnet:.*?)\"', torrent_page)
        if magnet_match and magnet_match.groups():
            print('{0} {1}'.format(magnet_match.groups()[0], download_url))
        else:
            raise Exception('Error, please fill a bug report!')

    def search(self, what, cat='all'):
        cat = "" if cat == "all" else "&category={0}".format(self.supported_categories[cat])
        parser = self.HTMLParser(self.url)
        current_page = 1
        while True:
            url = '{0}search?q={1}{2}&p={3}'.format(self.url, what, cat, current_page)
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            current_page += 1
