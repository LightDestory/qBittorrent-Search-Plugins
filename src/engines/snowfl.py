# VERSION: 1.1
# AUTHORS: LightDestory (https://github.com/LightDestory)

# Based on gitDew work (https://github.com/gitDew/qbittorrent-snowfl-search-plugin)

import urllib.parse
import json
import random
import re
import string
import time

from helpers import retrieve_url
from novaprinter import prettyPrinter


class snowfl(object):
    url = 'https://snowfl.com/'
    name = 'Snowfl'
    # No categories provided
    supported_categories = {'all': '0'}

    class Parser:

        def __init__(self, url):
            self.url = url
            self.token = self.__retrieveToken()

        def feed(self, collection):
            for torrent in collection:
                data = {
                    'link': urllib.parse.quote(torrent['url']),
                    'name': torrent['name'],
                    'size': torrent['size'],
                    'seeds': torrent['seeder'],
                    'leech': torrent['leecher'],
                    'engine_url': self.url,
                    'desc_link': torrent['url']
                }
                prettyPrinter(data)

        def __retrieveToken(self):
            index_html = retrieve_url(self.url + "index.html")
            file_name = re.findall(r'.+?\"(b.min.js\?.+)\"', index_html)[0]
            script = retrieve_url(self.url + file_name)
            # Retrieving the token
            token = re.findall(r'\"([a-zA-Z0-9]+)\",step,queryId,count,sort,topx,filters=\[\],sources=\[\],nsfwFilter=!1,loadingMore=!1,resultItems=', script)[0]
            return token

        def generateQuery(self, what):
            random_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
            return '{0}/{1}/{2}/{3}/0/SEED/NONE/1?_={4}'.format(self.url, self.token, what, random_str,
                                                                str(int(time.time() * 1000)))

    def download_torrent(self, info):
        torrent_page = retrieve_url(urllib.parse.unquote(info))
        magnet_match = re.search(
            r'\"(magnet:.*?)\"', torrent_page)
        if magnet_match and magnet_match.groups():
            print('{0} {1}'.format(magnet_match.groups()[0], info))
        else:
            raise Exception('Error, please fill a bug report!')

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        parser = self.Parser(self.url)
        what = parser.generateQuery(what)
        parser.feed(json.loads(retrieve_url(what)))
