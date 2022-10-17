#!/usr/bin/env python3

from conf.jellyConf import *

import jellyfin_apiclient_python

class JellyClient():
    def __init__(self):        
        jConf = JellyConf()
        self.credentials = []
        self.username = jConf.username
        self.url = jConf.url

foo = JellyClient()

