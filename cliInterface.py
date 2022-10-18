from conf.constants import CLIENT_VERSION
from connection import jellyConnect
from jellyfin_apiclient_python import api 

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
        'Say bye-bye to the server'
        print('See you later aligator!')
        sys.exit(0)

    def do_version(self, args):
        'Prints version of the client'
        print(CLIENT_VERSION)

    def do_showusers(self, args):
        'Shows all registered users'
        if self.connection is None:
            print('Client is not connected! Please connect to the server.')
            return
        users = self.client.jellyfin.get_users()
        for i in range(len(users)):
            userName = users[i]["Name"]
            print(userName)

