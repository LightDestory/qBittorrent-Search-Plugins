# VERSION: 1.0
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
import urllib.parse
from helpers import retrieve_url
from novaprinter import prettyPrinter


class kickasstorrents(object):
    url = 'https://katcr.to/'
    name = 'Kickasstorrents'

    supported_categories = {'all': '', 'movies': 'movies', 'tv': 'tv', 'music': 'music', 'games': 'games', 'anime': 'anime', 'software': 'apps'}
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
            # Find all TR nodes with class odd or even
            trs = re.findall(r'<tr class=\"(?:odd|even)\">.*?</tr>', html)
            for tr in trs:
                url_titles = re.search(
                    r'.+?torrentname.+?href=\"(.+?)\".+?cellMainLink\">(.+?)<.+?nobr.+?>([0-9\.\,]+ (TB|GB|MB|KB)).+?green.+?>([0-9,]+).+?red.+?>([0-9,]+)',
                    tr)
                if url_titles:
                    torrents.append([
                        urllib.parse.quote('{0}{1}'.format(self.url, url_titles.group(1))),
                        url_titles.group(2),
                        url_titles.group(3).replace(",", ""),
                        url_titles.group(5).replace(",", ""),
                        url_titles.group(6).replace(",", "")
                    ])
            return torrents

    def download_torrent(self, info):
        torrent_page = retrieve_url(urllib.parse.unquote(info))
        magnet_match = re.search(r'\"(magnet:.*?)\"', torrent_page)
        if magnet_match and magnet_match.groups():
            print('{0} {1}'.format(magnet_match.groups()[0], info))
        else:
            raise Exception('Error, please fill a bug report!')

    def search(self, what, cat='all'):
        parser = self.HTMLParser(self.url)
        category = "" if cat == "all" else 'category/{0}/'.format(self.supported_categories[cat])
        for currPage in range(0, self.max_pages):
            url = '{0}search/{1}/{2}{3}/'.format(self.url, what, category, currPage)
            # Some replacements to format the html source
            html = retrieve_url(url).replace("	", "").replace("\n", "").replace("\r", "")\
                .replace("<strong class=\"red\">", "").replace("</strong>", "")
            parser.feed(html)
            if parser.pageResSize <= 0:
                break
