from prettytable import PrettyTable
from conf.constants import PLAYLIST_FILE 

import json
import os

def parse(arg):
    return tuple(map(str, arg.split()))

# json.dump treats keys always as a string,
# so here is a small workaround...
def jsonKeys2int(json):
    if isinstance(json, dict):
        return {int(k):v for k,v in json.items()}
    return json

def printPrettyTable(data):
    i = 0
    for z in data:
        if i == 0:
            z.insert(0, "No")
        else:
            z.insert(0, i)
        i += 1
    tab = PrettyTable(data[0])
    tab.add_rows(data[1:])
    print(tab)

def showBufferOrPlaylist(buforplay):
    if len(buforplay) > 0:
        bList = [["Name"]]
        for i in buforplay:
            smList = list()
            smList.append(buforplay[i][0])
            bList.append(smList)
        printPrettyTable(bList)
    else:
        print('The list is empty at this momment.')

def savePlaylist(playlist):
    if len(playlist) == 0:
        print('Hey buddy! There is nothing to be saved, your playlist is empty!')
        return
    try:
        with open(PLAYLIST_FILE, 'w') as f:
            json.dump(playlist, f, ensure_ascii=True)
    finally:
        print ('Playlist has been saved successfully')

def loadPlaylist():
    playlist = ''
    try:
        f = open(PLAYLIST_FILE)
        playlist = json.load(f, object_hook=jsonKeys2int)
        f.close()
    finally:
        print('Playlist has been loaded successfully')
    return playlist

