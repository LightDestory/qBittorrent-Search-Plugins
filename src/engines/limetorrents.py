# VERSION: 1.1
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
import sys
from urllib.parse import quote, unquote

from helpers import retrieve_url, download_file
from novaprinter import prettyPrinter


class limetorrents(object):
    url = 'https://www.limetorrents.lol/'
    name = 'LimeTorrents'
    supported_categories = {'all': 'all',
                            'anime': 'anime',
                            'movies': 'movies',
                            'music': 'music',
                            'tv': 'tv',
                            'software': 'applications',
                            'games': 'games',
                            }
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
                    'desc_link': torrents[torrent][5]
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            search_table = re.findall(r'<table .+?>.+?</table>', html)[1]
            trs = re.findall(
                r'<tr.+?>.+?</tr>', search_table)[1:]
            for tr in trs:
                url_titles = re.search(
                    r'.+?href=\"(.+?\") rel.+?href=\"(.+?)\".+?([0-9\,\.]+\s?(TB|GB|MB|KB)).+?tdseed\">([0-9,]+).+?tdleech\">([0-9,]+)',
                    tr)
                if url_titles:
                    generic_url = '{0}{1}'.format(self.url[:-1], url_titles.group(2))
                    name = url_titles.group(1).split("title=",1)[1].replace("-", " ")
                    torrent_data = [
                        url_titles.group(1).strip('"\' '),
                        name,
                        url_titles.group(3),
                        url_titles.group(5),
                        url_titles.group(6),
                        generic_url
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, info):
        try:
            info = unquote(info.strip(' "\''))
            if info.startswith(self.url):
                html = retrieve_url(info)
                # Try to extract magnet link first
                magnet_match = re.search(r'href="(magnet:\?xt=urn:btih:[^"]+)"', html)
                if magnet_match:
                    magnet_link = magnet_match.group(1)
                    print(download_file(magnet_link))
                    return
                # If no magnet, try .torrent link extraction
                torrent_match = re.search(r'href="(http[^"]+\.torrent[^"]*)"', html)
                if torrent_match:
                    torrent_url = torrent_match.group(1)
                    print(download_file(torrent_url))
                    return
                print(f"Could not find magnet or torrent link on page: {info}", file=sys.stderr)
            else:
                # info might be magnet or torrent link directly
                print(download_file(info))
        except Exception as e:
            print(f"Error in download_torrent: {e}", file=sys.stderr)


    def search(self, what, cat='all'):
        what = what.replace('%20', '-')
        parser = self.HTMLParser(self.url)
        current_page = 1
        while True:
            url = '{0}search/{1}/{2}/{3}/'.format(self.url, self.supported_categories[cat], what, current_page)
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            current_page += 1
