# music_quiz.py

## Usage
1. Install dependencies (virtualenv recommended, in `env` directory)
1. Run `python music_quiz.py`

Output:
- video: `output/MusicQuiz.mp4`
- audio-only: `output/MusicQuiz.mp3`

## Set up
Place `input.csv` and `timer.mp4` at the root of this directory.

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
