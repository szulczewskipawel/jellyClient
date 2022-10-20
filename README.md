# jellyClient
Brave attempt to write a command-line client for jellyfin.

## config file
You need a config file (~/.jconf.json), something like this:

~~~
{"url":"some_url", "username": "some_user", "password": "some_pass", "authssl": "True", "player": "mplayer"}
~~~
Where:
* url -- url of the server,
* username -- your jelly username,
* password -- your password,
* authssl -- authentication via SSL? Acceptable values: True or False, False is by default,
* player -- your local media player, like mplayer or whatever

