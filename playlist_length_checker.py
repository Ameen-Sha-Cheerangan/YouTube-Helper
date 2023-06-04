from googleapiclient.discovery import build
import os
import re

url = input("Enter the youtube url : ")

api_key = os.environ.get('YouTube_API')
service = build('youtube', 'v3', developerKey=api_key)

playlistid_pattern = re.compile(r'[\?|&](list=)([\w-]*)\&?')
pid = playlistid_pattern.search(url)
pid = pid.group(2)
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')
nextPageToken = None
totaltime = 0

pl_request = service.playlists().list(
        part='contentDetails',
        id=pid,
    )
pl_response = pl_request.execute()
playlist = pl_response['items'][0]
video_count = playlist['contentDetails']['itemCount']
print(f"There are {video_count} videos in the playlist")

qn = input("Do you want to specify starting and ending index (y|N)")
no_of_videos = 1000
starting_index = 0
if qn=="y" or qn=="Y":
    starting_index = int(input("Enter the starting index : "))
    ending_index = int(input("Enter the ending index : "))
    no_of_videos = ending_index - starting_index + 1


while True:

    if no_of_videos <= 0:
        break
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
        if starting_index > 0:
            starting_index-=1
            continue
        duration = item['contentDetails']['duration']
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        length = seconds + minutes*60 + hours*3600
        totaltime += length
        no_of_videos -= 1
        if no_of_videos <=0:
            break
    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:  # for the last page this will give None
        break

hh = totaltime//3600
totaltime = totaltime % 3600
mm = totaltime//60
totaltime = totaltime % 60
ss = totaltime
print(hh, " hours,", mm, " minutes,", ss, " seconds")
