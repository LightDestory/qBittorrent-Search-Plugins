# VERSION: 1.2
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
import urllib.parse

from helpers import retrieve_url
from novaprinter import prettyPrinter


class glotorrents(object):
    url = 'https://www.gtdb.to/'
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
                    'desc_link': urllib.parse.unquote(torrents[torrent][0])
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            trs = re.findall(
                r'<tr class=\'t-row\'><td class=\'ttable_col1\' align=\'center\' valign=\'middle\'>.+?</tr>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'.+?title.+?href=\"(.+?)\"><b>(.+?)</b></a>.+?align=\'center\'>([0-9\,\.]+ (TB|GB|MB|KB)).+?<font color=\'green\'><b>([0-9,]+)</b>.+?<font color=\'#[0-9a-zA-Z]{6}\'><b>([0-9,]+)</b>',
                    tr)
                if url_titles:
                    torrents.append(
                        [urllib.parse.quote('{0}{1}'.format(self.url, url_titles.group(1))), url_titles.group(
                            2), url_titles.group(3).replace(",", ""), url_titles.group(5).replace(",", ""),
                         url_titles.group(6).replace(",", "")])
            return torrents

    def download_torrent(self, info):
        torrent_page = retrieve_url(urllib.parse.unquote(info))
        magnet_match = re.search(
            r'\"(magnet:.*?)\"', torrent_page)
        if magnet_match and magnet_match.groups():
            print('{0} {1}'.format(magnet_match.groups()[0], info))
        else:
            raise Exception('Error, please fill a bug report!')

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        for currPage in range(0, self.max_pages):
            url = '{0}search_results.php?search={1}&cat={2}&page={3}'.format(
                self.url, what, self.supported_categories[cat], currPage)
            # Some replacements to format the html source
            html = retrieve_url(url).replace("	", "").replace(
                "\n", "").replace("\r", "")

            parser.feed(html)
            # if there are no results exit
            if parser.pageResSize <= 0:
                break
