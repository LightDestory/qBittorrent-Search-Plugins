# VERSION: 1.00
# AUTHORS: LightDestory (https://github.com/LightDestory)


import re
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
from time import sleep
from datetime import datetime


class torrentdownloads(object):
    url = "https://www.torrentdownloads.pro/"
    name = "TorrentDownloads"
    supported_categories = {
        "all": "0",
        "movies": "4",
        "tv": "8",
        "music": "5",
        "games": "3",
        "anime": "1",
        "software": "7",
        "books": "2",
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
            trs = re.findall(
                r"<div class=\"grey_bar3(?: back_none)?\".+?check_box.+?</div>", html
            )[1:]
            for tr in trs:
                url_titles = re.search(
                    r"href=\"(.+?)\".+?>\s?(.+?)</a>.+?<span>([0-9,.]+).+?span>([0-9,.]).+?([0-9\,\.]+ (TB|GB|MB|KB))",
                    tr,
                )
                if url_titles:
                    # Get Unix timestamp if possible using datetime.timestamp() function, otherwise set it to -1
                    timestamp = -1
                    generic_url = "{0}{1}".format(self.url[:-1], url_titles.group(1))
                    torrent_data = [
                        generic_url,
                        url_titles.group(2),
                        url_titles.group(5),
                        url_titles.group(3),
                        url_titles.group(4),
                        generic_url,
                        timestamp,
                    ]
                    torrents.append(torrent_data)
            return torrents

    def download_torrent(self, info):
        torrent_page = re.sub(r"\s+", " ", retrieve_url(info)).strip()
        download_link = re.search(r"href=\"(https?://itorrents.+?)\"", torrent_page)
        if download_link:
            print(download_file(download_link.group(1)))
        else:
            raise Exception("Download link not found")

    def search(self, what, cat="all"):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self.url)
        current_page = 1
        while True:
            url = "{0}search/?page={1}&search={2}&s_cat={3}&srt=seeds&pp=50&order=desc".format(
                self.url, current_page, what, self.supported_categories[cat]
            )
            html = re.sub(r"\s+", " ", retrieve_url(url)).strip()
            parser.feed(html)
            if parser.noTorrents:
                break
            current_page += 1
            # Always set a sleep(3) after each request to the search engine website, otherwise you might get banned by the search engine.
            sleep(3)
