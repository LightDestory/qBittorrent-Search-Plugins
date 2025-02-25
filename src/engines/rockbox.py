# VERSION: 1.1
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re

from helpers import retrieve_url
from novaprinter import prettyPrinter


class rockbox(object):
    url = 'https://rawkbawx.rocks/'
    name = 'RockBox'
    """ 
        TLDR; It is safer to force an 'all' research
        RockBox's categories are very specific for music-type
        qBittorrent does not provide enough categories to implement a good filtering.
    """
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
                    'desc_link': torrents[torrent][5]
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            trs = re.findall(r'<TR><td align=\"center\".*?</TR>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'.+?HREF=\"(.+?)\".+?details\: ?(.+?)\">.+?rating.+?HREF=(.+?)>.+?([0-9\,\.]+ (TB|GB|MB|KB)).+?peers details\">([0-9,]+).+?peers details\">([0-9,]+).+?',
                    tr)
                if url_titles:
                    torrents.append([
                        '{0}{1}'.format(self.url, url_titles.group(3)),
                        url_titles.group(2),
                        url_titles.group(4).replace(",", ""),
                        url_titles.group(6).replace(",", ""),
                        url_titles.group(7).replace(",", ""),
                        '{0}{1}'.format(self.url, url_titles.group(1))
                    ])
            return torrents

    def search(self, what, cat='all'):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        counter: int = 0
        while True:
            url = '{0}torrents.php?active=0&search={1}&options=0&order=data&page={2}'.format(self.url, what, counter)
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            counter += 1
