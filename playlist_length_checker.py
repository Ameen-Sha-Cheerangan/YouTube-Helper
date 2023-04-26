from googleapiclient.discovery import build
import os
import re

url = input("Enter the youtube url : ")
api_key = os.environ.get('YouTube_API')
service = build('youtube', 'v3', developerKey=api_key)


# pl_request = service.playlists().list(
#     part='snippet',
#     channelId='UCCezIgC97PvUuR4_gbFUs5g')
# pl_response = pl_request.execute()
# print(pl_response)
# for item in pl_response['items']:
#     print(item)
#     print()

# We can find playlist id

playlistid_pattern = re.compile(r'[\?|&](list=)([\w-]*)\&?')
pid = playlistid_pattern.search(url)
pid = pid.group(2)
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')
nextPageToken = None
totaltime = 0

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
    # print(','.join(list_vid))
    vid_request = service.videos().list(
        part='contentDetails',
        id=','.join(list_vid)  # possible to only about 50 videos
    )
    vid_response = vid_request.execute()
    # this will only have five videos of the playlist
    for item in vid_response['items']:
        duration = item['contentDetails']['duration']
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)
        hours = int(hours.group(1)) if hours else 0
        # Similiar to
        # if hours:
        #     hours = int(hours.group(1))
        # else:
        #     hours = 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        length = seconds + minutes*60 + hours*3600
        totaltime += length
    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:  # for the last page this will give None
        break

hh = totaltime//3600
totaltime = totaltime % 3600
mm = totaltime//60
totaltime = totaltime % 60
ss = totaltime
print(hh, " hours,", mm, " minutes,", ss, " seconds")
