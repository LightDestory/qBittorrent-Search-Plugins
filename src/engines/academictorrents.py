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

    def formatTemplate(self):
        return {'link': '-1', 'name': '-1', 'size': '-1', 'seeds': '-1', 'leech': '-1', 'engine_url': self.url,
                'desc_link': '-1'}

    def parseJSON(self, collection):
        for torrent in collection:
            data = self.formatTemplate()
            data['link'] = urllib.parse.quote(torrent['url'])
            data['name'] = torrent['name']
            data['size'] = torrent['size']
            data['seeds'] = torrent['mirrors']
            data['leech'] = torrent['downloaders']
            data['desc_link'] = urllib.parse.unquote(data['link'])
            prettyPrinter(data)

    def download_torrent(self, info):
        hash = urllib.parse.unquote(info).split("/")[-1]
        if len(hash) == 40:
            print(download_file('{0}/download/{1}.torrent'.format(self.url, hash)))
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
