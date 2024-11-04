# music_quiz.py

## Usage
1. Install dependencies (virtualenv recommended, in `env` directory)
1. Run `python music_quiz.py`

Output:
- video: `output/MusicQuiz.mp4`
- audio-only: `output/MusicQuiz.mp3`

## Set up
Place `input.csv` and `timer.mp4` at the root of this directory.

### config.ini
`config.default.ini` contains default variables for the project and is committed to source control. To override any of these, create `config.ini` with the values you wish to override.\
Said another way, `config.ini` is not committed to source control, so default settings should go in `config.default.ini` and custom changes should go in `config.ini`.

### input.csv format
|column|description|
|---|---|
|url|youtube link|
|start|starting timestamp in seconds|
|game|game name to display|
|song|song name to display|
|img|image to display (will fallback to searched cover art if empty)|

### timer.mp4
the timer video to display during the song countdown
