from pathlib import Path
from conf.constants import CONF_FILE, MUST_HAVE_KEYS

import json
import os
import sys

class JellyConf():
    def __init__(self):
        credsData = self.getConfs()
        self.url = credsData['url']
        self.username = credsData['username'] 
        self.password = credsData['password']
        self.player = credsData['player']

        if not 'authssl' in credsData:
            self.authssl = False
        else:
            self.authssl = credsData['authssl']

        if not 'autoconnect' in credsData:
            self.autoConnect = 'f' 
        else:
            self.autoConnect = credsData['autoconnect']

        if not 'autoloadplaylist' in credsData:
            self.autoLoadPlayList = 'f' 
        else:
            self.autoLoadPlayList = credsData['autoloadplaylist'] 

    def getConfs(self, file=CONF_FILE):
        file = Path(CONF_FILE)
        if not file.exists():
            print("\nFATAL: Configuration file {} does not exist!\n".format(CONF_FILE))
            sys.exit(100)

        f = open(file) 
        confData = json.load(f)
        f.close()

        # checking if all necessary keys (to connect) are available
        notConfKeys = []
        for k in MUST_HAVE_KEYS:
            if k not in confData:
               notConfKeys.append(k) 
        if len(notConfKeys) > 0:
            print ("\nFATAL: The following mandatory key(s) are not in the config file: ")
            print (", ".join(notConfKeys))
            sys.exit(99)

        return confData

