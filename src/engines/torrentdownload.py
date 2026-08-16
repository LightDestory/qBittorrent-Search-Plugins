# VERSION: 1.2
# AUTHORS: LightDestory (https://github.com/LightDestory)
# CONTRIBUTORS: YoWhatupGee (https://github.com/YoWhatupGee)

import re
from html import unescape
from time import sleep

from helpers import retrieve_url
from novaprinter import prettyPrinter


class torrentdownload(object):
    url = "https://www.torrentdownload.info"
    name = "TorrentDownload"
    supported_categories = {
        "all": "",
        "anime": "anime",
        "books": "books",
        "games": "games",
        "movies": "movies",
        "music": "music",
        "software": "applications",
        "tv": "tv",
    }
    max_pages = 10
    # Delay between page requests, the site throttles aggressive crawling
    page_delay = 1

    trackers = (
        "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
        "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
        "&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce"
        "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
        "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce"
        "&tr=udp%3A%2F%2Ftracker.birkenwald.de%3A6969%2Fannounce"
        "&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce"
    )

    class HTMLParser:
        # A result row always starts with "<tr><td" (sponsored rows carry a bgcolor attribute)
        row_re = re.compile(r"<tr><td.+?tt-name.+?</tr>")
        # Cells are matched individually so that an unexpected value in one of them
        # cannot silently discard the whole row
        torrent_re = re.compile(
            r'href="/(?P<hash>[0-9A-Fa-f]{40})/(?P<slug>[^"]*)">(?P<name>.*?)</a>'
            r'(?:\s*<span class="smallish">\s*(?:&raquo;|»)\s*(?P<cat>[^<]*)</span>)?'
            r'.*?<td class="tdnormal">[^<]*</td>'
            r'\s*<td class="tdnormal">(?P<size>[^<]*)</td>'
            r'\s*<td class="tdseed">(?P<seeds>[^<]*)</td>'
            r'\s*<td class="tdleech">(?P<leech>[^<]*)</td>'
        )
        tag_re = re.compile(r"<[^>]+>")
        # "1 - 50 of 1,740 for ..." in the results table header
        total_re = re.compile(r"<h1>[\d,]+ - [\d,]+ of ([\d,]+) for")
        # The site labels rows with its own category names
        category_rules = (
            ("anime", ("anime",)),
            ("books", ("book",)),
            ("movies", ("movie",)),
            ("tv", ("tv", "television")),
            ("music", ("music", "audio", "lossless")),
            ("games", ("game", "xbox", "playstation")),
            ("software", ("applic", "software")),
        )

        def __init__(self, engine):
            self.engine = engine
            self.seen = set()
            self.printed = 0
            self.total = None
            self.pageResSize = 0

        def feed(self, html, category="all"):
            self.pageResSize = 0
            total = self.total_re.search(html)
            if total:
                self.total = int(total.group(1).replace(",", ""))
            for row in self.row_re.findall(html):
                torrent = self.torrent_re.search(row)
                if not torrent:
                    continue
                self.pageResSize += 1
                info_hash = torrent.group("hash").lower()
                # The same torrent can show up on several pages
                if info_hash in self.seen:
                    continue
                self.seen.add(info_hash)
                if not self.__matches(torrent.group("cat"), category):
                    continue
                desc_link = "{0}/{1}/{2}".format(
                    self.engine.url, torrent.group("hash"), torrent.group("slug")
                )
                prettyPrinter({
                    "link": "magnet:?xt=urn:btih:{0}&dn={1}{2}".format(
                        info_hash, torrent.group("slug"), self.engine.trackers
                    ),
                    "name": self.__clean(torrent.group("name")),
                    "size": torrent.group("size").replace(",", "").strip(),
                    "seeds": self.__count(torrent.group("seeds")),
                    "leech": self.__count(torrent.group("leech")),
                    "engine_url": self.engine.url,
                    "desc_link": desc_link,
                })
                self.printed += 1

        def __clean(self, name):
            return unescape(self.tag_re.sub("", name)).strip()

        def __count(self, value):
            value = value.replace(",", "").strip()
            return value if value.isdigit() else "-1"

        def __matches(self, label, category):
            if category == "all":
                return True
            if not label:
                return False
            label = label.lower()
            for name, needles in self.category_rules:
                if any(needle in label for needle in needles):
                    return name == category
            return False

    def download_torrent(self, download_url):
        # Results are magnet links, qBittorrent handles them without a temporary file
        print(download_url + " " + download_url)

    def search(self, what, cat="all"):
        what = what.replace("%20", "+")
        parser = self.HTMLParser(self)
        for currPage in range(1, self.max_pages + 1):
            url = "{0}/search?q={1}&p={2}".format(self.url, what, currPage)
            # Collapse the whitespace so that the row patterns can rely on a single layout
            html = re.sub(r"\s+", " ", retrieve_url(url)).strip()
            parser.feed(html, cat)
            if parser.pageResSize <= 0:
                break
            if parser.total is not None and len(parser.seen) >= parser.total:
                break
            sleep(self.page_delay)
