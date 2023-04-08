#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mpd import (MPDClient, CommandError)
from random import choice
from socket import error as SocketError
from sys import exit
import logging

# SETTINGS BECAUSE WHY NOT
#
HOST = 'localhost'
PORT = '6600'
PASSWORD = False
#
client = MPDClient()

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


def main ():
    connectClient()
    checkPassword()
    startPlaying()
    while True:
        client.idle('player')
        logging.info("Player event spotted")
        if checkLastSong():
            enqRandom()
            logging.info("Enqueueing another song")

if __name__ == "__main__":
    try:
        main()
    except:
        logging.error("Something bad happened, maybe you crashed mpd or skipped too fast it stopped?")
        exit(1)



