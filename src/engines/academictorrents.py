# VERSION: 1.1
# AUTHORS: LightDestory (https://github.com/LightDestory)

from urllib import parse, request
import xml.etree.ElementTree as ET
from helpers import retrieve_url, download_file
from novaprinter import prettyPrinter

DATABASE_URL = "https://academictorrents.com/database.xml"
FILTERS = []

class academictorrents(object):
    url = 'https://academictorrents.com/'
    name = 'AcademicTorrents'
    """ 
    ***TLDR; It is safer to force an 'all' research***
        AcademicTorrents categories are very specific
        qBittorrent does not provide enough categories to implement a good filtering.
    """
    supported_categories = {'all': '0'}

    def parseXML(self, collection):
        for torrent in collection:
            data = {
                'link': parse.quote(torrent.findtext("link")),
                'name': torrent.findtext("title"),
                'size': torrent.findtext("size"),
                'seeds': -1,
                'leech': -1,
                'engine_url': self.url,
                'desc_link': torrent.findtext("link")
            }
            prettyPrinter(data)

    def torrent_filter(self, item) -> bool:
        global FILTERS
        title: str = item.findtext("title").lower()
        desc: str = item.findtext("description").lower()
        title_check: bool = True
        desc_check: bool = True
        for f in FILTERS:
            if f not in title:
                title_check = False
                break
        for f in FILTERS:
            if f not in desc:
                desc_check = False
                break
        return title_check or desc_check

    def retrieve_database(self):
        # TO-DO: Implement a cross-platform cache system
        req = request.urlopen(DATABASE_URL)
        db_local_text = req.read().decode("utf-8")
        req.close()
        return ET.fromstring(db_local_text)

    def download_torrent(self, info):
        infoHash = parse.unquote(info).split("/")[-1]
        if len(infoHash) == 40:
            print(download_file('{0}/download/{1}.torrent'.format(self.url, infoHash)))
        else:
            raise Exception('Error, please fill a bug report!')

    def search(self, what, cat='all'):
        global FILTERS
        FILTERS = [f.lower() for f in str(what).split("%20")]
        db = self.retrieve_database()
        filtered = list(filter(self.torrent_filter, db.findall("channel/item")))
        self.parseXML(filtered)
