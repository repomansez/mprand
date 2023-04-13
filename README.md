## mprand
Play random songs within your MPD database.

This script was inspired by oldlaptop's [mprand](https://github.com/oldlaptop/mprand) script, written in Tcl, thanks to him for his help and inspiration.
## Usage
Just have MPD running and run the script.

If mpd is not playing, it'll start playing, if the playlist is empty, it'll enqueue two songs, if the playlist is not empty it'll only enqueue a new song if you're on the last or second to last song of the playlist.

## Dependencies
[python-mpd2](https://github.com/Mic92/python-mpd2)
