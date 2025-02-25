# VERSION: 1.1
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re

from helpers import retrieve_url
from novaprinter import prettyPrinter


class torrentdownload(object):
    url = 'https://www.torrentdownload.info/'
    name = 'TorrentDownload'
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
                r'<tr><td.+?tt-name.+?</tr>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'.+?href=\"/(.+?)\">(.+?)</a>.+?tdnormal\">([0-9\,\.]+ (TB|GB|MB|KB)).+?tdseed\">([0-9,]+).+?tdleech\">([0-9,]+)',
                    tr)
                if url_titles:
                    torrent_data = [
                        'magnet:?xt=urn:btih:{0}&dn=&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker.ipv6tracker.ru%3A80%2Fannounce&tr=udp%3A%2F%2Fretracker.hotplug.ru%3A2710%2Fannounce&tr=https%3A%2F%2Ftracker.fastdownload.xyz%3A443%2Fannounce&tr=https%3A%2F%2Fopentracker.xyz%3A443%2Fannounce&tr=http%3A%2F%2Fopen.trackerlist.xyz%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.birkenwald.de%3A6969%2Fannounce&tr=https%3A%2F%2Ft.quic.ws%3A443%2Fannounce&tr=https%3A%2F%2Ftracker.parrotsec.org%3A443%2Fannounce&tr=udp%3A%2F%2Ftracker.supertracker.net%3A1337%2Fannounce&tr=http%3A%2F%2Fgwp2-v19.rinet.ru%3A80%2Fannounce&tr=udp%3A%2F%2Fbigfoot1942.sektori.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcarapax.net%3A6969%2Fannounce&tr=udp%3A%2F%2Fretracker.akado-ural.ru%3A80%2Fannounce&tr=udp%3A%2F%2Fretracker.maxnet.ua%3A80%2Fannounce&tr=udp%3A%2F%2Fbt.dy20188.com%3A80%2Fannounce&tr=http%3A%2F%2F0d.kebhana.mx%3A443%2Fannounce&tr=http%3A%2F%2Ftracker.files.fm%3A6969%2Fannounce&tr=http%3A%2F%2Fretracker.joxnet.ru%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.moxing.party%3A6969%2Fannounce'.format(url_titles.group(1).split("/")[0]),
                        url_titles.group(2).replace("<span class=\"na\">", "").replace("</span>", ""),
                        url_titles.group(3).replace(",", ""),
                        url_titles.group(5).replace(",", ""),
                        url_titles.group(6).replace(",", ""),
                        '{0}{1}'.format(self.url, url_titles.group(1))
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, download_url):
        print(download_url + " " + download_url)

    def search(self, what, cat='all'):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        for currPage in range(1, self.max_pages):
            url = '{0}search?q={1}&p={2}'.format(self.url, what, currPage)
            # Some replacements to format the html source
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip()
            parser.feed(html)
            if parser.pageResSize <= 0:
                break
