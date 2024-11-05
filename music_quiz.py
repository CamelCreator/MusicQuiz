import json
import re
from moviepy.editor import AudioFileClip, ColorClip, CompositeAudioClip, \
    CompositeVideoClip, concatenate_videoclips, ImageClip, TextClip, \
    VideoFileClip
from pytubefix import YouTube
import pandas
import requests
from config import get_config


def youtube_to_mp3(youtube_url, output_path, start=0, end=20):
    yt = YouTube(youtube_url)
    video_stream = yt.streams.filter(only_audio=True).first()
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


def download_image(image_url, image_path='./temp'):
    if image_url is None:
        image_url = None  # put backup image here
    img_data = requests.get(image_url, timeout=10).content
    with open(image_path, 'wb') as handler:
        handler.write(img_data)


def main():
    config = get_config()
    temp_path = config.get('paths', 'temp_path')
    output_path = config.get('paths', 'output_path')
    data_location = config.get('paths', 'data_location')

    video_width = int(config.get('music_quiz', 'video_width'))
    video_height = int(config.get('music_quiz', 'video_height'))

    guess_length = int(config.get('music_quiz', 'guess_length'))
    answer_length = int(config.get('music_quiz', 'answer_length'))
    total_length = guess_length + answer_length

    boxart_api = config.get('music_quiz', 'boxart_api')
    timer_clip_path = config.get('paths', 'timer_clip_path')

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
            fontsize=int(
                .105 * video_height),
            color='white',
            method="caption",
            size=(
                video_width,
                video_height),
            stroke_color='black').set_duration(answer_length).set_pos('center')
        num_text = '# ' + str(video_index + 1) + ' / ' + str(total_videos)

        image_path = temp_path + 'img_' + re.sub(r'[^\w]', '', game_name)
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
            answer_length).set_opacity(.6).set_pos('center')
        imageclip = imageclip.resize((int(video_width / 2.4), video_height))
        black_bg = ColorClip(
            size=(
                video_width, video_height), color=(
                0, 0, 0)).set_duration(answer_length)
        answerclip = CompositeVideoClip([black_bg, imageclip, textclip_answer])

        video_clip = VideoFileClip(timer_clip_path).resize(
            height=video_height, width=video_width)
        number_clip = TextClip(num_text,
                               fontsize=int(.095 * video_height),
                               color='white').set_pos((5,
                                                       5)).set_duration(guess_length)
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
