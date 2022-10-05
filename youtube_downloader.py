# prerequisite : run pip install pytube

from pytube import YouTube
from pytube.cli import on_progress
link = input("Enter the url of the video : ")
youtube_1 = YouTube(link, on_progress_callback=on_progress)
print(youtube_1.thumbnail_url)
print("Title of the video : ", youtube_1.title)
videos = youtube_1.streams
# videos = youtube_1.streams.filter(only_audio="True")
print("What do you want ?")
print("1. Video \n2. Audio \n3. Both")
option = int(input(("Enter the option : ")))
if (option == 1):
    videos = youtube_1.streams.filter(type="video")
elif (option == 2):
    videos = youtube_1.streams.filter(type="audio")
else:
    videos = youtube_1.streams.all()
vid = list(enumerate(videos))
for video in vid:
    print(video)
no = int(input("Enter the option to download :"))
videos[no].download()
