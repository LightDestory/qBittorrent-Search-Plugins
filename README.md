<a name="readme-top"></a>

<!-- Presentation Block -->
<br />

<div align="center">

  <a href="https://github.com/LightDestory/qBittorrent-Search-Plugins">
    <img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/presentation_image.png" alt="Preview" width="90%">
  </a>

  <h2 align="center">qBittorrent Search Plugins</h2>
  
  <p align="center">
      A growing collection of search plugins for the qBittorrent, an awesome and opensource torrent client.
  </p>
  
  <br />
  <br />

</div>

<!-- ToC -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#book-about-the-project">📖 About The Project</a>
    </li>
    <li>
      <a href="#gear-getting-started">⚙️ Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#plugin-list">Plugin List</a></li>
        <li><a href="#notes">Notes</a></li>
        <li><a href="#developer-notes">Developer Notes</a></li>
      </ul>
    </li>
    <li><a href="#dizzy-contributing">💫 Contributing</a></li>
    <li><a href="#handshake-support">🤝 Support</a></li>
    <li><a href="#warning-license">⚠️ License</a></li>
    <li><a href="#hammer_and_wrench-built-with">🛠️ Built With</a></li>
  </ol>
</details>

<!-- About Block -->

## :book: About The Project

This repository contains various search engine plugins that I developed for qBittorrent, an amazing and open source torrent client.

If you want to request a specific plugin or a existing one stops working, please let me know by opening an issue.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Setup Block -->

## :gear: Getting Started

These plugins are unofficial, so you must install them manually.

Due to qBittorrent behavior, to update unofficial plugins you must check this repository periodically or wait until a plugin stops working for you.

_If you want improve such behavior, please help me reaching qBittorrent's developer by upvoting: [Improve Plugin Manager behavior](https://github.com/qbittorrent/qBittorrent/issues/17445)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

There are 2 ways to install unofficial plugins:

- The easier way is to copy the link of the "Download" table's column and use it as "web link" for qBittorrent.

- The other way is to save the file in a temporary location by going to the download link and saving the document as a **python file**, `.py`. Then you can install the plugin by selecting the file from your filesystem.

Some plugins may need additional settings to work properly, please read carefully the _Notes_ section.

