# VERSION: 1.1
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
import urllib.parse

from helpers import retrieve_url, download_file
from novaprinter import prettyPrinter


class rarbg(object):
    url = 'http://www.rarbg.is/'
    name = 'RARBG'
    """ 
    ***TLDR; It is safer to force an 'all' research***
        RARBG's categories are very specific
        qBittorrent does not provide enough categories to implement a good filtering.
        For example, qBittorrent provides only a generic 'games' category meanwhile the website uses: pc, xbox and so on
    """
    supported_categories = {'all': '0'}
    # RARBG's search divided into pages, so we are going to set a limit on how many pages to read
    max_pages = 5

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
                    'desc_link': urllib.parse.unquote(torrents[torrent][0]).replace("http", "https")
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            trs = re.findall(r'<tr class=\"lista2\">.*?</tr>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'.+?\" href=\"/(.+?)\".+?>(.+?)</a>.+?([0-9\,\.]+ (TB|GB|MB|KB)).+?color=.+?>([0-9,]+).+?lista\">([0-9,]+).+?',
                    tr)
                if url_titles:
                    torrents.append(
                        [urllib.parse.quote('{0}{1}'.format(self.url, url_titles.group(1))), url_titles.group(
                            2), url_titles.group(3).replace(",", ""), url_titles.group(5),
                         url_titles.group(6)])
            return torrents

    def download_torrent(self, info):
        torrent_page = retrieve_url(urllib.parse.unquote(info))
        file_link = re.search(
            r'.+?href=\"/(download\.php\?.+?\.torrent)\"', torrent_page)
        if file_link and file_link.groups():
            print(download_file(self.url + file_link.groups()[0]))
        else:
            raise Exception('Error, please fill a bug report!')

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        for currPage in range(0, self.max_pages):
            url = '{0}torrents.php?search={1}&page={2}'.format(
                self.url, what, currPage)
            # Some replacements to format the html source
            html = retrieve_url(url).replace("	", "").replace(
                "\n", "").replace("\r", "")
            parser.feed(html)
            # if there are no results exit
            if parser.pageResSize <= 0:
                break
