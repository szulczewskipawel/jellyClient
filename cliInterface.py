from conf.constants import CLIENT_VERSION
from click import clear
from connection import jellyConnect
from jellyfin_apiclient_python import api
from tabulate import tabulate

import cmd
import sys

class cliInterface(cmd.Cmd):

    intro = "\nWelcome to pszs jellyConf client. Type help or ? to list commands.\n"
    prompt = '(jelly) '

    connection = None

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
        print(CLIENT_VERSION)

    def do_showUsers(self, arg):
        'Shows all registered users'
        if self.connection is None:
            print('Client is not connected! Please connect to the server.')
            return
        users = self.client.jellyfin.get_users()
        for i in range(len(users)):
            userName = users[i]["Name"]
            print(userName)

    def do_recentlyAddedStuff(self, arg):
        'Shows recently added stuff'
        added = self.client.jellyfin.get_recently_added()
        values = list()
        print()
        for i in range(len(added)):
            val = [] 
            val.append(i+1)
            val.append(added[i]["Name"])
            values.append(val)
        print(tabulate(values, headers=["Lp", "Title"]))
        print()

    def do_clear(self, arg):
        'Clears the screen'
        clear()

