# VERSION: 1.0
# AUTHORS: LightDestory (https://github.com/LightDestory)


import re
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
from time import sleep
from datetime import datetime


class nyaa(object):
    url = "https://nyaa.si/"
    name = "Nyaa"
    supported_categories = {
        "all": "0_0",
        "movies": "4_0",
        "music": "2_0",
        "games": "6_2",
        "anime": "1_0",
        "software": "6_1",
        "books": "3_0",
        "pictures": "5_0",
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
            trs = re.findall(r"<tr class=.+?</tr>", html)
            for tr in trs:
                url_titles = re.search(
                    r"href=\"(/view/\d+)\"\s?.+?\"(.+?)\">.+?(magnet.+?)\".+?([0-9\,\.]+ (?:TiB|GiB|MiB|KiB|Bytes)).+?timestamp=\"(\d+)\".+?\">(\d+).+?\">(\d+)",
                    tr,
                )
                if url_titles:
                    torrent_data = [
                        url_titles.group(3),
                        url_titles.group(2),
                        url_titles.group(4),
                        url_titles.group(6),
                        url_titles.group(7),
                        "{0}{1}".format(self.url[:-1], url_titles.group(1)),
                        url_titles.group(5),
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, info):
        print(info + " " + info)

    def search(self, what, cat="all"):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        current_page = 1
        while True:
            url = "{0}?f=0&c={1}&q={2}&p={3}".format(
                self.url, self.supported_categories[cat], what, current_page
            )
            html = re.sub(r"\s+", " ", retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            current_page += 1
            # Always set a sleep(3) after each request to the search engine website, otherwise you might get banned by the search engine.
            sleep(3)
