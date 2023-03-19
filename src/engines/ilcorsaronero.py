# VERSION: 1.3
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
from helpers import retrieve_url
from novaprinter import prettyPrinter


class ilcorsaronero(object):
    url = 'https://ilcorsaronero.link/'
    name = 'Il Corsaro Nero'
    """ 
        TLDR; It is safer to force an 'all' research
        IlCorsaroNero's categories are very specific
        qBittorrent does not provide enough categories to implement a good filtering.
        For example, qBittorrent provides only a generic 'games' category meanwhile the website uses: pc, xbox and so on
    """
    supported_categories = {'all': '0'}

    class HTMLParser:

        def __init__(self, url):
            self.url = url
            self.noTorrents = False

        def feed(self, html):
            self.noTorrents = False
            torrents = self.__findTorrents(html)
            if len(torrents) == 0:
                self.noTorrents = True
                return
            for torrent in range(len(torrents)):
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
            # Find all TR nodes with class odd or odd2
            trs = re.findall(r'<tr class=\"odd2?\">.*?</TR>', html)
            for tr in trs:
                # Extract from the A node all the needed information
                url_titles = re.search(
                    r'A class=\"tab\" HREF=\"(.+?)\" >(.+?)?</A>.+?([0-9\.\,]+ (TB|GB|MB|KB)).+?value=\"(.+?)\".+?#[0-9a-zA-Z]{6}\'>([0-9,]+)<.+?#[0-9a-zA-Z]{6}\'>([0-9,]+)',
                    tr)
                if url_titles:
                    name = url_titles.group(1).split("/")[5]
                    torrents.append([
                        'https://itorrents.org/torrent/{0}.torrent'.format(url_titles.group(5)),
                        name.replace("_", " "),
                        url_titles.group(3).replace(",", ""),
                        url_titles.group(6).replace(",", ""),
                        url_titles.group(7).replace(",", ""),
                        url_titles.group(1)
                    ])
            return torrents

    def search(self, what, cat='all'):
        parser = self.HTMLParser(self.url)
        counter: int = 0
        while True:
            url = '{0}advsearch.php?search={1}&&page={2}'.format(self.url, what, counter)
            # Some replacements to format the html source
            html = retrieve_url(url).replace("	", "").replace("\n", "").replace("\r", "").replace("n/a", "0")
            parser.feed(html)
            if parser.noTorrents:
                break
            counter += 1
