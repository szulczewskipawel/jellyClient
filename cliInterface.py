from click import clear
from conf.constants import CLIENT_VERSION
from connection import jellyConnect
from outputs import *

import cmd
import subprocess
import sys

songBuffer = dict()
playlist = dict()

class cliInterface(cmd.Cmd):
    intro = "\nWelcome to pszs jellyConf client. Type help or ? to list commands.\n"
    prompt = '(jelly) '
    connection = None
    conf = None

    def emptyline(self):
        return

    def default(self, arg):
        print ("What? Dunno understand ya, type help or ? to list commands.")

    def do_c(self, arg):
        'Tries to connect to the server...'
        self.connection = jellyConnect(self.conf)
        self.client = self.connection.client
        
    def do_q(self, arg):
        'Says bye-bye to the server'
        print('See you later aligator!')
        sys.exit(0)

    def do_v(self, arg):
        'Prints version of the client'
        print("{}".format(CLIENT_VERSION))

    def do_u(self, arg):
        'Shows all registered users'
        if self.connection is None:
            print('Client is not connected! Please connect to the server.')
            return

        users = self.client.jellyfin.get_users()
        usersList = [["Name"]]
        for i in range(len(users)):
            uList = list()
            uList.append(users[i]["Name"])
            usersList.append(uList)

        printPrettyTable(usersList)

    def do_r(self, arg):
        'Shows recently added stuff'
        added = self.client.jellyfin.get_recently_added()
        addedList = [["Name"]] 
        for i in range(len(added)):
            aList = list()
            aList.append(added[i]["Name"])
            addedList.append(aList)

        printPrettyTable(addedList)

    def do_clear(self, arg):
        'Clears the screen'
        clear()

    def do_s(self, arg):
        # TODO searching statements, eg "losing my religion" (words between ")
        '''Searches the database:
        s <word> <limit>
            <word>  is a word you want to search, default = chopin, 
            <limit> shows first <limit> items found, default = 20'''
        songBuffer.clear()
        tArgs = parse(arg)
        searchTerm = tArgs[0] if len(tArgs) > 0 else 'chopin'
        searchLimit = tArgs[1] if len(tArgs) > 1 else 20

        searches = self.client.jellyfin.search_media_items(term=searchTerm, limit=searchLimit)["Items"]
        sList = [["Name", "Type", "Artist(s)"]]
        for i in range(len(searches)):
            searchesList = list()

            searchName = searches[i]["Name"]
            searchId = searches[i]["Id"]
            searchType = searches[i]["Type"]

            # you wont believe -- not every audio has tags!
            # and yes, print max 3 artists of the song, otherwise the output will be screwed up
            if 'Artists' in searches[i]:
                searchArtists = ','.join(str(a).strip() for a in searches[i]["Artists"][0:3])
            else:
                searchArtists = '?'

            searchesList.append(searchName)
            searchesList.append(searchType)
            searchesList.append(searchArtists)
            sList.append(searchesList)
            songBuffer[i+1] = (searchName, searchId, )

        printPrettyTable(sList)

    def do_b(self, arg):
        'Shows actual buffer'
        showBufferOrPlaylist(songBuffer)
   
    def do_p(self, arg):
        'Shows playlist'
        showBufferOrPlaylist(playlist)

    def do_i(self, arg):
        '''Insert song (existed in buffer) to playlist
        i <number>
            <number> is a buffer's song number, default = 1'''
        tArgs = parse(arg)
        songNumber = int(tArgs[0]) if len(tArgs) > 0 else 1

        if songNumber not in songBuffer:
            print("Check the buffer again, this number aint existing there!")
            return

        l = len(playlist)
        songName = songBuffer[songNumber][0]
        playlist[l+1] = songBuffer[songNumber]
        print ('Song "{}" added to the playlist at position {}'.format(songName, l+1))

    def do_pl(self, arg):
        '''Plays the song
        pl <number>
            <number> is a playlist's song number, default = 1'''
        tArgs = parse(arg)
        songNumber = int(tArgs[0]) if len(tArgs) > 0 else 1

        if songNumber not in playlist:
            print("Check the playlist, this number aint existing there!")
            return

        songUrl = self.client.jellyfin.download_url(playlist[songNumber][1])

        pList = list()
        pList.append(self.conf.player)
        pList.append(songUrl)

        subprocess.run(pList)

    def do_sp(self, arg):
        'Saves playlist'
        savePlaylist(playlist)

    def do_lp(self, arg):
        'Loads playlist'
        global playlist
        playlist = loadPlaylist()
        self.do_p(self)

    def do_d(self, arg):
        '''Deletes song from playlist
        d <number>
            <number> is a playlist's song number, default = 1'''
        tArgs = parse(arg)
        songNumber = int(tArgs[0]) if len(tArgs) > 0 else 1
        global playlist

        if songNumber not in playlist:
            print("Check the playlist, this number aint existing there!")
            return
        playlist.pop(songNumber)

    def do_sh(self, arg):
        'Plays random song from your playlist'
        global playlist

        lenPlaylist = len(playlist)
        if lenPlaylist == 0:
            print('Hey buddy! Your playlist is empty!')
            return

        from random import randrange
        randSongNumber = randrange(lenPlaylist) + 1
        self.do_pl(str(randSongNumber))

