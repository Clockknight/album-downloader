<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
<a href="https://github.com/Clockknight/album-downloader">
<h3 align="center">Album Downloader
</h3></a>

  <p align="center">
    Python based script that downloads discographies and applies tags according to Discogs
    <br />
    <a href="https://github.com/Clockknight/album-downloader"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Clockknight/album-downloader">View Demo</a>
    ·
    <a href="https://github.com/Clockknight/album-downloader/issues">Report Bug</a>
    ·
    <a href="https://github.com/Clockknight/album-downloader/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://Clockknight.github.io)

Code has various modes to find songs to download, and tag based on information on [Discogs.com](https://discogs.com). When using Cache or Search Modes, mp3s downloaded should have 
* Album Name
* Album Artwork
* Song Name
* Track Number
* Artist Name

In the mp3 file. Also has url mode to support downloading a YouTube video as an mp3 directly, and Update will check for previously undownloaded releases from any artists that you've used this script for before.  

For more projects, check out my [github.io](http://clockknight.github.io).

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [eyed3](https://pypi.org/project/eyed3/)
* [urllib](https://urllib3.readthedocs.io/en/stable/)
* [pytube](https://github.com/pytube/pytube)
* [requests](https://docs.python-requests.org/en/latest/)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
* [moviepy](https://zulko.github.io/moviepy/)
* [json](https://docs.python.org/3/library/json.html)
* [shutil](https://docs.python.org/3/library/shutil.html)
* [regex](https://docs.python.org/3/library/re.html)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow these simple example steps.

Currently working on getting a release. Current version can be hard to work with:

1. Be sure python and all the above libraries are installed

2. Run the script

3. Search an artist or release on [Discogs](https://Discogs.com) - results are pulled directly from that site. 

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

Available on the [Trello Board](https://trello.com/b/iQFpYHnQ).

See the [open issues](https://github.com/Clockknight/album-downloader/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - tylerf2wang@gmail.com

Project Link: [https://github.com/Clockknight/album-downloader](https://github.com/Clockknight/album-downloader)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Clockknight/album-downloader.svg?style=for-the-badge
[contributors-url]: https://github.com/Clockknight/album-downloader/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Clockknight/album-downloader.svg?style=for-the-badge
[forks-url]: https://github.com/Clockknight/album-downloader/network/members
[stars-shield]: https://img.shields.io/github/stars/Clockknight/album-downloader.svg?style=for-the-badge
[stars-url]: https://github.com/Clockknight/album-downloader/stargazers
[issues-shield]: https://img.shields.io/github/issues/Clockknight/album-downloader.svg?style=for-the-badge
[issues-url]: https://github.com/Clockknight/album-downloader/issues
[license-shield]: https://img.shields.io/github/license/Clockknight/album-downloader.svg?style=for-the-badge
[license-url]: https://github.com/Clockknight/album-downloader/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/tyler-wang-b3241963
[product-screenshot]: assets/screenshot.png