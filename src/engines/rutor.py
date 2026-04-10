# VERSION: 1.00
# AUTHORS: LightDestory (https://github.com/LightDestory)


import re
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
from time import sleep
from datetime import datetime


RU_MONTHS = {
    "янв": 1,
    "фев": 2,
    "мар": 3,
    "апр": 4,
    "май": 5,
    "июн": 6,
    "июл": 7,
    "авг": 8,
    "сен": 9,
    "окт": 10,
    "ноя": 11,
    "дек": 12,
}


class rutor(object):
    url = "https://rutor.is/"
    name = "Rutor"
    supported_categories = {
        "all": "0",
        "music": "2",
        "games": "8",
        "anime": "10",
        "software": "9",
        "books": "11",
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
            trs = re.findall(r"<tr class=\"(?:gai|tum)\">.+?</tr>", html)
            for tr in trs:
                url_titles = re.search(
                    r"<td>(.+?)</td>.+?(magnet.+?)\">.+?(/torrent.+?)\">\s*(.+?)\s?</a>.+?([0-9\,\.]+ (?:TB|GB|MB|KB)).+?([0-9,.]+)</span>.+?([0-9\,\.])</span>",
                    tr,
                )
                if url_titles:
                    # Get Unix timestamp if possible using datetime.timestamp() function, otherwise set it to -1
                    day, mon, year = url_titles.group(1).strip().split()
                    mon = RU_MONTHS.get(mon.lower(), 0)
                    timestamp = int(
                        datetime.strptime(f"{day}/{mon}/{year}", "%d/%m/%y").timestamp()
                    )
                    torrent_data = [
                        url_titles.group(2),
                        url_titles.group(4),
                        url_titles.group(5),
                        url_titles.group(6),
                        url_titles.group(7),
                        "{0}{1}".format(self.url[:-1], url_titles.group(3)),
                        timestamp,
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, info):
        print(info)

    def search(self, what, cat="all"):
        parser = self.HTMLParser(self.url)
        current_page = 0
        while True:
            url = "{0}search/{1}/{2}/000/0/{3}".format(
                self.url, current_page, self.supported_categories[cat], what
            )
            html = re.sub(r"\s+", " ", retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            current_page += 1
            # Always set a sleep(3) after each request to the search engine website, otherwise you might get banned by the search engine.
            sleep(3)
