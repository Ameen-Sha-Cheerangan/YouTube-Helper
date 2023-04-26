# downloaded first 319 songs

from googleapiclient.discovery import build
from pytube import YouTube
from pytube.cli import on_progress
import os
import unicodedata
import re


# An easier method to download
#         ydl_opts = {
#                     'format': 'bestaudio/best',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#         }
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download(link)





def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def downloadmp3(link):
    try:
        youtube_1 = YouTube(link, on_progress_callback=on_progress)
        # print("Title of the video : ", youtube_1.title) Doesn't work if there is some arabic
        audios = youtube_1.streams.filter(type="audio").order_by('abr').desc()
        title=youtube_1.title
        title = slugify(title)
        if(os.path.exists(f'./{title}.mp3')==False):
            audios.first().download(filename=f"{title}.mp3")
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
done = 307

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
