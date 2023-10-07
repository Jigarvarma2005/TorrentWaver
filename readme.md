# TorrentWaver 

This is a simple web-based aria2p downloader built using python. It allows users to add and monitor the progress of downloading torrent magnet links and get direct download URL of it.

## Features

- Username and Password based login
- Add torrent magnet links for downloading
- Monitor the progress of downloads in real-time
- Automatic refresh of download status
- Pause or Resume the download
- Cancel the download
- Download files are saved in a designated downloads folder
- Access of files only to authenticated users


## ToDo
- [ ] File Cleanup
- [x] Download Cancel
- [x] User Login (maybe)
- [ ] Admin page for managing users

## Requirements

- Python 3.x
- Aria2c (command-line tool)

## Installation

1. Setup

   ```
   #Install command-line tools
   sudo apt-get install aria2 python3 git curl nano
   
   #Clone the repo
   git clone https://github.com/Jigarvarma2005/TorrentWaver.git
   
   #Navigate to the project directory
   cd TorrentWaver

   #Fill the config variables
   nano configs.py
   
   #Install the required Python packages
   pip install -r requirements.txt
   ```

2. Start
   ```
   python3 app.py
   ```

## Customization

    - To customize the appearance and layout of the web interface, modify the HTML templates in the templates folder.

## Manage Users
   ```
   python3 manage.py
   ```

## Follow on:
<p align="left">
<a href="https://github.com/Jigarvarma2005"><img src="https://img.shields.io/badge/GitHub-Follow%20on%20GitHub-inactive.svg?logo=github"></a>
</p>
<p align="left">
<a href="https://twitter.com/Jigarvarma2005"><img src="https://img.shields.io/badge/Twitter-Follow%20on%20Twitter-informational.svg?logo=twitter"></a>
</p>
<p align="left">
<a href="https://instagram.com/Jigarvarma2005"><img src="https://img.shields.io/badge/Instagram-Follow%20on%20Instagram-important.svg?logo=instagram"></a>
</p>

### Support Group
- [JV Community](https://t.me/jv_community)

## Credits
- [Jigar Varma (me)](https://github.com/jigarvarma2005)

