# VERSION: 1.00
# AUTHORS: YOUR_NAME (YOUR_MAIL)

# LICENSING INFORMATION

import re
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
from time import sleep
from datetime import datetime


class engine_name(object):
    """
    `url`, `name`, `supported_categories` should be static variables of the engine_name class,
     otherwise qbt won't install the plugin.

    `url`: The URL of the search engine.
    `name`: The name of the search engine, spaces and special characters are allowed here.
    `supported_categories`: What categories are supported by the search engine and their corresponding id,
    possible categories are ('all', 'movies', 'tv', 'music', 'games', 'anime', 'software', 'pictures', 'books').
    """

    url = "http://www.engine-url.org"
    name = "Full engine name"
    supported_categories = {
        "all": "0",
        "movies": "6",
        "tv": "4",
        "music": "1",
        "games": "2",
        "anime": "7",
        "software": "3",
    }

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
                    "link": torrents[torrent][0],
                    "name": torrents[torrent][1],
                    "size": torrents[torrent][2],
                    "seeds": torrents[torrent][3],
                    "leech": torrents[torrent][4],
                    "engine_url": self.url,
                    "desc_link": torrents[torrent][5],
                    "pub_date": torrents[torrent][6],
                }
                prettyPrinter(data)

        def __findTorrents(self, html):
            torrents = []
            trs = re.findall(r"SINGLE_CONTAINER_REGEX", html)
            for tr in trs:
                url_titles = re.search(r"EXTRACTING_REGEX", tr)
                if url_titles:
                    # Get Unix timestamp if possible using datetime.timestamp() function, otherwise set it to -1
                    timestamp = -1
                    torrent_data = [
                        url_titles.group(-1),
                        url_titles.group(-1),
                        url_titles.group(-1),
                        url_titles.group(-1),
                        url_titles.group(-1),
                        "{0}{1}".format(self.url, url_titles.group(-1)),
                        timestamp,
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, info):
        """
        Providing this function is optional.
        It can however be interesting to provide your own torrent download
        implementation in case the search engine in question does not allow
        traditional downloads (for example, cookie-based download).
        """
        print(download_file(info))

    def search(self, what, cat="all"):
        # what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        current_page = 1
        while True:
            url = "{0}".format(
                self.url,
            )
            html = re.sub(r"\s+", " ", retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            current_page += 1
            # Always set a sleep(3) after each request to the search engine website, otherwise you might get banned by the search engine.
            sleep(3)
