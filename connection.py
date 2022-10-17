from conf.constants import *
from jellyfin_apiclient_python import JellyfinClient
from jellyfin_apiclient_python.connection_manager import CONNECTION_STATE
from conf.jellyConf import *

class jellyConnect():
    def __init__(self):
        jConf = JellyConf()
        self.authssl = jConf.authssl
        self.url = jConf.url
        self.username = jConf.username
        self.password = jConf.password
        self.client = self.connectClient()
    
    def connectClient(self, authssl=True):
       client = JellyfinClient(allow_multiple_clients=False)
       client.config.app(USER_APP_NAME, CLIENT_VERSION, 'foo', 'foo2')
       client.config.data['auth.ssl'] = authssl

       client.auth.connect_to_address(self.url)

       # TODO: information 'client connected' or so
       return client

