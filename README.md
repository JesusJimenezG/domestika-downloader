# Domestika downloader

This is a simple python script to download Domestika courses using ffmpeg. (You need to have access to the course you want to download)

## Requirements
- Python 3
- ffmpeg

## Installation

1. Clone the repository
```bash
git clone
```

2. Install the requirements
```bash
pip install -r requirements.txt
```

3. Install ffmpeg
```bash
sudo apt install ffmpeg
```

## Usage

1. In the page of the course you want to download, open the developer tools and go to the network tab. For each video, press play button and filter the requests by "m3u8" or "master". You can copy each link and save it in a file or have the developer tools open while running the script.
2. Run the script, it'll ask for the course name (folder where the videos will be saved) the name of the course (file name, do not include extension) and the links to the master's m3u8 files. NOTE: do not add the query parameters to the link.
3. If you want to download subtitles, go to the network tab and filter by "playlist", you'll see several requests with "playlist.m3u8". Inspect each one and look for the one with "subtitles" in the path (usually with the format "/subtitles/en/playlist.m3u8"). Copy the link and paste it when the script asks for it. NOTE: do not add the query parameters to the link.
4. The script will download the videos and subtitles in the same folder where the script is located in a courses folder and a folder with the course name.
5. Select "y" if you want to download another video for the same course, "n" if you want to download another course, you must run the script again.

## TODOs

This was a quick script I made to download a course I bought, so it's not perfect. Here are some things I'd like to improve:

- [ ] Best case scenario would be to automate the process of getting the m3u8 links from the course page.
- [ ] Otherwise, add support for downloading multiple videos and subtitles if needed at once.

## Disclaimer

This script is for offline access to the courses you have bought. You must have access to the course you want to download. I do not support piracy.