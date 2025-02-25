# VERSION: 1.2
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
import urllib.parse

from helpers import retrieve_url
from novaprinter import prettyPrinter


class pirateiro(object):
    url = 'https://pirateiro.com/'
    name = 'Pirateiro'
    supported_categories = {
        'all': '0',
        'anime': '2',
        'games': '3',
        'movies': '1',
        'music': '4',
        'software': '6',
        'tv': '5'
    }
    max_pages = 10

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
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            links = re.findall(r'<a href=\"(.+?)\".+?<h6.+?>(.+?)</h6>.+?(\d+)</span>.+?(\d+)</span>.+?</a>', html)
            for a in links:
                    torrents.append([
                        a[0],
                        a[1],
                        -1,
                        a[2],
                        a[3],
                        a[0]
                    ])
            return torrents

    def download_torrent(self, info):
        torrent_page = retrieve_url(urllib.parse.unquote(info))
        magnet_match = re.search(r'\"(magnet:.*?)\"', torrent_page)
        if magnet_match and magnet_match.groups():
            print('{0} {1}'.format(magnet_match.groups()[0], info))
        else:
            dl_link = re.search(r'<a class=\"btn-down\".+?href=\"(.+?)\".+>.+?</a>', torrent_page.replace("	", "").replace("\n", "").replace("\r", ""))
            if dl_link and dl_link.groups():
                self.download_torrent(dl_link.groups()[0].replace("kickasstorrents", "katcr"))
            else:
                raise Exception('Error, please fill a bug report!')

    def search(self, what, cat='all'):
        what = what.replace('%20', '+')
        parser = self.HTMLParser(self.url)
        cat_str = "" if cat == 'all' else '&category={0}'.format(self.supported_categories[cat])
        for currPage in range(1, self.max_pages):
            url = '{0}search?query={1}&page={2}{3}'.format(self.url, what, currPage, cat_str)
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
