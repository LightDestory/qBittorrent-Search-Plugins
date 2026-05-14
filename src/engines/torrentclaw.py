# VERSION: 1.0
# AUTHORS: Deivid Soto (TorrentClaw) <[email protected]>
#
# TorrentClaw qBittorrent search plugin.
#
# TorrentClaw aggregates 10+ public torrent sources and enriches each release
# with TrueSpec metadata (real audio/subtitles/codec/HDR — not filename guesses)
# and a 0-100 quality score.
#
# Public JSON API at https://torrentclaw.com/api/v1/search. An API key is
# optional for unauthenticated reads, but required to receive ready-made magnet
# links. Without a key, the plugin reconstructs the magnet locally from the
# returned info_hash plus a public tracker list (works in qBittorrent the same).
#
# To use an API key, set the TORRENTCLAW_API_KEY environment variable before
# launching qBittorrent, or edit the API_KEY constant below.

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from helpers import retrieve_url
from novaprinter import prettyPrinter


API_KEY: str = os.environ.get("TORRENTCLAW_API_KEY", "")
HTTP_TIMEOUT_SECONDS: int = 15

# Public open trackers (subset of the list TorrentClaw uses server-side).
# Drift risk: if upstream tracker list changes, this falls behind. Update
# manually from src/lib/tracker-list.ts on each plugin release.
TRACKERS: List[str] = [
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://open.tracker.cl:1337/announce",
    "udp://tracker.openbittorrent.com:6969/announce",
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://open.stealth.si:80/announce",
    "udp://exodus.desync.com:6969/announce",
    "udp://open.demonii.com:1337/announce",
    "udp://tracker.qu.ax:6969/announce",
    "udp://tracker.dler.org:6969/announce",
    "udp://tracker.filemail.com:6969/announce",
]


def _format_size(size_bytes: Optional[int]) -> str:
    """qBittorrent expects a human-readable size string ("1.2 GB"), not int."""
    if not size_bytes or size_bytes < 0:
        return "-1"
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size_bytes)
    unit_index = 0
    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1
    return f"{value:.2f} {units[unit_index]}"


class torrentclaw:
    name = "TorrentClaw"
    url = "https://torrentclaw.com"
    # supported_categories maps qBT standard category names to the TorrentClaw
    # API "type" filter value (None = no filter).
    supported_categories = {
        "all": None,
        "movies": "movie",
        "tv": "show",
    }

    def _build_magnet(self, info_hash: str, title: str) -> str:
        dn = urllib.parse.quote(title.replace(" ", "."))
        trs = "".join(f"&tr={urllib.parse.quote(t, safe='')}" for t in TRACKERS)
        return f"magnet:?xt=urn:btih:{info_hash}&dn={dn}{trs}"

    def _fetch(self, what: str, cat_filter: Optional[str]) -> Dict[str, Any]:
        params: Dict[str, str] = {
            "q": what,
            "limit": "50",
        }
        if cat_filter:
            params["type"] = cat_filter

        url = f"{self.url}/api/v1/search?{urllib.parse.urlencode(params)}"

        # retrieve_url() respects qBittorrent proxy settings but does not allow
        # custom headers. When an API key is set we fall back to urllib (which
        # bypasses the qBT proxy — acceptable trade-off for users who opt in to
        # an API key and presumably know their network setup).
        if API_KEY:
            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "User-Agent": "qBittorrent (TorrentClaw plugin)",
                    "Accept": "application/json",
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
                    body = resp.read().decode("utf-8", errors="replace")
            except (urllib.error.URLError, TimeoutError, OSError):
                return {"results": []}
        else:
            try:
                body = retrieve_url(url)
            except Exception:
                return {"results": []}

        try:
            return json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return {"results": []}

    def _emit(
        self,
        content_title: str,
        content_url: Optional[str],
        torrent: Dict[str, Any],
    ) -> None:
        info_hash: Optional[str] = torrent.get("infoHash")
        raw_title: str = torrent.get("rawTitle") or content_title
        if not info_hash:
            return

        # Prefer API-provided magnet (PRO keys) but fall back to local build.
        magnet: str = torrent.get("magnetUrl") or self._build_magnet(info_hash, raw_title)

        # Decorate title with quality score and TrueSpec tag — same convention
        # the Torznab endpoint uses, so Sonarr/Radarr Custom Formats match.
        decorated = raw_title
        score = torrent.get("qualityScore")
        if isinstance(score, int):
            decorated += f" [TC-{score}]"
        if torrent.get("scanStatus") == "success":
            decorated += " [TrueSpec]"

        size_str = _format_size(torrent.get("sizeBytes"))
        seeds_val = torrent.get("seeders")
        leech_val = torrent.get("leechers")
        seeds_str = str(seeds_val) if isinstance(seeds_val, int) else "-1"
        leech_str = str(leech_val) if isinstance(leech_val, int) else "-1"
        uploaded_at = torrent.get("uploadedAt")

        # Convert ISO-8601 timestamp to UNIX seconds (qBittorrent wants int).
        pub_date: int = -1
        if uploaded_at:
            try:
                from datetime import datetime
                pub_date = int(
                    datetime.fromisoformat(uploaded_at.replace("Z", "+00:00")).timestamp()
                )
            except (ValueError, TypeError):
                pub_date = -1

        desc_link = f"{self.url}{content_url}" if content_url else self.url

        prettyPrinter(
            {
                "link": magnet,
                "name": decorated,
                "size": size_str,
                "seeds": seeds_str,
                "leech": leech_str,
                "engine_url": self.url,
                "desc_link": desc_link,
                "pub_date": pub_date,
            }
        )

    def search(self, what: str, cat: str = "all") -> None:
        decoded = urllib.parse.unquote(what)
        cat_filter = self.supported_categories.get(cat)

        data = self._fetch(decoded, cat_filter)
        results: List[Dict[str, Any]] = data.get("results") or []

        for content in results:
            content_title: str = content.get("title") or ""
            content_url: Optional[str] = content.get("contentUrl")
            torrents: List[Dict[str, Any]] = content.get("torrents") or []
            for t in torrents:
                self._emit(content_title, content_url, t)


if __name__ == "__main__":
    # Local manual test:
    #   python3 torrentclaw.py "the dark knight"
    #   python3 torrentclaw.py "breaking bad" tv
    import sys

    query = sys.argv[1] if len(sys.argv) > 1 else "matrix"
    category = sys.argv[2] if len(sys.argv) > 2 else "all"
    torrentclaw().search(query, category)
