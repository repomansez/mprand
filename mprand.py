#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mpd import (MPDClient, CommandError, ConnectionError)
from random import choice
from socket import error as SocketError
import sys
import logging

# SETTINGS BECAUSE WHY NOT
#
HOST = 'localhost'
PORT = '6600'
PASSWORD = False
#
client = MPDClient()

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)
root = logging.getLogger()
root.setLevel(logging.INFO)

# Connects mprand to the MPD daemon
def connectClient():
    try:
        client.connect(host=HOST, port=PORT)
    except SocketError:
        logging.error("SOCKET ERROR: couldnt connect to mpd, maybe start it dumbass")
        exit(1)

def disconnectClient():
    client.close()

# If MPD requires a password, SET IT HERE 
def checkPassword():
    if PASSWORD:
        try:
            client.password(PASSWORD)
        except CommandError:
            logging.error("Prolly wrong password bro")
            exit(1)

# Uses client.list["file"] to get a list of all files in the MPD database
# then uses random.choice() to pick and return a random one
def getrandomsong():
    piss = choice(client.list("file"))
    return piss['file']

def enqRandom():
    client.add(getrandomsong())

# If MPD is not playing, start playing. If it is already playing, do nothing. If it errors out for some reason it also does nothing
# bc i have no idea what exactly could go wrong here that isnt filtered already 
def checkPlaying():
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
def checkLastSong():
    songPos = client.status()['song']
    playPos = client.status()['playlistlength']
    
    if int(playPos) == int(songPos) + 1:
        return True 

# If the playlist is empty, enqueue a song and start playing. 
# If it's not, then check if its on the last song. If it is, enqueue a new one. If it isn't, do nothing apart from checking if it's playing or not.
def startPlaying():
    if (client.status()['playlistlength']) == '0':
        enqRandom()
        client.play()
    else:
        if (checkLastSong()):
            enqRandom()
        checkPlaying()

# Use the mpd idle feature to wait for a player event (which unfortunately also includes pauses and such, which will get logged too, cluttering the stdout a bit)
def enqLoop():
    while True:
        client.idle('player')
        logging.info("Player event spotted")
        if checkLastSong():
            enqRandom()
            logging.info("Enqueueing another song")

def main ():
    checkPassword()
    startPlaying()
    enqLoop()

if __name__ == "__main__":
    connectClient()
    while True: 
            try:
                main()
            except ConnectionError:
                logging.error("CONNECTION ERROR: could not connect to MPD, did it crash? Terminating.")
                exit(1)
            except Exception as ex:
                logging.warning("UNKNOWN: Something bad happened, what did you do? Trying to recover.")
                continue
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt detected, terminating.")
                disconnectClient()
                exit(0)
            except:
                logging.error("Couldn't recover, terminating")
                disconnectClient()
                exit(1)