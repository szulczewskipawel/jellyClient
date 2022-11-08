from prettytable import PrettyTable
from conf.constants import PLAYLIST_FILE 

import json
import os
import re
import subprocess

def parse(arg):
    result = re.findall(r"(-?\w+)(?:-(\w+)|)\s*(?:(\w+)|\"([^\"]+)|(\d+)-(\d+)|)", arg)
    argsTuple = tuple(args for z in result for args in z if args != '')
    parmDict = dict()
    if len(argsTuple) == 0:
        return parmDict

    if '-' not in argsTuple[0]:
        parmDict['max'] = max(argsTuple)
        parmDict['min'] = min(argsTuple)
        return parmDict

    i = 1
    for a in argsTuple:
        if i == 1:
            parmDict[a] = ''
        else:
            if i %2 == 0 and i > 1:
                    parmDict[argsTuple[i-2]] = a
        i += 1
    return parmDict

def playSong(songUrl, player):
    pList = list()
    pList.append(player)
    pList.append(songUrl)

    subprocess.run(pList)

def printPrettyTable(data, headerNo=True):
    i = 0
    for z in data:
        if headerNo == True:
            if i == 0:
                z.insert(0, "No")
            else:
                z.insert(0, i)
            i += 1
    tab = PrettyTable(data[0])
    tab.add_rows(data[1:])
    print(tab)

def showBufferOrPlaylist(buforplay, buffer=True):
    if len(buforplay) > 0:
        if buffer == True:
            bList = [["Name"]]
        else:
            bList = [["No", "Name"]]
        for i in buforplay:
            smList = list()
            if buffer != True:
                smList.append(i)
            smList.append(buforplay[i][0])
            bList.append(smList)
        printPrettyTable(bList, buffer)
    else:
        print('The list is empty at this momment.')

def savePlaylists(playlists):
    if len(playlists) == 0:
        print('Hey buddy! There is nothing to be saved, your playlist is empty!')
        return
    try:
        with open(PLAYLIST_FILE, 'w') as f:
            json.dump(playlists, f, ensure_ascii=True)
    finally:
        print ('Playlist has been saved successfully')

def loadPlaylist():
    playlists = ''
    if not os.path.exists(PLAYLIST_FILE):
        print('Playlist file {} is not present'.format(PLAYLIST_FILE))
        return
    try:
        f = open(PLAYLIST_FILE)
        playlists = json.load(f)
        f.close()
    finally:
        print('Playlist has been loaded successfully')
    return playlists

def songsFromAlbum(sItems):
    sList = list()
    for i in sItems:
        tmpTuple = tuple()
        searchName = i["Name"]
        searchId = i["Id"]
        searchType = i["Type"]
        searchIdxNo = i["IndexNumber"]

        tmpTuple = (searchName, searchId, searchType, searchIdxNo)
        sList.append(tmpTuple)

    sortedList = sorted(sList, key=lambda song: song[3])
    return sortedList

