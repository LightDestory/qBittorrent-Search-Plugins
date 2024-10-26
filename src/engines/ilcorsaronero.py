# VERSION: 1.8
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
from helpers import retrieve_url
from novaprinter import prettyPrinter


class ilcorsaronero(object):
    url = 'https://ilcorsaronero.link/'
    name = 'Il Corsaro Nero'
    supported_categories = {'all': '',
                            'movies': 'film',
                            'music': 'musica',
                            'games': 'giochi',
                            'anime': 'animazione',
                            'books': 'libri',
                            'software': 'software',
                            'tv': 'serie-tv'}

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
                    'pub_date': torrents[torrent][6]
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            # Find all TR nodes with class odd or odd2
            trs = re.findall(r'(<tr>.+?</tr>)', html)
            for tr in trs[1:]: # Skip the first TR node because it's the header
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'href=\"(.+?)\">(.+?)</a>.+?green.+?>.*?([0-9]+).*?red.*?>.*?([0-9]+).+?([0-9\.\,]+ (?:TiB|GiB|MiB|KiB|B)).+?timestamp=\"(.+?)\"',
                    tr)
                if url_titles:
                    generic_url = '{0}{1}'.format(self.url[:-1], url_titles.group(1))
                    torrents.append([
                        generic_url,
                        url_titles.group(2),
                        url_titles.group(5),
                        url_titles.group(3),
                        url_titles.group(4),
                        generic_url,
                        url_titles.group(6)
                    ])
            return torrents

    def download_torrent(self, info):
        torrent_page = ' '.join(retrieve_url(info).split())
        magnet_match = re.search(r'href=\"(magnet:.*?)\"', torrent_page)
        if magnet_match and magnet_match.groups():
            magnet_str = magnet_match.groups()[0]
            print(magnet_str + " " + magnet_str)
        else:
            raise Exception('Error, please fill a bug report!')

    def search(self, what, cat='all'):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        counter: int = 1
        filter = '&cat={0}'.format(self.supported_categories[cat])
        while True:
            url = '{0}search?q={1}&cat={2}&page={3}'.format(self.url, what, filter, counter)
            # Some replacements to format the html source
            html = ' '.join(retrieve_url(url).split())
            parser.feed(html)
            if parser.noTorrents:
                break
            counter += 1
