from googleapiclient.discovery import build
import os
import re

url = input("Enter the youtube url : ")
api_key = os.environ.get('YouTube_API')
service = build('youtube', 'v3', developerKey=api_key)

playlistid_pattern = re.compile(r'[\?|&](list=)(\w*)\&?')
pid = playlistid_pattern.search(url)
pid = pid.group(2)
videos = []
nextPageToken = None
while True:
    pl_request = service.playlistItems().list(
        part='contentDetails',
        playlistId=pid,
        maxResults=50,
        pageToken=nextPageToken
    )
    pl_response = pl_request.execute()
    list_vid = []  # This is created so as to reduce the api calls . to not call for each vid_id
    for item in pl_response['items']:
        list_vid.append(item['contentDetails']['videoId'])
    vid_request = service.videos().list(
        part='statistics',
        id=','.join(list_vid)  # possible to only about 50 videos
    )
    vid_response = vid_request.execute()
    # this will only have five videos of the playlist
    for item in vid_response['items']:
        vidId = item['id']
        views = int(item['statistics']['viewCount'])
        yt_link = f'https://youtu.be/{vidId}'
        videos.append(
            {
                'views': views,
                'url': yt_link
            }
        )
    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:  # for the last page this will give None
        break

videos.sort(key=lambda vid: vid['views'], reverse=True)
for video in videos:
    print(video['views'], video['url'])
