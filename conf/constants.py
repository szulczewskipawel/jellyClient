APP_NAME = "pszs-jellyClient"
USER_APP_NAME = "pszs-jellyClient"
CLIENT_VERSION = "0.0.1"
USER_AGENT = "pszs-jellyClient/%s" % CLIENT_VERSION
CAPABILITIES = {
    "PlayableMediaTypes": "Video",
    "SupportsMediaControl": True,
    "SupportedCommands": (
        "MoveUp,MoveDown,MoveLeft,MoveRight,Select,"
        "Back,ToggleFullscreen,"
        "GoHome,GoToSettings,TakeScreenshot,"
        "VolumeUp,VolumeDown,ToggleMute,"
        "SetAudioStreamIndex,SetSubtitleStreamIndex,"
        "Mute,Unmute,SetVolume,DisplayContent,"
        "Play,Playstate,PlayNext,PlayMediaSource"
    ),
}

