# VERSION: 1.2
# AUTHORS: LightDestory (https://github.com/LightDestory)

import sys
from pathlib import Path
from datetime import date
from urllib import request
import xml.etree.ElementTree as ET

from helpers import retrieve_url
from novaprinter import prettyPrinter

DATABASE_URL = "https://academictorrents.com/database.xml"
FILTERS = []
home = str(Path.home())
system_paths = {
    'win32': f"{home}/AppData/Roaming",
    'linux': f"{home}/.local/share",
    'darwin': f"{home}/Library/Application Support",
}
cache_path = Path(f"{system_paths[sys.platform]}/qbit_plugins_data/academic_cache.xml")


class academictorrents(object):
    url = 'https://academictorrents.com/'
    name = 'AcademicTorrents'
    """ 
    ***TLDR; It is safer to force an 'all' research***
        AcademicTorrents categories are very specific
        qBittorrent does not provide enough categories to implement a good filtering.
    """
    supported_categories = {'all': '0'}

    def _parseXML(self, collection):
        for torrent in collection:
            data = {
                'link': f"{self.url}/download/{torrent.findtext('infohash')}.torrent",
                'name': torrent.findtext("title"),
                'size': torrent.findtext("size"),
                'seeds': -1,
                'leech': -1,
                'engine_url': self.url,
                'desc_link': torrent.findtext("link")
            }
            prettyPrinter(data)

    def _torrent_filter(self, item) -> bool:
        global FILTERS
        title: str = item.findtext("title").lower()
        desc: str = item.findtext("description").lower()
        for f in FILTERS:
            if f in title or f in desc:
                return True
        return False

    def _retrieve_database(self):
        folder_path = Path(f"{system_paths[sys.platform]}/qbit_plugins_data")
        if not folder_path.exists():
            folder_path.mkdir()
        self._update_database_cache()
        with open(cache_path, encoding="utf-8") as f:
            lines = f.readlines()[1:]
            return ET.fromstring("".join(lines))

    def _update_database_cache(self):
        if cache_path.exists():
            current_date = str(date.today())
            with open(cache_path, encoding="utf-8") as f:
                saved_date = f.readline().rstrip()
                if current_date == saved_date:
                    return
        req = request.urlopen(DATABASE_URL)
        db_local_text = req.read().decode("utf-8")
        f = open(cache_path, "w", encoding="utf-8")
        f.write(f"{str(date.today())}\n")
        f.write(db_local_text)
        f.close()
        req.close()


    def search(self, what, cat='all'):
        global FILTERS
        FILTERS = [f.lower() for f in str(what).split("%20")]
        db = self._retrieve_database()
        filtered = list(filter(self._torrent_filter, db.findall("channel/item")))
        self._parseXML(filtered)
