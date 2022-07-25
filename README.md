# qBittorrent Search Plugins

This is a still growing collection of search plugins for qBittorent, an amazing and open source torrent client,
maintained by me, LightDestory.

If a plugin stops working or you need a specific plugin, let me know by opening an issue.

- [qBittorrent Search Plugins](#qbittorrent-search-plugins)
  - [Status](#status)
  - [Install and Usage](#install-and-usage)
  - [:book: Notes](#book-notes)
  - [Contributions and Testing](#contributions-and-testing)
  - [Support](#support)
  - [:warning: License](#warning-license)

## Status

| Plugin                                                                   | Version | Last Updated | Working?           |
| ------------------------------------------------------------------------ |---------|--------------| ------------------ |
| ![AcademicTorrents](./src/engines/academictorrents.png) AcademicTorrents | 1.1     | 01/05/2022   | :heavy_check_mark: |
| ![btetree](./src/engines/btetree.png) btetree                            | 1.2     | 17/06/2021   | :heavy_check_mark: |
| ![ETTV](./src/engines/ettv.png) ETTV                                     | 1.2     | 17/06/2021   | :heavy_multiplication_x: - **Site seems to be closed at 08-02-22** |
| ![GloTorrents](./src/engines/glotorrents.png) GloTorrents                | 1.4     | 25/07/2022   | :heavy_check_mark: |
| ![IlCorsaroNero](./src/engines/ilcorsaronero.png) IlCorsaroNero          | 1.2     | 17/06/2021   | :heavy_check_mark: |
| ![RARBG](./src/engines/rarbg.png) RARBG                                  | 1.1     | 06/12/2021   | :heavy_check_mark: |
| ![RockBox](./src/engines/rockbox.png) RockBox                            | 1.0     | 17/06/2021   | :heavy_check_mark: |
| ![Snowfl](./src/engines/snowfl.png) Snowfl                               | 1.1     | 03/06/2022   | :heavy_check_mark: |
| ![ThePirateBay](./src/engines/thepiratebay.png) ThePirateBay             | 1.0     | 14/11/2021   | :heavy_check_mark: |
| ![TNTVillageDump](./src/engines/tntvillagedump.png) TNTVillageDump       | 1.1     | 31/01/2022   | :heavy_check_mark: |
| ![YourBittorrent](./src/engines/yourbittorrent.png) YourBittorrent       | 1.3     | 22/02/2022   | :heavy_check_mark: |

## Install and Usage

To install a search plugin please refers to
the [official wiki](https://github.com/qbittorrent/search-plugins/wiki/Install-search-plugins).

Some plugins can need some settings, please read carefully the *Notes* section.

## :book: Notes

- **IlCorsaroNero** has been blacklisted on Italy's DNS, please **use a different DNS such as Google or Cloudflare**
- **AcademicTorrents** please set "Search in" properly!
- **Snowfl** is a torrent aggregator, there is not a fixed way to fetch the torrent. I tried to fix the in-app torrent
  fetch implementing a generic magnet link fetch, but it doesn't work every time.
- **RARBG** uses an anti-spam system, if you perform a lot of queries on a short time the plugin will stop working until their system
  removes you from a "alert" list
- **TNTVillage** uses a emdebed dump so it is a bit fatty: 20MB of plugin!
- **YourBittorrent** by default the website only shows 50 torrent based on your text-query, I tried to force pagination but it causes duplicates results. So... use specific queries!

## Contributions and Testing

To contribute, just write your own script following
the [official wiki](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin#python-class-file-structure)
and put it inside `/src/engines`.

For comodity I have included the needed files requires to testing the plugins, the nova scripts:

1. `cd ./src`
2. > python ./nova2.py **search_engine** **category** **search keywords**

## Support

<p align="center">
    <a href="https://coindrop.to/lightdestory" target="__blank"><img alt="Coindrop" title="Support me with a donation!"
            src="https://img.shields.io/badge/-Support me with coindrop.to-yellowgreen?style=for-the-badge&logo=paypal&logoColor=white" /></a>
</p>

## :warning: License

This collection is under GNU GPL-3.0 License.
