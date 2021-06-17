# VERSION: 1.0
# AUTHORS: LightDestory (https://github.com/LightDestory)

import urllib.parse
import json

from helpers import retrieve_url, download_file
from novaprinter import prettyPrinter

YOUR_API_KEY = ""
YOUR_UID = ""


class academictorrents(object):
    url = 'https://academictorrents.com/'
    name = 'AcademicTorrents'
    """ 
    ***TLDR; It is safer to force an 'all' research***
        AcademicTorrents categories are very specific
        qBittorrent does not provide enough categories to implement a good filtering.
    """
    supported_categories = {'all': '0'}

    def parseJSON(self, collection):
        for torrent in collection:
            data = {
                'link': urllib.parse.quote(torrent['url']),
                'name': torrent['name'],
                'size': torrent['size'],
                'seeds': torrent['mirrors'],
                'leech': torrent['downloaders'],
                'engine_url': self.url,
                'desc_link': torrent['url']
            }
            prettyPrinter(data)

    def download_torrent(self, info):
        infoHash = urllib.parse.unquote(info).split("/")[-1]
        if len(infoHash) == 40:
            print(download_file('{0}/download/{1}.torrent'.format(self.url, infoHash)))
        else:
            raise Exception('Error, please fill a bug report!')

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        what = what.replace("%20", "+")
        auth = "" if (not YOUR_API_KEY or not YOUR_UID) else '&uid={0}&pass={1}&limit=9999'.format(YOUR_UID,
                                                                                                   YOUR_API_KEY)
        url = '{0}apiv2/entries?search={1}{2}'.format(
            self.url, what, auth)
        # Getting JSON from API
        collection = json.loads(retrieve_url(url))
        self.parseJSON(collection)
