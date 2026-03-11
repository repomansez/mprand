#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# mprand - play random songs within your MPD database

# Copyleft (C) 2025 repomansez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from mpd import (MPDClient, CommandError, ConnectionError)
from random import choice
from socket import error as SocketError
import getpass
import sys
import logging
import argparse

def parse_args(): # If you wish to change any default setting, change the value in here
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--quiet", "-q", action="store_true")
    parser.add_argument("--host", "-s", default="localhost")
    parser.add_argument("--port", "-p", type=int, default=6600)
    parser.add_argument("--help", "-h", action="store_true")
    parser.add_argument("--password", "-P", nargs="?", const="",default=None)
    return parser.parse_args()

def print_help():
    print("""mprand - enqueue random songs in MPD

Usage:
  mprand [options]

Options:
  -q, --quiet           Disable logging output
  -s, --host HOST       MPD host (default: localhost)
  -p, --port PORT       MPD port (default: 6600)
  -h, --help            Show this help message and exit
  -P, --password        MPD Password (if you use one)
""")

client = MPDClient()

def setup_logging(args):
    FORMAT = '%(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)
    root = logging.getLogger()
    if args.quiet:
        root.setLevel(logging.CRITICAL)
    else:
        root.setLevel(logging.INFO)

# Connects mprand to the MPD daemon
def connect_client(args):
    try:
        client.connect(host=args.host, port=args.port)
    except SocketError:
        logging.critical("SOCKET ERROR: couldnt connect to mpd, is the server running? is the host correct?")
        sys.exit(1)

def disconnect_client():
    client.close()
    client.disconnect()

def check_password(args):
    try:
        client.status()
    except CommandError as e:
        if "permission" in str(e).lower():
            if args.password is None:
                logging.critical("MPD requires a password")
                pw = getpass.getpass("MPD password: ")
            else:
                pw = args.password

            try:
                client.password(pw)
            except CommandError:
                logging.critical("Prolly wrong password bro")
                sys.exit(1)
        else:
            raise


# Uses client.list["file"] to get a list of all files in the MPD database
# then uses random.choice() to pick and return a random one
def get_random_song():
    piss = choice(client.list("file"))
    return piss['file']

def enqueue_random():
    client.add(get_random_song())

# If MPD is not playing, start playing. If it is already playing, do nothing. If it errors out for some reason it also does nothing
# bc i have no idea what exactly could go wrong here that isnt filtered already 
def check_playing():
    try:
        if not client.status()['state'] == "play":
            client.play()
            logging.info("Starting player")
        else:
            logging.info("already playin yo")
    except:
        print("something happened fam")

# If the playlist length is equal to the position of the song + 1, that means you're on the last song (i guess) 
# and the script should enqueue another song to prevent mpd from stopping 
def check_last_song():
    songPos = client.status()['song']
    playPos = client.status()['playlistlength']
    
    if int(playPos) == int(songPos) + 1:
        logging.info("Last song detected, enqueueing new song")
        return True 

# If the playlist is empty, enqueue a song and start playing. 
# If it's not, then check if its on the last song. If it is, enqueue a new one. If it isn't, do nothing apart from checking if it's playing or not.
def start_playing():
    if (client.status()['playlistlength']) == '0':
        enqueue_random()
        client.play()
    elif (client.status()['state']) == 'stop':
        client.play()
    else:
        if (check_last_song()):
            enqueue_random()
        check_playing()

# Use the mpd idle feature to wait for a player event (which unfortunately also includes pauses and such, which will get logged too, cluttering the stdout a bit)
def enqueue_loop():
    while True:
        client.idle('player')
        logging.info("Player event spotted")
        if check_last_song():
            enqueue_random()
            logging.info("Enqueueing another song")
def recover():
    start_playing()
    enqueue_loop()

def main ():
    args = parse_args()
    if args.help:
        print_help()
        sys.exit(1)

    setup_logging(args)
    connect_client(args)
    check_password(args)
    start_playing()
    enqueue_loop()

if __name__ == "__main__":
    attempt = 1
    while True: 
            try:
                main()
            except ConnectionError:
                logging.error("CONNECTION ERROR: could not connect to MPD, did it crash? Terminating.")
                sys.exit(1)
            except KeyboardInterrupt:
                logging.critical("KeyboardInterrupt detected, terminating.")
                disconnect_client()
                sys.exit(0)
            except IndexError:
                logging.critical("Cannot choose from an empty playlist")
                disconnect_client()
                sys.exit(1)
            except Exception:
                logging.warning("UNKNOWN: Oh no, an exception! It was prolly nothing, trying to continue.")
                try:
                    attempt = attempt+1
                    if attempt == 4:
                        sys.exit(1)
                    recover()
                except KeyboardInterrupt:
                        logging.critical("KeyboardInterrupt detected, terminating")
                        sys.exit(1)
                except:
                    logging.critical("Couldn't recover, terminating.")
                    disconnect_client()
                    sys.exit(1)
