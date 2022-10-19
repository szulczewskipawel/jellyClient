from conf.constants import CLIENT_VERSION
from click import clear
from connection import jellyConnect
from tabulate import tabulate

import cmd
import sys

def printPrettyTable(data, headers):
    values = list()
    fixedHeaders = ["Lp"]
    print()
    for i in range(len(data)):
        val = []
        val.append(i+1)
        val.append(data[i])
        values.append(val)
    print(tabulate(values, fixedHeaders + list(headers)))
    print()

class cliInterface(cmd.Cmd):

    intro = "\nWelcome to pszs jellyConf client. Type help or ? to list commands.\n"
    prompt = '(jelly) '

    connection = None

    def emptyline(self):
        self.default('')

    def default(self, arg):
        print ("\nWhat? Dunno understand ya, type help or ? to list commands.\n")

    def do_connect(self, arg):
        'Tries to connect to the server...'
        self.connection = jellyConnect()
        self.client = self.connection.client
        
    def do_quit(self, arg):
        'Says bye-bye to the server'
        print('\nSee you later aligator!\n')
        sys.exit(0)

    def do_version(self, arg):
        'Prints version of the client'
        print("\n{}\n".format(CLIENT_VERSION))

    def do_showUsers(self, arg):
        'Shows all registered users'
        if self.connection is None:
            print('Client is not connected! Please connect to the server.')
            return

        users = self.client.jellyfin.get_users()
        usersList = []
        for i in range(len(users)):
            usersList.append(users[i]["Name"])

        printPrettyTable(usersList, ["username"])

    def do_recentlyAddedStuff(self, arg):
        'Shows recently added stuff'
        added = self.client.jellyfin.get_recently_added()
        addedList = []
        for i in range(len(added)):
            addedList.append(added[i]["Name"])

        printPrettyTable(addedList, ["Name"])

    def do_clear(self, arg):
        'Clears the screen'
        clear()

