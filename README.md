# MusicQuiz.py

## Usage
1. Install dependencies (virtualenv recommended)
1. Run `python MusicQuiz.py`

Video will be output to `output/MusicQuiz.mp4`.

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
