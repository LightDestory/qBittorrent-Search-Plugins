# VERSION: 1.0
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
import urllib.parse
from helpers import retrieve_url
from novaprinter import prettyPrinter


class pirateiro(object):
    url = 'https://pirateiro.com/'
    name = 'Pirateiro'
    supported_categories = {'all': '0'}
    max_pages = 10

    class HTMLParser:

        def __init__(self, url):
            self.url = url
            self.pageResSize = 0

        def feed(self, html):
            self.pageResSize = 0
            torrents = self.__findTorrents(html)
            resultSize = len(torrents)
            if resultSize == 0:
                return
            else:
                self.pageResSize = resultSize
            for torrent in range(resultSize):
                data = {
                    'link': torrents[torrent][0],
                    'name': torrents[torrent][1],
                    'size': torrents[torrent][2],
                    'seeds': torrents[torrent][3],
                    'leech': torrents[torrent][4],
                    'engine_url': self.url,
                    'desc_link': urllib.parse.unquote(torrents[torrent][0])
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            links = re.findall(r'<a class=\"card-link\".*?>.*?</a>', html)
            for a in links:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'<a class=\"card-link\".+?href=\"(.+?)\">.+?card-title\">(.+?)</h5>.+?size-badge\">([0-9\.\,]+ (TB|GB|MB|KB)).+?prog-green.+?>.+?([0-9]+).+?prog-red.+?>.+?([0-9]+).+?</a>',
                    a)
                if url_titles:
                    torrents.append([
                        urllib.parse.quote(url_titles.group(1)),
                        url_titles.group(2),
                        url_titles.group(3),
                        url_titles.group(5),
                        url_titles.group(6)
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
        for currPage in range(1, self.max_pages):
            url = '{0}search?query={1}&page={2}'.format(self.url, what, currPage)
            html = retrieve_url(url).replace("	", "").replace("\n", "").replace("\r", "")
            parser.feed(html)
            if parser.pageResSize <= 0:
                break
