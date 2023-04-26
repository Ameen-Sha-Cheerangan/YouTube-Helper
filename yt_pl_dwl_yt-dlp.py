#done with 319 songs

import yt_dlp

from googleapiclient.discovery import build
import os
import unicodedata
import re

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
        f = open("not_downloaded.txt","a")
        f.write(link+"\n")
        f.close()
    print()
    print()

url = input("Enter the youtube url : ")
api_key = os.environ.get('YouTube_API')
service = build('youtube', 'v3', developerKey=api_key)

# We can find playlist id

playlistid_pattern = re.compile(r'[\?|&](list=)([\w-]*)\&?')
pid = playlistid_pattern.search(url)
pid = pid.group(2)
nextPageToken = None

x = 0
done = 51

while True:

    pl_request = service.playlistItems().list(
        part='contentDetails',
        playlistId=pid,
        maxResults=50,
        pageToken=nextPageToken
    )
    pl_response = pl_request.execute()
    for item in pl_response['items']:
        if done>0:
            done-=1
        else:
            # print(item['contentDetails']['videoId'])
            vidId = item['contentDetails']['videoId']
            yt_link = f'https://youtu.be/{vidId}'
            print(x,yt_link)
            downloadmp3(yt_link)
            x+=1
    
    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:  # for the last page this will give None
        break

print(f'Downloaded {x} mp3 files')
