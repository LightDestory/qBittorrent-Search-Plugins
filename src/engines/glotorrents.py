# VERSION: 1.5
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

    # GloTorrents' search divided into pages, so we are going to set a limit on how many pages to read
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
                count = 0
            for torrent in range(resultSize):
                count = count + 1
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


    def download_torrent(self, info):
        print('{0} {1}'.format(info, info))

    def search(self, what, cat='all'):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        for currPage in range(0, self.max_pages):
            url = '{0}search_results.php?search={1}&cat={2}&page={3}'.format(self.url, what, self.supported_categories[cat], currPage)
            # Some replacements to format the html source
            html = retrieve_url(url).replace("	", "").replace("\n", "").replace("\r", "")
            parser.feed(html)
            sleep(2)
            if parser.pageResSize <= 0:
                break