For any doubts about the installation process, please refer to the official wiki: [Install search plugins](https://github.com/qbittorrent/search-plugins/wiki/Install-search-plugins).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Plugin List

| Plugin                                                                   | Type          | Version (Updated)        | Working?                 | Download                                                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------ | ------------- |--------------------------| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ![AcademicTorrents](./src/engines/academictorrents.png) AcademicTorrents | Torrent Index | **1.2** - _(19/03/2023)_ | :heavy_check_mark:       | <div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/academictorrents.py)</div>                                                                        |
| ![btetree](./src/engines/btetree.png) btetree                            | Torrent Index | **1.3** - _(19/03/2023)_ | :heavy_check_mark:       | <div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/btetree.py)</div>                                                                                 |
| ![ETTV](./src/engines/ettv.png) ETTV                                     | Torrent Index | **1.2** - _(17/06/2021)_ | :heavy_multiplication_x: | <div align=center>Site Down :cry: <br> [<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/ettv.py) </div>                                                                         |
| ![GloTorrents](./src/engines/glotorrents.png) GloTorrents                | Torrent Index | **1.6** - _(19/03/2023)_ | :heavy_check_mark:       | <div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/glotorrents.py)</div>                                                                             |
| ![IlCorsaroNero](./src/engines/ilcorsaronero.png) IlCorsaroNero          | Torrent Index | **1.5** - _(19/04/2023)_ | :heavy_check_mark:       | <div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/ilcorsaronero.py)</div>                                                                           |
| ![Kickasstorrents](./src/engines/kickasstorrents.png) Kickasstorrents    | Torrent Index | **1.1** - _(19/03/2023)_ | :question:       | <span>KATCR is using cloudflare, the plugin will not when CF is active. So the plugin is unstable and will work only when CF is set to low threats.</span> <br/><div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/kickasstorrents.py)</div>                                                                         |
| ![Nitro](./src/engines/nitro.png) Nitro                                  | Torrent Index | **1.0** - _(29/07/2022)_ | :heavy_multiplication_x: | <div align=center> Site Down since 9/11/22 :cry: <br> [<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/nitro.py)</div>                                               |
| ![Pirateiro](./src/engines/pirateiro.png) Pirateiro                      | Aggregator    | **1.0** - _(28/07/2022)_ | :heavy_multiplication_x: | <div align=center> Site Down :cry: <br> [<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/pirateiro.py)</div>                                                         |
| ![RARBG](./src/engines/rarbg.png) RARBG                                  | Torrent Index | **1.1** - _(06/12/2021)_ | :heavy_multiplication_x: | <div align=center>My implementation is not working anymore, the following links to the official working one<br>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/rarbg.py)</div> |
| ![RockBox](./src/engines/rockbox.png) RockBox                            | Torrent Index | **1.1** - _(19/03/2023)_ | :heavy_check_mark:       | <div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/rockbox.py)</div>                                                                                 |
| ![Snowfl](./src/engines/snowfl.png) Snowfl                               | Aggregator    | **1.3** - _(28/07/2022)_ | :heavy_check_mark:       | <div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/snowfl.py)</div>                                                                                  |
| ![ThePirateBay](./src/engines/thepiratebay.png) ThePirateBay             | Torrent Index | **1.1** - _(19/03/2023)_ | :heavy_check_mark:       | <div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/thepiratebay.py)</div>                                                                            |
| ![TNTVillageDump](./src/engines/tntvillagedump.png) TNTVillageDump       | Static Dump   | **1.1** - _(31/01/2022)_ | :heavy_check_mark:       | <div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/tntvillagedump.py)</div>                                                                          |
| ![TorrentDownload](./src/engines/torrentdownload.png) TorrentDownload    | Aggregator    | **1.0** - _(28/07/2022)_ | :heavy_multiplication_x: | <div align=center> Stopped offering DL :cry: <br> [<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/torrentdownload.py)</div>                                         |
| ![YourBittorrent](./src/engines/yourbittorrent.png) YourBittorrent       | Torrent Index | **1.3** - _(22/02/2022)_ | :heavy_check_mark:       | <div align=center>[<img src="https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/dl_image.png" width=32>](https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/yourbittorrent.py)</div>                                                                          |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Notes

- **IlCorsaroNero** has been blacklisted on Italy's DNS, please **use a different DNS such as Google or Cloudflare**
- **AcademicTorrents** please set "Search in" properly!
- **Torrent aggregators** mix multiple torrent indexes, I tried to implement the most generic torrent/magnet fetch but
  sometime it fails
- **RARBG** uses an anti-spam system, for most of the time my implementation will not work, use the official plugin
  based on torrentapi.
- **TNTVillage** uses an embeded dump, so it is a bit fatty: 20MB of plugin!
- **YourBittorrent** by default the website only shows 50 torrent based on your text-query, I tried to force pagination
  but it causes duplicates results. So... use specific queries!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Developer Notes

If you want to create a new search engine, please refer to the [official wiki](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin#python-class-file-structure)
and put it inside `/src/engines`.

For commodity, I have included the needed files requires to testing the plugins, the nova scripts:

1. `cd ./src`
2. > python ./nova2.py **search_engine** **category** **search keywords**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Contribute Block -->

## :dizzy: Contributing

If you are interested in contributing, please refer to [Contributing Guidelines](.github/CONTRIBUTING.md) for more information and take a look at open issues. Ask any questions you may have and you will be provided guidance on how to get started.

Thank you for considering contributing.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Support Block -->

## :handshake: Support

If you find value in my work, please consider making a donation to help me create, and improve my projects.

Your donation will go a long way in helping me continue to create free software that can benefit people around the world.

<p align="center">
<a href='https://ko-fi.com/M4M6KC01A' target='_blank'><img src='https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/.github/assets/images/support.png' alt='Buy Me a Hot Chocolate at ko-fi.com' width="45%" /></a>
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- License Block -->

## :warning: License

The content of this repository, except the nova scripts by qBittorrent devs, is distributed under the GNU GPL-3.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Built With Block -->

## :hammer_and_wrench: Built With

- [Python](https://www.python.org/)
- [Regex](https://en.wikipedia.org/wiki/Regular_expression)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
