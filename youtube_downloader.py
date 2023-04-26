# prerequisite : run pip install pytube

from pytube import YouTube
from pytube.cli import on_progress

link = input("Enter the url of the video : ")
youtube_1 = YouTube(link, on_progress_callback=on_progress)
# print(youtube_1.thumbnail_url)
# print("Title of the video : ", youtube_1.title)
# videos = youtube_1.streams
# print("What do you want ?")
# print("1. Video \n2. Audio \n3. Both")
# option = int(input(("Enter the option : ")))
# if (option == 1):
#     videos = youtube_1.streams.filter(type="video")
# elif (option == 2):
#     videos = youtube_1.streams.filter(type="audio")
# else:
#     videos = youtube_1.streams.all()
videos = youtube_1.streams
# highresvid = youtube_1.streams.get_highest_resolution()
# highresvid.download()
x = 0
for video in videos:
    print(x, video)
    x += 1
no = int(input("Enter the option to download :"))
videos[no].download()
