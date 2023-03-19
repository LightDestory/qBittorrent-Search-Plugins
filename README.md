# qBittorrent Search Plugins

This is a still growing collection of search plugins for qBittorrent, an amazing and open source torrent client,
maintained by me, LightDestory.

If a plugin stops working or you need a specific plugin, let me know by opening an issue.

- [qBittorrent Search Plugins](#qbittorrent-search-plugins)
    - [:bookmark: Status](#bookmark-status)
    - [:wrench: Install and Usage](#wrench-install-and-usage)
    - [:book: Notes](#book-notes)
    - [:gear: Contributions and Testing](#gear-contributions-and-testing)
    - [:handshake: Support](#handshake-support)
    - [:warning: License](#warning-license)

## :bookmark: Status

| Plugin                                                                   | Type          | Version (Updated)        | Working?                  | Download                                                                                                                                                                                                                                                              |
|--------------------------------------------------------------------------|---------------|--------------------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![AcademicTorrents](./src/engines/academictorrents.png) AcademicTorrents | Torrent Index | **1.2** - *(19/03/2023)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/academictorrents.py)</div>                                                                        |
| ![btetree](./src/engines/btetree.png) btetree                            | Torrent Index | **1.3** - *(19/03/2023)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/btetree.py)</div>                                                                                 |
| ![ETTV](./src/engines/ettv.png) ETTV                                     | Torrent Index | **1.2** - *(17/06/2021)* | :heavy_multiplication_x:  | <div align=center>Site Down :cry: <br> [<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/ettv.py) </div>                                                                         |
| ![GloTorrents](./src/engines/glotorrents.png) GloTorrents                | Torrent Index | **1.6** - *(19/03/2023)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/glotorrents.py)</div>                                                                             |
| ![IlCorsaroNero](./src/engines/ilcorsaronero.png) IlCorsaroNero          | Torrent Index | **1.3** - *(19/03/2023)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/ilcorsaronero.py)</div>                                                                           |
| ![Kickasstorrents](./src/engines/kickasstorrents.png) Kickasstorrents    | Torrent Index | **1.0** - *(28/07/2022)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/kickasstorrents.py)</div>                                                                         |
| ![Nitro](./src/engines/nitro.png) Nitro                                  | Torrent Index | **1.0** - *(29/07/2022)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/nitro.py)</div>                                                                                   |
| ![Pirateiro](./src/engines/pirateiro.png) Pirateiro                      | Aggregator    | **1.0** - *(28/07/2022)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/pirateiro.py)</div>                                                                               |
| ![RARBG](./src/engines/rarbg.png) RARBG                                  | Torrent Index | **1.1** - *(06/12/2021)* | :heavy_multiplication_x:  | <div align=center>My implementation is not working anymore, the following links to the official working one<br>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/rarbg.py)</div> |
| ![RockBox](./src/engines/rockbox.png) RockBox                            | Torrent Index | **1.0** - *(17/06/2021)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/rockbox.py)</div>                                                                                 |
| ![Snowfl](./src/engines/snowfl.png) Snowfl                               | Aggregator    | **1.3** - *(28/07/2022)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/snowfl.py)</div>                                                                                  |
| ![ThePirateBay](./src/engines/thepiratebay.png) ThePirateBay             | Torrent Index | **1.0** - *(14/11/2021)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/thepiratebay.py)</div>                                                                            |
| ![TNTVillageDump](./src/engines/tntvillagedump.png) TNTVillageDump       | Static Dump   | **1.1** - *(31/01/2022)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/tntvillagedump.py)</div>                                                                          |
| ![TorrentDownload](./src/engines/torrentdownload.png) TorrentDownload    | Aggregator    | **1.0** - *(28/07/2022)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/torrentdownload.py)</div>                                                                         |
| ![YourBittorrent](./src/engines/yourbittorrent.png) YourBittorrent       | Torrent Index | **1.3** - *(22/02/2022)* | :heavy_check_mark:        | <div align=center>[<img src="./.github/assets/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/yourbittorrent.py)</div>                                                                          |

## :wrench: Install and Usage

There are 2 way to install these plugins.

The easy way is to copy the link of the "Download" column of the table and use it as "web link" for qBittorrent.

The other way is to download the file by going to the download link and saving the file as a python file and then you
can install the plugin by selecting the file from your filesystem.

For any doubts about the installation process, please refer to the [official wiki](https://github.com/qbittorrent/search-plugins/wiki/Install-search-plugins).

Some plugins can need some settings, please read carefully the *Notes* section.

## :book: Notes

- **IlCorsaroNero** has been blacklisted on Italy's DNS, please **use a different DNS such as Google or Cloudflare**
- **AcademicTorrents** please set "Search in" properly!
- **Torrent aggregators** mix multiple torrent indexes, I tried to implement the most generic torrent/magnet fetch but
sometime it can fails
- **RARBG** uses an anti-spam system, for most of the time my implementation will not work, use the official plugin
based on torrentapi.
- **TNTVillage** uses an embed dump, so it is a bit fatty: 20MB of plugin!
- **YourBittorrent** by default the website only shows 50 torrent based on your text-query, I tried to force pagination
  but it causes duplicates results. So... use specific queries!

## :gear: Contributions and Testing

To contribute, just write your own script following
the [official wiki](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin#python-class-file-structure)
and put it inside `/src/engines`.

For commodity, I have included the needed files requires to testing the plugins, the nova scripts:

1. `cd ./src`
2. > python ./nova2.py **search_engine** **category** **search keywords**

## :handshake: Support

<p align="center">
    <a href="https://coindrop.to/lightdestory" target="__blank"><img alt="Coindrop" title="Support me with a donation!"
            src="https://img.shields.io/badge/-Support me with coindrop.to-yellowgreen?style=for-the-badge&logo=paypal&logoColor=white" /></a>
</p>

## :warning: License

This collection is under GNU GPL-3.0 License.
