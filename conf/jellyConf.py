from pathlib import Path

import json
import os
import sys

confFile = os.path.expanduser('~') + '/.jconf.json'
mustHaveKeys = ['url', 'username', 'password', 'player']

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

    def getConfs(self, file=confFile):
        file = Path(confFile)
        if not file.exists():
            print("\nFATAL: Configuration file {} does not exist!\n".format(confFile))
            sys.exit(100)

        f = open(file) 
        confData = json.load(f)
        f.close()

        # checking if all necessary keys (to connect) are available
        notConfKeys = []
        for k in mustHaveKeys:
            if k not in confData:
               notConfKeys.append(k) 
        if len(notConfKeys) > 0:
            print ("\nFATAL: The following mandatory key(s) are not in the config file: ")
            print (", ".join(notConfKeys))
            sys.exit(99)

        return confData

