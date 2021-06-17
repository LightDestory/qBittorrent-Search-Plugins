# VERSION: 1.0
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
import urllib.parse

from helpers import retrieve_url, download_file
from novaprinter import prettyPrinter


class yourbittorrent(object):
    url = 'https://yourbittorrent.com/'
    name = 'YourBittorrent'
    supported_categories = {'all': '0', 'movies': '1', 'tv': '3', 'music': '2', 'games': '4', 'anime': '6',
                            'software': '5'}
    # YourBittorrent's search divided into pages, so we are going to set a limit on how many pages to read
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
            html = re.findall(r'<div class=\"table-responsive\">.+?</table></div>', html)[1]
            trs = re.findall(r'<tr class=\"table-default\">.+?</tr>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'.+?href=\"(.+?)\".+?title=\"(.+?)\".+?([0-9\.\,]+ (TB|GB|MB|kB)).+?sd\">([0-9,]+)<.+?pr\">([0-9,]+)<',
                    tr)
                if url_titles:
                    torrents.append(
                        [urllib.parse.quote('{0}{1}'.format(self.url, url_titles.group(1))), url_titles.group(
                            2).replace("<b>", "").replace("</b>", ""), url_titles.group(3).replace(",", ""),
                         url_titles.group(5).replace(",", ""),
                         url_titles.group(6).replace(",", "")])
            return torrents

    def download_torrent(self, info):
        torrent_page = retrieve_url(urllib.parse.unquote(info))
        file_link = re.search(
            r'(down/.+?\.torrent)', torrent_page)
        if file_link and file_link.groups():
            print(download_file(self.url + file_link.groups()[0]))
        else:
            raise Exception('Error, please fill a bug report!')

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        what = what.replace("%20", "-")
        parser = self.HTMLParser(self.url)
        for currPage in range(1, self.max_pages):
            url = '{0}?q={1}&c={2}&page={3}'.format(
                self.url, what, self.supported_categories[cat], currPage)
            # Some replacements to format the html source
            html = retrieve_url(url).replace("	", "").replace(
                "\n", "").replace("\r", "")
            parser.feed(html)
            # if there are no results exit
            if parser.pageResSize <= 0:
                break
