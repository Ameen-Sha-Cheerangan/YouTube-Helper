
from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg

link = input("Enter the url of the video : ")
youtube_1 = YouTube(link, on_progress_callback=on_progress)
print(youtube_1.thumbnail_url)
print("Title of the video : ", youtube_1.title)
audios = youtube_1.streams.filter(type="audio").order_by('abr').desc()
for audio in audios:
    print(audio)
audios.first().download(filename=f"{youtube_1.title}.mp3")
videos = youtube_1.streams.filter(
    type="video", progressive=False).order_by('resolution').desc()
videos.first().download(filename=f"{youtube_1.title}.mp4")
video_stream = ffmpeg.input(f"{youtube_1.title}.mp4")
audio_stream = ffmpeg.input(f"{youtube_1.title}.mp3")
video_name = youtube_1.title+" (merged).mp4"
print(video_name)
ffmpeg.output(audio_stream, video_stream, video_name).run()
