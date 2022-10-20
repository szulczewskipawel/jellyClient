from conf.constants import CLIENT_VERSION
from click import clear
from connection import jellyConnect
from prettytable import PrettyTable

import cmd
import sys

songBuffer = dict()
playlist = dict()

def printPrettyTable(data):
    i = 0
    for z in data:
        if i == 0:
            z.insert(0, "Lp")
        else:
            z.insert(0, i)
        i += 1
    tab = PrettyTable(data[0])
    tab.add_rows(data[1:])
    print(tab)

def parse(arg):
    return tuple(map(str, arg.split()))

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

class cliInterface(cmd.Cmd):
    intro = "\nWelcome to pszs jellyConf client. Type help or ? to list commands.\n"
    prompt = '(jelly) '
    connection = None
    conf = None

    def emptyline(self):
        self.default('')

    def default(self, arg):
        print ("\nWhat? Dunno understand ya, type help or ? to list commands.\n")

    def do_connect(self, arg):
        'Tries to connect to the server...'
        self.connection = jellyConnect(self.conf)
        self.client = self.connection.client
        
    def do_quit(self, arg):
        'Says bye-bye to the server'
        print('\nSee you later aligator!\n')
        sys.exit(0)

    def do_version(self, arg):
        'Prints version of the client'
        print("\n{}\n".format(CLIENT_VERSION))

    def do_users(self, arg):
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

    def do_recentlyAddedStuff(self, arg):
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

    def do_search(self, arg):
        # TODO searching statements, eg "losing my religion" (words between ")
        '''Searches the database:
        search <word> <limit>
            <word>  is a word you want to search, default = chopin, 
            <limit> shows first <limit> items found, default = 20'''
        songBuffer.clear()
        tArgs = parse(arg)
        searchTerm = tArgs[0] if len(tArgs) > 0 else 'chopin'
        searchLimit = tArgs[1] if len(tArgs) > 1 else 20

        searches = self.client.jellyfin.search_media_items(term = searchTerm, limit = searchLimit)["Items"]
        sList = [["Name"]]
        for i in range(len(searches)):
            searchesList = list()

            songName = searches[i]["Name"]
            songId = searches[i]["Id"]

            searchesList.append(songName)
            sList.append(searchesList)
            songBuffer[i+1] = (songName, songId, )

        printPrettyTable(sList)

    def do_buffer(self, arg):
        'Shows actual buffer'
        showBufferOrPlaylist(songBuffer)
   
    def do_playlist(self, arg):
        'Shows playlist'
        showBufferOrPlaylist(playlist)

