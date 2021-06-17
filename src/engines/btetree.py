# VERSION: 1.2
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
import urllib.parse

from helpers import retrieve_url, download_file
from novaprinter import prettyPrinter


class btetree(object):
    url = "http://bt.etree.org/"
    name = "bt.etree"
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
            trs = re.findall(
                r'<tr align=\"right\" bgcolor=\"#ffffff\">.+?</tr>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'<tr.+?details_link\" href=\"(.+?)\".+?<b>(.+?)</b>.+?([0-9\,\.]+ (TB|GB|MB|KB)).+?seeders\">([0-9,]+).+?leechers\">([0-9,]+)',
                    tr)
                if url_titles:
                    torrents.append(
                        [urllib.parse.quote('{0}{1}'.format(self.url, url_titles.group(1))), url_titles.group(
                            2), url_titles.group(3).replace(",", ""), url_titles.group(5).replace(",", ""),
                         url_titles.group(6).replace(",", "")])
            return torrents

    def download_torrent(self, info):
        torrent_page = retrieve_url(urllib.parse.unquote(info))
        file_link = re.search(
            r'.+?href=\"(.+?\.torrent)\"', torrent_page)
        if file_link and file_link.groups():
            print(download_file(self.url + file_link.groups()[0]))
        else:
            raise Exception('Error, please fill a bug report!')

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        what = what.replace('%20', '+')
        parser = self.HTMLParser(self.url)
        for currPage in range(0, self.max_pages):
            url = '{0}index.php?searchzzzz={1}&cat=0&page={2}'.format(
                self.url, what, 50*currPage)
            html = retrieve_url(url).replace(
                "	", "").replace("\n", "").replace("\r", "")
            parser.feed(html)
            # if there are no results exit
            if parser.pageResSize <= 0:
                break
