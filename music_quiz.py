import json
import re
from moviepy.editor import AudioFileClip, ColorClip, CompositeAudioClip, \
    CompositeVideoClip, concatenate_videoclips, ImageClip, TextClip, \
    VideoFileClip
from pytubefix import YouTube
import pandas
import requests


def youtube_to_mp3(youtube_url, output_path, start=0, end=20):
    yt = YouTube(youtube_url)
    video_stream = yt.streams.first()
    downloaded_file = video_stream.download(output_path=output_path)
    mp3_audio = AudioFileClip(downloaded_file).subclip(start, end)
    return mp3_audio


def grab_boxart(game_name, boxart_api):
    result = requests.get(boxart_api + game_name, timeout=10).text
    result = json.loads(result)

    game_names = [re.sub(r'[^\w]', '', a['name']) for a in result]
    truncated_game_name = re.sub(r'[^\w]', '', game_name)
    if truncated_game_name in game_names:
        image_url = result[game_names.index(truncated_game_name)]['cover']
    else:
        image_url = result[0]['cover']
        print('No exact game name match for ' + truncated_game_name)

    return image_url


def download_image(image_url, image_path):
    if image_url is None:
        image_url = None  # put backup image here
    img_data = requests.get(image_url, timeout=10).content
    with open(image_path, 'wb') as handler:
        handler.write(img_data)


def main():
    temp_path = './temp/'  # directory to download assets to
    output_path = './output/'  # output directory
    data_location = 'input.csv'

    video_width = 640
    video_height = 360

    guess_length = 15
    answer_length = 5
    total_length = guess_length + answer_length

    boxart_api = 'https://api.topsters.org/api/igdb/search/'
    timer_clip_path = 'timer.mp4'

    data = pandas.read_csv(data_location)
    total_videos = len(data['url'])

    audio_clips = []
    vidlist = []

    for video_index in range(total_videos):
        start = data['start'][video_index]
        end = start + total_length
        url = data['url'][video_index]
        game_name = data['game'][video_index]
        song_name = data['song'][video_index]

        mp3 = youtube_to_mp3(url, output_path=temp_path, start=start, end=end)
        mp3 = mp3.set_start(video_index * total_length)
        audio_clips.append(mp3)

        answer = game_name + '\n' + song_name
        textclip_answer = TextClip(
            answer,
            fontsize=38,
            color='white',
            method="caption",
            size=(
                video_width,
                video_height),
            stroke_color='black').set_duration(answer_length).set_pos('center')
        num_text = '#' + str(video_index + 1) + ' / ' + str(total_videos)

        image_path = temp_path + 'img_' + game_name
        if 'img' in data and str(data['img'][video_index]) != 'nan':
            download_image(
                data['img'][video_index],
                image_path=image_path)  # Allow custom thumbnails
        else:
            download_image(
                grab_boxart(
                    game_name,
                    boxart_api),
                image_path=image_path)

        imageclip = ImageClip(image_path).set_duration(
            answer_length).set_opacity(.6).set_pos('center').resize((264, 352))
        black_bg = ColorClip(
            size=(
                video_width, video_height), color=(
                0, 0, 0)).set_duration(answer_length)
        answerclip = CompositeVideoClip([black_bg, imageclip, textclip_answer])

        video_clip = VideoFileClip(timer_clip_path).resize(
            height=video_height, width=video_width)
        number_clip = TextClip(
            num_text, fontsize=34, color='white').set_pos(
            (10, 10)).set_duration(guess_length)
        guessing_clip = CompositeVideoClip([video_clip, number_clip])
        guessing_clip.audio = mp3

        vidlist.append(guessing_clip)
        vidlist.append(answerclip.crossfadein(0.4))

    # Audio quiz
    audio_quiz = CompositeAudioClip(audio_clips)
    audio_quiz.write_audiofile(output_path + 'MusicQuiz.mp3', fps=44100)

    # Video quiz
    video_quiz = concatenate_videoclips(vidlist, method='compose')
    video_quiz.write_videofile(output_path + 'MusicQuiz.mp4')


if __name__ == "__main__":
    main()
