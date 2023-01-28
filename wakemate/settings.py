# user settings
SLEEP_INTERVAL_SECONDS = 15
# percentage the cpu has to reach for the PC to inhibit (stay on)
inhibit_percentage = 80
# locks the screen when the PC normally goes to sleep.
# If it is set to True, it directly inhibits the PC. If set to False, it will set the inactivity time until going to sleep to never.
# If the PC is set to enter the lockscreen (setting in screensaver settings menu) it will still do that if keep_screen_on is False.
# Setting it to True may be necessary if you are not running Cinnamon. Otherwise, you would have to search for other commands to edit the power settings on your system.
# If you find other commands that work for your system, it would be great if you would open a pull request so it could be integrated for everyone!
lock_screen = True
# inhibits the black screen (lock_screen must be set to False)
keep_screen_on = False
# after the time_inactive time (in mili sec.) the PC would normally go to sleep.
# This is used to reset the setting to the user setting.
# The values entered here are the default values and will be updated if the settings are changed by the user.
default_time_inactive = {
    "screen": {"decharging": 300, "charging": 300},
    "sleep": {"decharging": 600, "charging": 600},
}

# tell the programm in which window situations it should inhibit.
# In the example below you have "Telegram" as a porgram name (application name or class_group_name).
# the 2 behind the "count" means, that the PC will inhibit, if the application ("Telegram") has 2 or more windows open
# the "Vorschau" behind "title" of the "Anki" application means, that the PC will inhibit, if a window named "Vorschau" of the application named "Anki" is open
# to check out how your open windows (applications) are called, you can uncommennt print lines in the "windows_and_audio_filter.py" file (the first print is the following: "print("new window:")")
# info: the application title and the window title specified here only have to be part of the real title.
window_filter = {
    "Telegram": {"count": 2},
    "Audacity": {"count": 1},
    "Audio": {"title": "Audio-Rekorder"},
    "cinnamon-session": {"title": "Sitzung"},
}
# all: all detected audio playing inhibits the PC
# none: audio playing does not inhibit the PC
# ["application1", "application2"]: inhibit if audio comes form specified application (application1 or application2 in this example)
audio_filter = "all"
