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


def connectClient():
    try:
        client.connect(host=HOST, port=PORT)
    except SocketError:
        logging.error("SOCKET ERROR: couldnt connect to mpd, maybe start it dumbass")
        exit(1)

def checkPassword():
    if PASSWORD:
        try:
            client.password(PASSWORD)
        except CommandError:
            logging.error("Prolly wrong password bro")
            exit(1)

def getrandomsong():
    piss = choice(client.list("file"))
    return piss['file']

def enqRandom():
    client.add(getrandomsong())

def checkPlaying():
    try:
        if not client.status()['state'] == "play":
            client.play()
            logging.info("Starting player")
        else:
            logging.info("already playin yo")
    except:
        print("something happened fam")

def checkLastSong():
    songPos = client.status()['song']
    playPos = client.status()['playlistlength']
    
    if int(playPos) == int(songPos) + 1:
        return True 

def startPlaying():
    client.clear()
    enqRandom()
    checkPlaying()
    checkLastSong()

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
                logging.error("CONNECTION ERROR: could not connect to MPD, did it crash? Exiting.")
                exit(1)
            except Exception as ex:
                logging.warn("UNKNOWN: Something bad happened, what did you do? Trying to recover.")
                continue
            except:
                logging.error("Couldn't recover, dying")
                exit(1)