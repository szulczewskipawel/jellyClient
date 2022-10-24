# jellyClient
Brave attempt to write a command-line client for jellyfin.

## config file
You need a config file (~/.jconf.json), something like this:

~~~
{"url":"some_url", "username": "some_user", "password": "some_pass", "authssl": "True", "player": "mplayer", "autoconnect": "True"}
~~~
Where:
* url -- url of the server,
* username -- your jelly username,
* password -- your password,
* authssl -- authentication via SSL? Acceptable values: True or False, False is by default,
* player -- your local media player, like mplayer or whatever
* autoconnect -- should client connect to the server automaticaly after run?

## commands
* a \<name\> -- shows/changes active playlist,
* b -- shows buffer (list of searched songs you may wanna add to the playlist),
* c -- connect to the server,
* clear -- clears the screen,
* d \<number\> \<playlist\> -- deletes song number \<number\> from playlist \<playlist\>, by default
  \<playlist\> is active one,
* help -- should help you with commands,
* i <number> -- insert song number <number> (from buffer) to the playlist, default 1,
* lp -- loads playlist(s) from file
* p -- show playlist
* pl <number> -- plays the song number <number> (from playlist), default 1,
* q -- quits this beautiful client,
* r -- shows recently added to the server stuff,
* s -s \<word\> -l \<limit\> -t \<type\>- - searches database:
--\<word\> is a word to search, default chopin,\n
--\<limit\> limits items found, default 20, \n
--\<type\> type (one of: All, Audio, Folder, MusicAlbum, MusicArtist), default = Audio\n
* sh -- plays random song from playlist,
* sp -- saves playlist to file,
* u -- shows all registered users,
* v -- shows version of the client

## TODO
* Searching not only by words, but also by statements, like "losing my religion" (words between "),
* Some nice information like 'Connected to the server' when you're connected to the server,
* ~~Infite play (shuffle or repeat),~~
* Adding whole songs from album to playlist at one shot,
* ~~Flag to connected to the server automatically~~

