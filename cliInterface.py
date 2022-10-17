from conf.constants import CLIENT_VERSION
from connection import jellyConnect

import cmd
import sys

class cliInterface(cmd.Cmd):

    intro = "\nWelcome to pszs jellyConf client. Type help or ? to list commands.\n"
    prompt = '(jelly) '

    def do_connect(self, arg):
        'Tries to connect to the server...'
        client = jellyConnect()

    def do_quit(self, arg):
        'Say bye-bye to the server'
        print('See you later aligator!')
        sys.exit(0)

    def do_version(self, args):
        'Prints version of the client'
        print(CLIENT_VERSION)

