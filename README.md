# qBittorrent Search Plugins

This is a still growing collection of search plugins for qBittorent, an amazing and open source torrent client, maintained by me, LightDestory.

If a plugin stops to work or you need a specific plugin, let me know by opening an issue.

- [qBittorrent Search Plugins](#qbittorrent-search-plugins)
  - [Status](#status)
  - [Install and Usage](#install-and-usage)
  - [:book: Notes](#book-notes)
  - [Contributions and Testing](#contributions-and-testing)
  - [:warning: License](#warning-license)

## Status

| Plugin        | Version | Last Updated | Working?           |
| ------------- | ------- | ------------ | ------------------ |
| btetree       | 1.0     | 29/05/2021   | :heavy_check_mark: |
| ETTV          | 1.0     | 29/05/2021   | :heavy_check_mark: |
| IlCorsaroNero | 1.0     | 29/05/2021   | :heavy_check_mark: |

## Install and Usage

To install a search plugin please refers to the [official wiki](https://github.com/qbittorrent/search-plugins/wiki/Install-search-plugins).

Some plugins can need some settings, please read carefully the *Notes* section.

## :book: Notes

- IlCorsaroNero has been blacklisted on Italy's DNS, please __use a different DNS such as Google or Cloudflare__

## Contributions and Testing

To contribute, just write your own script following the [official wiki](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin#python-class-file-structure) and put it inside `/src/engines`.

For comodity I have included the needed files requires to testing the plugins, the nova scripts:

  1. `cd ./src`
  2. > python ./nova2.py **search_engine** **category** **search keywords**

## :warning: License

This collection is under GNU GPL-3.0 License.
