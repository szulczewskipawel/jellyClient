from pathlib import Path

import json
import os
import sys

confFile = os.path.expanduser('~') + '/.jconf.json'
mustHaveKeys = ['url', 'username', 'password']

class JellyConf():
    def __init__(self):
        credsData = self.getCredentials()
        self.url = credsData['url']
        self.username = credsData['username'] 
        self.password = credsData['password']

        if not 'authssl' in credsData:
            self.authssl = False
        else:
            self.authssl = credsData['authssl']

    def getCredentials(self, file=confFile):
        file = Path(confFile)
        if not file.exists():
            print("\nFATAL: Configuration file {} does not exist!\n".format(confFile))
            sys.exit(100)

        f = open(file) 
        credsData = json.load(f)
        f.close()

        # checking if all necessary keys (to connect) are available
        notCredsKeys = []
        for k in mustHaveKeys:
            if k not in credsData:
               notCredsKeys.append(k) 
        if len(notCredsKeys) > 0:
            print ("\nFATAL: The following mandatory key(s) are not in the config file: ")
            print (", ".join(notCredsKeys))
            sys.exit(99)

        return credsData

