from conf.constants import *
from conf.jellyConf import *
from jellyfin_apiclient_python import JellyfinClient

class jellyConnect():
    def __init__(self):
        jConf = JellyConf()
        self.authssl = jConf.authssl
        self.url = jConf.url
        self.username = jConf.username
        self.password = jConf.password
        self.client = self.connectClient(self.authssl)
    
    def connectClient(self, authssl=True):
        client = JellyfinClient(allow_multiple_clients=False)
        client.config.app(USER_APP_NAME, CLIENT_VERSION, 'command_line', 'foo2')
        client.config.data['http.user_agent'] = USER_AGENT
        client.config.data['app.default'] = True
        client.config.data['auth.ssl'] = authssl

        client.auth.connect_to_address(self.url)
        result = client.auth.login(self.url, self.username, self.password)

       # TODO: information 'client connected' or so
        return client
