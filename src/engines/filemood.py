# VERSION: 1.0
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
from urllib.parse import quote, unquote

from helpers import retrieve_url
from novaprinter import prettyPrinter


class filemood(object):
    url = 'https://filemood.com/'
    name = 'FileMood'

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
            trs = re.findall(
                r'<table>.+?</table>', html)[7:]
            for tr in trs:
                url_titles = re.search(
                    r'.+?href=\"(.+?([a-z0-9]{40}).+?)\" title=\"(.+?)\".+?b>([0-9,]+)\/([0-9,]+).+?([0-9\,\.]+\s?(TB|GB|MB|KB))',
                    tr)
                if url_titles:
                    generic_url = '{0}{1}'.format(self.url[:-1], url_titles.group(1))
                    dotted_name = url_titles.group(3).replace(" ", ".")
                    magnet_link = f"magnet:?xt=urn:btih:{url_titles.group(2)}&dn={dotted_name}&tr=https%3A%2F%2Ftracker.bjut.jp%2Fannounce&tr=https%3A%2F%2Fapi.ipv4online.uk%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3Dcbb9f62431802fc7372c0e323954f417&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3D9b05ae8e24a8048518545dcbe53d4a49&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3D39587f193c03d3877f1c79f18448e82e&tr=http%3A%2F%2Fmycarpathians.net%3A2710%2F4c242dced71f9fcfc07ad884c30c0aa5%2Fannounce&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3Db27e932a002eeb2ff9f8870fb632c914&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3D64024a20513018fc579f82dac62d0d95&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3D3fa2096a6ff57c995fa061270491cc3c&tr=http%3A%2F%2Fwww.thetradersden.org%2Fforums%2Ftracker%2Fannounce.php%3Fpasskey%3D076a404e6fe8cd98236cb35518c247e0&tr=http%3A%2F%2Fbt.zlofenix.org%3A81%2Fps2wluqkjplh0xdpt8cyfufsbu4jde82%2Fannounce&tr=https%3A%2F%2Ftracker.linvk.com%2Fannounce&tr=https%3A%2F%2Ftracker.wsaoa.eu.org%2Fannounce&tr=http%3A%2F%2Funit193.net%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.trainsim.ru%2Fannounce.php&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3Ddb2095becd888c069565f49d7a1c0594&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3D3d0588a8c3b251e3be554d8c22e7606e&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3D698d51e4fb05a5f1ff7c9fe1d8dd5eb3&tr=http%3A%2F%2Fgood73.net%2Fannounce.php%3Fpasskey%3Df9b19ea8afab63079761e964ad0f1df2&tr=http%3A%2F%2Fwww.good73.net%2Fannounce.php%3Fpasskey%3D945e006a8a649fc10101e709633f4055"
                    torrent_data = [
                        quote(magnet_link),
                        url_titles.group(3),
                        url_titles.group(6),
                        url_titles.group(4),
                        url_titles.group(5),
                        generic_url,
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, info):
        unquoted_magnet = unquote(info)
        print(unquoted_magnet + " " + unquoted_magnet)

    def search(self, what, cat='all'):
        what = what.replace('%20', '+')
        parser = self.HTMLParser(self.url)
        current_page = 0
        while True:
            url = '{0}result?q={1}+in%3Atitle&f={2}'.format(self.url, what, current_page*20)
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            current_page += 1