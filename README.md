# qBittorrent Search Plugins

This is a still growing collection of search plugins for qBittorent, an amazing and open source torrent client,
maintained by me, LightDestory.

If a plugin stops to work or you need a specific plugin, let me know by opening an issue.

- [qBittorrent Search Plugins](#qbittorrent-search-plugins)
  - [Status](#status)
  - [Install and Usage](#install-and-usage)
  - [:book: Notes](#book-notes)
  - [Contributions and Testing](#contributions-and-testing)
  - [:warning: License](#warning-license)

## Status

| Plugin                                                          | Version | Last Updated | Working?           |
| --------------------------------------------------------------- | ------- | ------------ | ------------------ |
| ![btetree](./src/engines/academictorrents.ico) AcademicTorrents | 1.0     | 17/06/2021   | :heavy_check_mark: |
| ![btetree](./src/engines/btetree.ico) btetree                   | 1.2     | 17/06/2021   | :heavy_check_mark: |
| ![ETTV](./src/engines/ettv.ico) ETTV                            | 1.2     | 17/06/2021   | :heavy_check_mark: |
| ![GloTorrents](./src/engines/glotorrents.ico) GloTorrents       | 1.1     | 17/06/2021   | :heavy_check_mark: |
| ![IlCorsaroNero](./src/engines/ilcorsaronero.ico) IlCorsaroNero | 1.2     | 17/06/2021   | :heavy_check_mark: |

## Install and Usage

To install a search plugin please refers to
the [official wiki](https://github.com/qbittorrent/search-plugins/wiki/Install-search-plugins).

Some plugins can need some settings, please read carefully the *Notes* section.

## :book: Notes

- **IlCorsaroNero** has been blacklisted on Italy's DNS, please **use a different DNS such as Google or Cloudflare**
- **AcademicTorrents** is protected by CloudFlare, so vanilla Python 3 is not suitable to scrap this engine. The plugin
  uses the official AcademicTorrents' API **but** by default requests without a _API KEY_ are limited to only 20
  results.

      To use properly AcademicTorrents' plugins, please register an account on their website and paste your UID and API_KEY
      inside the python file, you can find on the head two empty strings to fill by yourself.

## Contributions and Testing

To contribute, just write your own script following
the [official wiki](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin#python-class-file-structure)
and put it inside `/src/engines`.

For comodity I have included the needed files requires to testing the plugins, the nova scripts:

1. `cd ./src`
2. > python ./nova2.py **search_engine** **category** **search keywords**

## :warning: License

This collection is under GNU GPL-3.0 License.
