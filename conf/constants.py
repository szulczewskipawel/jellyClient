import os

CONF_FILE = os.path.expanduser('~') + '/.jconf.json'
PLAYLIST_FILE = os.path.expanduser('~') + '/.jconf_playlist.json'
MUST_HAVE_KEYS = ['url', 'username', 'password', 'player']

APP_NAME = "pszs-jellyClient"
USER_APP_NAME = "pszs-jellyClient"
CLIENT_VERSION = "0.0.1"
USER_AGENT = "pszs-jellyClient/%s" % CLIENT_VERSION

