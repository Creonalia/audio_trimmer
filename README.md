# audio_trimmer

Command line program to trim silence from the start and end of audio files.
Mainly just using to get rid of silence from music.

## Setup and usage

Only dependency is pydub. Accepts an arbitrarily long list of files and a few other arguments. By default it will not trim anything, use -l/--leading and -t/--trailing to trim leading and trailing silence.

```bash
# remove trailing silence from all mp3 files in working directory
$ python3 trimmer.py -t *.mp3
```
