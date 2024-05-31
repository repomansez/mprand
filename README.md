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

and on Matrix @sbctani:matrix.sussywebsite.xyz

## Dependencies
[python-mpd2](https://github.com/Mic92/python-mpd2)

## Video example of usage with ncmpcpp
https://github.com/repomansez/mprand/assets/62445306/10f4deb3-71b5-4fdf-8abc-d64a226c256a

## Known bugs
If you skip songs too fast, you outpace MPD itself and playback stops, which causes mprand to crash. Workaround for that is to just stop your brainrotten zoomer ass from skipping songs too fast.
