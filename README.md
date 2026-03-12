## mprand
Play random songs within your MPD database. 

Project focus is to be as simple and stupid as possible.

This script was inspired by oldlaptop's [mprand](https://github.com/oldlaptop/mprand) script, written in Tcl, which isn't simple (in a bad way) nor stupid. Thanks to him for his help and inspiration.

## Install

Install the dependency first.

### Arch Linux

```bash
pacman -S python-mpd2
```

### FreeBSD

```bash
pkg install py311-python-mpd2
```

Then install the script:

```bash
sudo make install
```

---

## Usage

Make sure MPD is running, then run:

```bash
mprand
```

Behavior:

- If MPD is **not playing**, it will start playback.
- If the playlist is **empty**, it will enqueue two songs.
- If the playlist already contains songs, it will only enqueue a new one when you reach the **last or second-to-last track**.

### Options

```
-q, --quiet            Disable logging output
-s, --host HOST        MPD host (default: localhost)
-p, --port PORT        MPD port (default: 6600)
-h, --help             Show help and exit
-P, --password         MPD password (if required)
```


## Contributing
If you find any bugs or think you know a way to improve my shitty code, feel free to create a pull request or something idk.

You can also find me on irc (libera.chat) @ repoman

and on Telegram @repomansez

## Dependencies
[python-mpd2](https://github.com/Mic92/python-mpd2)

## Video example of usage with ncmpcpp


https://github.com/repomansez/mprand/assets/62445306/ddb3cb6c-3dd7-4688-a5a7-446b1d1eb949


## Known bugs
crash if cleaning the playlist more than once, too lazy to fix it rn
