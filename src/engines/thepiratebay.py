# VERSION: 1.1
# AUTHORS: LightDestory (https://github.com/LightDestory)

import urllib.parse
import json
from helpers import retrieve_url, download_file
from novaprinter import prettyPrinter


class thepiratebay(object):
    url = 'https://thepiratebay.org/'
    api_url = "https://apibay.org/"
    name = 'The Pirate Bay'
    """ 
        TLDR; It is safer to force an 'all' research
        The Pirate Bay categories requires to set GET parameters
    """
    supported_categories = {'all': '0'}

    def parseJSON(self, collection):
        if collection[0]['name'] == "No results returned":
            return
        for torrent in collection:
            data = {
                'link': 'magnet:?xt=urn:btih:{0}&dn={1}&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2780%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2730%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=http%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce'
                .format(torrent['info_hash'], urllib.parse.quote(torrent['name'])),
                'name': torrent['name'],
                'size': torrent['size'],
                'seeds': torrent['seeders'],
                'leech': torrent['leechers'],
                'engine_url': self.url,
                'desc_link': 'https://thepiratebay.org/description.php?id={0}'.format(torrent["id"])
            }
            prettyPrinter(data)

    def search(self, what, cat='all'):
        url = '{0}q.php?q={1}&cat=0'.format(self.api_url, what)
        # Getting JSON from API
        collection = json.loads(retrieve_url(url))
        self.parseJSON(collection)
