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

class _Wrapper:

    def __init__(self, fd):
        self.fd = fd

    def readline(self, *args):
        try:
            return self.fd.readline(*args)
        except KeyboardInterrupt:
            res = input('\nCtrl+C has been pressed. Do you want to leave the program (y/n)? ')
            if res.lower() == 'y':
                return 'q'
            else:
                return '\n'

class cliInterface(cmd.Cmd):

    def __init__(self):
        super().__init__(stdin=_Wrapper(sys.stdin))
        self.use_rawinput = False
        self.intro = "\nWelcome to pszs jellyConf client. Type help or ? to list commands.\nTip: Type intro to get a short introduction.\n"
        self.prompt = '(jelly) '
        self.connection = None
        self.conf = None

    def emptyline(self):
        return

    def default(self, arg):
        print ("What? Dunno understand ya, type help or ? to list commands.")

    def do_intro(self, arg):
        print('''
First steps:
c               # connect to server (not required with autoconnect enabled)
a my_playlist   # create a new playlist (my_playlist)
s -s "foo bar"  # search song(s) to add
i <num>         # add song #num to playlist
pl              # start playback

Session handling:
p               # show current playlist
sp              # save playlist to file
q               # quit program
lp              # load previously stored playlist
a my_playlist   # set my_playlist as active
''')

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
        for i in users:
            uList = list()
            uList.append(i["Name"])
            usersList.append(uList)

        printPrettyTable(usersList)

    def do_r(self, arg):
        'Shows recently added stuff'
        added = self.client.jellyfin.get_recently_added()
        addedList = [["Name"]] 
        for i in added:
            aList = list()
            aList.append(i["Name"])
            addedList.append(aList)

        printPrettyTable(addedList)

    def do_clear(self, arg):
        'Clears the screen'
        clear()

    def do_s(self, arg):
        '''Searches the database:
        s -s <word> -l <limit>
            -s <word>  is a word you want to search, default = chopin, 
            -l <limit> shows first <limit> items found, default = 20,
            -t <type> type (All, Audio, Folder, MusicAlbum, MusicArtist), default = Audio'''
        songBuffer.clear()
        dArgs = parse(arg)

        searchTerm = dArgs['-s'] if '-s' in dArgs else 'chopin'
        searchLimit = dArgs['-l'] if '-l' in dArgs and dArgs['-l'].isnumeric() else 20
        searchType = dArgs['-t'] if '-t' in dArgs else 'Audio' 

        searches = self.client.jellyfin.search_media_items(term=searchTerm, media=searchType, limit=searchLimit)["Items"]
        sList = [["Name", "Type", "Artist(s)"]]
        i=0
        for song in searches:
            searchesList = list()

            searchName = song["Name"]
            searchId = song["Id"]
            searchType = song["Type"]

            # you wont believe -- not every audio has tags!
            # and yes, print max 3 artists of the song, otherwise the output will be screwed up
            if 'Artists' in song:
                searchArtists = ','.join(str(a).strip() for a in song["Artists"][0:3])
            else:
                searchArtists = '?'

            searchesList.append(searchName)
            searchesList.append(searchType)
            searchesList.append(searchArtists)
            sList.append(searchesList)
            songBuffer[str(i+1)] = (searchName, searchId, searchType)
            i += 1

        printPrettyTable(sList)

    def do_b(self, arg):
        'Shows actual buffer'
        showBufferOrPlaylist(songBuffer)
   
    def do_p(self, arg):
        '''Shows playlist <name>
        p <name>
            <name> is a name of playlist, shows all playlists if the parameter is not given
        '''
        playListName = arg if len(arg) > 0 else 'all'

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

        dArgs = parse(arg)
        songNumber = '1'

        if 'min' in dArgs and 'max' in dArgs:
            minNum = int(dArgs['min'])
            maxNum = int(dArgs['max'])

            if minNum != maxNum:
                for i in range(minNum, maxNum+1):
                    self.do_i(str(i))
                return            
            songNumber = str(minNum)

        global activePlayList
        global playlist

        if songNumber not in songBuffer:
            print("Check the buffer again, number {} aint existing there!".format(songNumber))
            return
        songName = songBuffer[songNumber][0]
        songType = songBuffer[songNumber][2]

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

        if songType == 'MusicAlbum':
            yn = input("You've chosen album. Do you want to add all songs from this album to the "
            + "playlist? ")
            if 'Y' in yn or 'y' in yn:
                albumId = songBuffer[songNumber][1]
                sItems = self.client.jellyfin.get_items_by_letter(parent_id=albumId)['Items']
                songsList = songsFromAlbum(sItems)
                i = 1
                for song in songsList:
                    playlist[maxNo + i] = song[:3]
                    print('Song "{}" added to the playlist at position {}'.format(song[0],
                                                                                  int(maxNo)+i))
                    i += 1
                playListDict[activePlayList] = playlist
                return
            return

        playlist[maxNo+1] = songBuffer[songNumber]

        playListDict[activePlayList] = playlist
        print ('Song "{}" added to the playlist at position {}'.format(songName, int(maxNo)+1))

    def do_pl(self, arg):
        '''Plays the song from active playlist
        pl <number> -f
            <number> is a playlist's song number, default = 1,
            -f plays the whole playlist forever'''
        tArgs = parse(arg)
        songNumber = int(tArgs['max']) if len(tArgs) > 0 and '-f' not in tArgs and tArgs['max'].isnumeric() else 1

        if activePlayList == '':
            try:
                songId = songBuffer[str(songNumber)][1]
                songUrl = self.client.jellyfin.download_url(songId)
                playSong(songUrl, self.conf.player)
            except:
                print("You don't have active playlist and don't have songs in the buffer. Cannot play the song.")
            return
        else:
            if not activePlayList in playListDict:
                print("You dont have any songs in your playlist, search (command s) and add some " +
                      "songs to your playlist (command i).")
                return
            playlist = playListDict[activePlayList]
            if '-f' not in tArgs:
                if songNumber not in playlist:
                    print(songNumber)
                    print("Check the playlist, this number {} aint existing there!".format(songNumber))
                    return
                song = playlist[songNumber]
                songUrl = self.client.jellyfin.download_url(song[1])
                playSong(songUrl, self.conf.player)
            else:
                # plays forever and ever
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

        for z in playListDict:
            tempdict = {int(k):v for k,v in playListDict[z].items()}
            playListDict[z] = tempdict

    def do_d(self, arg):
        '''Deletes song from active playlist
        d <number> 
            <number> is a playlist's song number, default = 1'''
        dArgs = parse(arg)
        songNumber = '1'

        if 'min' in dArgs and 'max' in dArgs:
            minNum = int(dArgs['min'])
            maxNum = int(dArgs['max'])

            if minNum != maxNum:
                for i in range(minNum, maxNum+1):
                    self.do_d(str(i))
                return
            songNumber = minNum

        if activePlayList == '':
            print("No active playlist, please use option a first")
            return

        playlist = playListDict[activePlayList]
        if songNumber not in playlist:
            print("Check the playlist, the number {} aint existing there!".format(songNumber))
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
        playListName = tArgs['max'] if len(tArgs) > 0 else ''
        global activePlayList

        if playListName == '':
            print("Active playlist: " + activePlayList)
        else:
            if playListName in playListDict:
                activePlayList = playListName
            else:
                yn = input("No playlist {} found. Do you want to create it? (y/n) ".format(playListName))
                if yn.lower() == 'y':
                    activePlayList = playListName
                    print("Playlist {} has been created and it's active now".format(playListName))

