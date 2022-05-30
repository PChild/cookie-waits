from playsound import playsound
from urllib.parse import urlparse
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from spleeter.separator import Separator
import os

separator = Separator('spleeter:2stems')
SONGS_DIR = 'songs/'


def is_url(item):
    return bool(urlparse(item).scheme)


def get_title(item):
    if item[-4:] == 'song':
        return item[:-5]
    else:
        return item


def get_song_fp(item):
    return SONGS_DIR + get_title(song) + '.mp3'


def fetch_song(item, force=False):
    search = VideosSearch(item, limit=1).result()['result'][0]
    if is_url(item):
        # noinspection PyTypeChecker
        title = search['title']
        to_fetch = item
    else:
        title = get_title(item)
        # noinspection PyTypeChecker
        to_fetch = search['link']

    file_path = get_song_fp(title)

    dl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    if force or not os.path.exists(file_path):
        YoutubeDL(dl_opts).extract_info(to_fetch)
    else:
        print('Using saved version of song:  ', title)


def delete_song(name):
    os.remove(get_song_fp(name))


def process_song(item):
    print(item)
    separator.separate_to_file(get_song_fp(item), 'splits/')


if __name__ == '__main__':
    song = 'culture of fear song'
    print(get_song_fp(song))
    #fetch_song(song)
    #process_song(song)
    #playsound(get_song_fp(song))
