#!/usr/bin/env python3

from conf.jellyConf import *
from cliInterface import cliInterface

class JellyClient():
    def __init__(self):
        conf = JellyConf()

        cliInterf = cliInterface()
        cliInterf.conf = conf

        # autoconnect
        if conf.autoConnect.lower() == 'true':
            cliInterf.do_c(self)

        # autoloadplaylist
        if conf.autoLoadPlayList.lower() == 'true':
            cliInterf.do_lp(self)

        cliInterf.cmdloop()

foo = JellyClient()

