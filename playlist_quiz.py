from random import uniform
from pytubefix import Playlist, YouTube
import pandas

def main():
    playlist_url = ''

    playlist = Playlist(playlist_url)

    output_data = []
    for youtube_url in playlist:
        yt = YouTube(youtube_url)
        title = yt.title
        thumbnail = yt.thumbnail_url

        if yt.length >= 30:
            timestart = int(uniform(0, yt.length - 30))
        else:
            timestart = 0

        output_data += [{'url': youtube_url, 'start': timestart,
                         'game': title, 'song': ' ', 'img': thumbnail}]

    pandas.DataFrame(output_data).to_csv('input.csv', index=False)


if __name__ == "__main__":
    main()
