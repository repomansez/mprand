## mprand
Play random songs within your MPD database. 

Project focus is to be as simple and stupid as possible.

This script was inspired by oldlaptop's [mprand](https://github.com/oldlaptop/mprand) script, written in Tcl, which isn't simple (in a bad way) nor stupid. Thanks to him for his help and inspiration.
## Usage
Just have MPD running and run the script.

If mpd is not playing, it'll start playing, if the playlist is empty, it'll enqueue two songs, if the playlist is not empty it'll only enqueue a new song if you're on the last or second to last song of the playlist.

## Contributing
If you find any bugs or think you know a way to improve my shitty code, feel free to create a pull request or something idk.

You can also find me on irc (libera.chat) @ repoman

## Dependencies
[python-mpd2](https://github.com/Mic92/python-mpd2)
