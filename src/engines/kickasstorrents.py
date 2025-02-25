# VERSION: 1.1
# AUTHORS: LightDestory (https://github.com/LightDestory)

import re
from time import sleep

from helpers import retrieve_url
from novaprinter import prettyPrinter


class kickasstorrents(object):
    url = 'https://katcr.to/'
    name = 'Kickasstorrents'

    supported_categories = {'all': '', 'movies': 'movies', 'tv': 'tv', 'music': 'music', 'games': 'games', 'anime': 'anime', 'software': 'apps'}
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

        def __findTorrents(self, html):
            # Find all TR nodes with class odd or even
            trs = re.findall(r'<tr class=\"(?:odd|even)\">.*?</tr>', html)
            for tr in trs:
                url_titles = re.search(
                    r'.+?torrentname.+?href=\"(.+?)\".+?cellMainLink\">(.+?)<.+?nobr.+?>([0-9\.\,]+ (TB|GB|MB|KB)).+?green.+?>([0-9,]+).+?red.+?>([0-9,]+)',
                    tr)
                if url_titles:
                    detail_link = '{0}{1}'.format(self.url, url_titles.group(1))
                    download_link = self.__retrieve_download_link(detail_link)
                    data = {
                        'link': download_link,
                        'name': url_titles.group(2),
                        'size': url_titles.group(3).replace(",", ""),
                        'seeds': url_titles.group(5).replace(",", ""),
                        'leech': url_titles.group(6).replace(",", ""),
                        'engine_url': self.url,
                        'desc_link': detail_link,
                    }
                    prettyPrinter(data)
                    sleep(1)
            return trs

        def __retrieve_download_link(self, detail_link):
            torrent_page = retrieve_url(detail_link)
            magnet_match = re.search(r'\"(magnet:.*?)\"', torrent_page)
            if magnet_match and magnet_match.groups():
                return str(magnet_match.groups()[0])
            else:
                return "NotFound"

    def search(self, what, cat='all'):
        parser = self.HTMLParser(self.url)
        category = "" if cat == "all" else 'category/{0}/'.format(self.supported_categories[cat])
        counter: int = 0
        while True:
            url = '{0}search/{1}/{2}{3}/'.format(self.url, what, category, counter)
            # Some replacements to format the html source
            html = re.sub(r'\s+', ' ', retrieve_url(url)).strip().replace("<strong class=\"red\">", "").replace("</strong>", "")
            parser.feed(html)
            if parser.noTorrents:
                break
            counter += 1
