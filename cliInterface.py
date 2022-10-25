from click import clear
from conf.constants import CLIENT_VERSION
from connection import jellyConnect
from outputs import *

import cmd
import operator
import sys

songBuffer = dict()
playlist = dict()
playListDict = dict()
activePlayList = ''

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
        print('See you later alligator!')
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
        s -s <word> -l <limit>
            -s <word>  is a word you want to search, default = chopin, 
            -l <limit> shows first <limit> items found, default = 20,
            -t <type> type (All, Audio, Folder, MusicAlbum, MusicArtist), default = Audio'''
        songBuffer.clear()
        dArgs = args2dict(arg)

        searchTerm = 'chopin'
        searchLimit = 20
        searchType = 'Audio'
        if '-s' in dArgs:
            searchTerm = dArgs['-s']
        if '-l' in dArgs:
            searchLimit = dArgs['-l']
        if '-t' in dArgs:
            searchType = dArgs['-t']

        searches = self.client.jellyfin.search_media_items(term=searchTerm, media=searchType, limit=searchLimit)["Items"]
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
            songBuffer[str(i+1)] = (searchName, searchId, )

        printPrettyTable(sList)

    def do_b(self, arg):
        'Shows actual buffer'
        showBufferOrPlaylist(songBuffer)
   
    def do_p(self, arg):
        '''Shows playlist <name>
        p <name>
            <name> is a name of playlist, shows all playlists if the parameter is not given
        '''
        tArgs = parse(arg)
        playListName = tArgs[0] if len(tArgs) > 0 else 'all'

        if playListName == 'all':
            for pList in playListDict:
                print("Playlist: " + pList)
                showBufferOrPlaylist(playListDict[pList], False)
        else:
            if playListName in playListDict:
                showBufferOrPlaylist(playListDict[playListName], False)
            else:
                print("No playlist {} found".format(playListName))

    def do_i(self, arg):
        '''Inserts song (existed in buffer) to active playlist
        i <number>
            <number> is a buffer's song number, default = 1'''
        if ',' in arg:
            tArgsList = parse(arg, ',')
            for a in tArgsList:
                self.do_i(a)
            return
        else:
            tArgs = parse(arg)
        songNumber = str(tArgs[0]) if len(tArgs) > 0 else '1'
        global activePlayList
        global playlist

        if songNumber not in songBuffer:
            print("Check the buffer again, number {} aint existing there!".format(songNumber))
            return
        songName = songBuffer[songNumber][0]

        if activePlayList == '':
            activePlayList = input("There are no songs in your playlist. What name do you want to "
            + "give to playlist? ")

        if activePlayList in playListDict:
            playlist = playListDict[activePlayList]
        else:
            playlist=dict()

        if len(playlist) > 0:
            maxNo = int(max(playlist.items(), key=operator.itemgetter(0))[0])
        else:
            maxNo = 0
        playlist[str(maxNo+1)] = songBuffer[songNumber]

        playListDict[activePlayList] = playlist
        print ('Song "{}" added to the playlist at position {}'.format(songName, maxNo+1))

    def do_pl(self, arg):
        '''Plays the song from active playlist
        pl <number> -f
            <number> is a playlist's song number, default = 1,
            -f plays the whole playlist forever'''
        tArgs = parse(arg)
        songNumber = str(tArgs[0]) if len(tArgs) > 0 else '1'

        if activePlayList == '':
            print("No active playlist, please use option a first, or search for any media")
            return
        else:
            playlist = playListDict[activePlayList]
            if '-f' not in tArgs:
                if songNumber not in playlist:
                    print(songNumber)
                    print(playlist)
                    print("Check the playlist, this number aint existing there!")
                    return
                song = playlist[songNumber]
                songUrl = self.client.jellyfin.download_url(song[1])
                playSong(songUrl, self.conf.player)
            else:
                # play forever and ever
                while 1 > 0:
                    for s in playlist:
                        song = playlist[s]
                        songUrl = self.client.jellyfin.download_url(song[1])
                        playSong(songUrl, self.conf.player)

    def do_sp(self, arg):
        'saves playlists to a file'
        savePlaylists(playListDict)

    def do_lp(self, arg):
        'Loads playlist'
        global playListDict
        playListFF = loadPlaylist()
        if playListFF is not None:
            playListDict = playListFF
            self.do_p('all')

    def do_d(self, arg):
        '''Deletes song from playlist
        d <number> <playlist>
            <number> is a playlist's song number, default = 1
            <playlist> name of playlist, default = active playlist'''
        if ',' in arg:
            tArgsList = parse(arg, ',')
            for a in tArgsList:
                self.do_d(a)
            return
        else:
            tArgs = parse(arg)
        songNumber = str(tArgs[0]) if len(tArgs) > 0 else '1'
        activePL = tArgs[1] if len(tArgs) > 1 else activePlayList

        if activePL not in playListDict:
            print("Playlist {} has not been found".format(activePL))
            return

        playlist = playListDict[activePL]
        if songNumber not in playlist:
            print("Check the playlist, this number aint existing there!")
            return

        playlist.pop(songNumber)

    def do_sh(self, arg):
        'Plays random song from your active playlist'

        if activePlayList == '':
            print('No active playlist, please use option a first')
            return
        
        playlist = playListDict[activePlayList]
        lenPlaylist = len(playlist)
        if lenPlaylist == 0:
            print('Hey buddy! Your playlist is empty!')
            return

        songNumbers = list(playlist.keys())
        from random import choice 
        randSongNumber = str(choice(songNumbers))
        self.do_pl(randSongNumber)

    def do_a(self, arg):
        '''Shows/changes active playlist
        a <name>
            changes active playlist to <name> or shows active playlist if the parameters is not
            given'''
        tArgs = parse(arg)
        playListName = tArgs[0] if len(tArgs) > 0 else ''
        global activePlayList

        if playListName == '':
            print("Active playlist: " + activePlayList)
        else:
            if playListName in playListDict:
                activePlayList = playListName
            else:
                yn = input("No playlist {} found. Do you want to create it? ".format(playListName))
                if 'y' or 'Y' in yn:
                    activePlayList = playListName
                    print("Playlist {} has been created and it's active now".format(playListName))

