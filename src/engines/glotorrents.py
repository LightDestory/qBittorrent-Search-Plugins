# VERSION: 1.6
# AUTHORS: LightDestory (https://github.com/LightDestory), BurningMop (https://github.com/BurningMop)

import re
from time import sleep

from helpers import retrieve_url
from novaprinter import prettyPrinter


class glotorrents(object):
    url = 'https://glodls.to/'
    name = 'GloTorrents'
    supported_categories = {'all': '0', 'movies': '1', 'tv': '41', 'music': '22', 'games': '10', 'anime': '28',
                            'software': '18'}

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
                    'desc_link': torrents[torrent][5]
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            trs = re.findall(
                r'<tr class=\'t-row\'><td class=\'ttable_col1\' align=\'center\' valign=\'middle\'>.+?</tr>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'title=\"(.+?)\".+?href=\"(.+?)\".+?</a>.+?align=\'center\'>.+?href=\"(magnet:.*?)\".+?([0-9\,\.]+ (TB|GB|MB|KB)).+?<font color=\'green\'><b>([0-9,]+)</b>.+?<font color=\'#[0-9a-zA-Z]{6}\'><b>([0-9,]+)</b>',
                    tr)
                if url_titles:
                    torrent_data = [
                        url_titles.group(3),
                        url_titles.group(1),
                        url_titles.group(4).replace(",", ""),
                        url_titles.group(6).replace(",", ""),
                        url_titles.group(7).replace(",", ""),
                        '{0}{1}'.format(self.url, url_titles.group(2)),
                    ]
                    torrents.append(torrent_data)
            return torrents

    def search(self, what, cat='all'):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        counter: int = 0
        while True:
            url = '{0}search_results.php?search={1}&cat={2}&page={3}'.format(self.url, what,
                                                                             self.supported_categories[cat], counter)
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            counter += 1
            sleep(5)
