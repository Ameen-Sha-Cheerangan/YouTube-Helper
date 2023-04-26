import yt_dlp
from pytube import YouTube
from pytube.cli import on_progress
import re
import os

import unicodedata


def downloadmp3(link):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'trim_file_name': 50, 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],     
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(link)
    except(Exception):
        print("Not Downloaded", link)
        f = open("still_not.txt","a")
        f.write(link+"\n")
        f.close()
    print()
    print()

done = 0
file1 = open("not_downloaded.txt", "r")
count = 0

while True:
    count += 1 
    line = file1.readline()
    # if line is empty
    # end of file is reached
    if not line:
        break
    yt_link = line.strip()
    print(count ,yt_link)
    downloadmp3(yt_link)
file1.close()

print(f'tried downloading {count} mp3 files')
