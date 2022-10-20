#!/usr/bin/env python3

from conf.jellyConf import *
from cliInterface import cliInterface

class JellyClient():
    def __init__(self):
        conf = JellyConf()

        cliInterf = cliInterface()
        cliInterf.conf = conf
        cliInterf.cmdloop()

foo = JellyClient()

