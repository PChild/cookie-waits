from playsound import playsound
from urllib.parse import urlparse
from youtube_search import YoutubeSearch
import youtube_dl
import webrtcvad

vad = webrtcvad.Vad(3)


def is_url(item):
    return bool(urlparse(item).scheme)


def fetch_video(item):
    if is_url(item):
        to_fetch = item
    else:
        to_fetch = 'https://www.youtube.com' + YoutubeSearch(item, max_results=1).videos[0]['link']

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': item + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([to_fetch])


def process_song(item):
    print(item)


if __name__ == '__main__':
    song = 'caught a ghost'
    fetch_video(song)
    # playsound(song + '.mp3')
