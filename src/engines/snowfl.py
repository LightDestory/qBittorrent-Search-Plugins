# VERSION: 1.4
# AUTHORS: LightDestory (https://github.com/LightDestory)

# Based on gitDew work (https://github.com/gitDew/qbittorrent-snowfl-search-plugin)

import sys
import os
import urllib.parse
import json
import random
import re
import string
import time
import helpers
#from helpers import retrieve_url
from novaprinter import prettyPrinter


debug = os.environ.get("DEBUG_SNOWFL", "") != ""


class TokenExpired(Exception):
    pass


def get_cache_dir():
    if sys.platform == "darwin":
        return os.environ["HOME"] + "/Library/Caches/qBittorrent/search"
    if sys.platform == "win32":
        return os.environ["HOME"] + "/AppData/Local/qBittorrent/qBittorrent/Cache"
    # linux, bsd, aix, ...
    return os.environ["HOME"] + "/.cache/qBittorrent/search"


def retrieve_url(url):
    """ Return the content of the url page as a string """
    #req = urllib.request.Request(url, headers=headers)
    req = urllib.request.Request(url, headers=helpers.headers)
    # no. raise urllib.error.URLError
    #try:
    #    response = urllib.request.urlopen(req)
    #except urllib.error.URLError as errno:
    #    print(" ".join(("Connection error:", str(errno.reason))))
    #    return ""
    response = urllib.request.urlopen(req)
    dat = response.read()
    # Check if it is gzipped
    if dat[:2] == b'\x1f\x8b':
        # Data is gzip encoded, decode it
        compressedstream = io.BytesIO(dat)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        extracted_data = gzipper.read()
        dat = extracted_data
    info = response.info()
    charset = 'utf-8'
    try:
        ignore, charset = info['Content-Type'].split('charset=')
    except Exception:
        pass
    dat = dat.decode(charset, 'replace')
    #dat = htmlentitydecode(dat)
    dat = helpers.htmlentitydecode(dat)
    # return dat.encode('utf-8', 'replace')
    return dat


class snowfl(object):
    url = 'https://snowfl.com/'
    name = 'Snowfl'
    # No categories provided
    supported_categories = {'all': '0'}
    cache_dir = get_cache_dir()

    def __init__(self):
        os.makedirs(self.cache_dir, exist_ok=True)

    class Parser:

        def __init__(self, engine):
            self.engine = engine
            self.url = engine.url
            self.cache_dir = engine.cache_dir
            self.token = self.get_token()
            # deduplicate results
            self.seen_btih_set = set()
            self.seen_btih_dict = dict()

        def feed(self, collection):
            #print(json.dumps(collection, indent=2)); sys.exit(1)
            def format_magnet(m):
                def filter_arg(arg):
                    if arg.startswith("tr="): # tracker
                        return False
                    if arg.startswith("dn="): # display name
                        return False
                    return True
                return "&".join(filter(filter_arg, m.split("&"))).lower()
            for torrent in collection:
                if "magnet" in torrent:
                    btih = re.search(r"xt=urn:btih:([0-9a-fA-F]{40})(&|$)", torrent['magnet'])
                    btih = btih.group(1).lower() if btih else None
                    if btih:
                        if btih in self.seen_btih_set:
                            if debug:
                                print("- btih", btih)
                                m1 = format_magnet(torrent['magnet'])
                                m2 = format_magnet(self.seen_btih_dict[btih])
                                if m1 != m2:
                                    print("  this  magnet", m1)
                                    print("  first magnet", m2)
                            # ignore duplicate
                            continue
                        self.seen_btih_set.add(btih)
                        if debug:
                            self.seen_btih_dict[btih] = torrent['magnet']
                            print("+ btih", btih) # , "from magnet", torrent['magnet'][:100])
                    else:
                        # no btih in magnet link
                        # never reached? snowfl returns only v1 torrents
                        # so there should be no v2 hash xt=urn:btmh:xxx
                        if debug:
                            print("no btih from magnet", torrent['magnet'][:100])
                data = {
                    'link': torrent['magnet'] if "magnet" in torrent else urllib.parse.quote(torrent['url'], safe="/:?&=#"),
                    'name': torrent['name'],
                    'size': torrent['size'],
                    'seeds': torrent['seeder'],
                    'leech': torrent['leecher'],
                    'engine_url': self.url,
                    'desc_link': torrent['url']
                }
                prettyPrinter(data)

        def update_token(self):
            self.token = self.get_token(True)

        def get_token(self, force_update=False):
            #return "asdf" # test: http error 404
            # example tokens
            # kPZXcfmzMnfqHbqPVAAIxlaCdTNMvUhJV
            # BwRIwYGdtihBNTvdyqVVcHhvWGByMYDtXUEc
            cache_path = self.cache_dir + "/snowfl.token.txt"
            if not force_update and os.path.exists(cache_path):
                # read cache
                if debug:
                    print("reading token from cache")
                with open(cache_path) as f:
                    token = f.read().strip()
                    return token
            # fetch token
            if debug:
                print("fetching token")
            index_html = helpers.retrieve_url(self.url + "index.html")
            # <script type="text/javascript" src="b.min.js?v=xxx"></script>
            file_name = re.search(r'src="(b\.min\.js\?[^"]+)"', index_html).group(1)
            if debug:
                print("file_name", file_name)
                print("script url", self.url + file_name)
            script = helpers.retrieve_url(self.url + file_name)
            token = re.search(r'\"([a-zA-Z0-9]+)\";\$\(\(function\(\){var e,t,n,r,o,a,i=', script).group(1)
            # write cache
            if debug:
                print("writing token to cache")
            with open(cache_path, "w") as f:
                f.write(token + "\n")
            if debug:
                print("token", token)
            return token

        def get_search_url_list(self, what):
            random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
            time_ms = int(time.time() * 1000)
            for page in range(0, 11):
                yield f'{self.url}/{self.token}/{what}/{random_str}/{page}/SEED/NONE/1?_={time_ms + page}'

    def download_torrent(self, info):
        if "magnet:?" in info:
            print('{0} {1}'.format(info, info))
        else:
            torrent_page = helpers.retrieve_url(urllib.parse.unquote(info))
            magnet_match = re.search(r'\"(magnet:.*?)\"', torrent_page)
            if magnet_match and magnet_match.groups():
                print('{0} {1}'.format(magnet_match.groups()[0], info))
            else:
                raise Exception('Error, please fill a bug report!')

    def search(self, what, cat='all'):
        parser = self.Parser(self)
        for retry_step in range(2):
            try:
                for url in parser.get_search_url_list(what):
                    try:
                        json_text = retrieve_url(url)
                    except urllib.error.URLError as exc:
                        if exc.status == 404:
                            raise TokenExpired
                        raise
                    parser.feed(json.loads(json_text))
                    time.sleep(1)
                break
            except TokenExpired:
                if debug:
                    print("token expired")
                parser.update_token()
