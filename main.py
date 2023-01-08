#!/usr/bin/env python3
import psutil
import os
import subprocess

# user settings
SLEEP_INTERVAL_SECONDS = 15
# percentage the cpu has to reach for the PC to inhibit (stay on)
inhibit_percentage = 2
# locks the screen when the PC normally goes to sleep. 
# If it is set to True, it directly inhibits the PC. If set to False, it will set the inactivity time until going to sleep to never. 
# If the PC is set to enter the lockscreen (setting in screensaver settings menu) it will still do that if keep_screen_on is False. 
lock_screen = False
# inhibits the black screen (lock_screen must be set to False)
keep_screen_on = False

# after the time_inactive time (in mili sec.) the PC would normally go to sleep
time_inactive = {"screen": {"decharging": 300, "charging": 300}, "sleep": {"decharging": 600, "charging": 600}}
# get the current time_inactive (power) settings
def get_time_inactive():
  return  {
    "sleep": {
      "decharging":
        # getting the inactivity time unitl the PC goes to sleep when running on battery (not connected to charging cable)
        int(subprocess.run(
          # command to make this work when running in the background with systemctl 
          # "adi": user name 
          # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
          'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' +
          'dconf read /org/cinnamon/settings-daemon/plugins/power/sleep-inactive-battery-timeout', 
          shell=True, 
          stdout=subprocess.PIPE
        ).stdout.strip().decode()),
      "charging":
        # getting the inactivity time unitl the PC goes to sleep when charging (ac connected)
        int(subprocess.run(
          # command to make this work when running in the background with systemctl 
          # "adi": user name 
          # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
          'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
          'dconf read /org/cinnamon/settings-daemon/plugins/power/sleep-inactive-ac-timeout', 
          shell=True, 
          stdout=subprocess.PIPE
        ).stdout.strip().decode()),
      },
    "screen": {
      "decharging":
        # getting the inactivity time unitl the screen goes blank when running on battery (not connected to charging cable)
        int(subprocess.run(
          # command to make this work when running in the background with systemctl 
          # "adi": user name 
          # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
          'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' +
          'dconf read /org/cinnamon/settings-daemon/plugins/power/sleep-display-battery', 
          shell=True, 
          stdout=subprocess.PIPE
        ).stdout.strip().decode()),
      "charging":
        # getting the inactivity time unitl the screen goes blank when charging (ac connected)
        int(subprocess.run(
          # command to make this work when running in the background with systemctl 
          # "adi": user name 
          # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
          'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
          'dconf read /org/cinnamon/settings-daemon/plugins/power/sleep-display-ac', 
          shell=True, 
          stdout=subprocess.PIPE
        ).stdout.strip().decode()),
    },
  }
def inhibit(reason="cpu working hard"):
  print("inhibit (reason: {})".format(reason))
  # update time_inactive (important if user changed it)
  global time_inactive
  if list(get_time_inactive()["sleep"].values()) != [0, 0]:
    time_inactive = get_time_inactive()
  # inhibit PC
  if lock_screen:
    os.system('sudo systemd-inhibit --why "{}" --what "sleep" script'.format(reason))
  else:
    # sets the inactivity time until the PC goes to sleep when running on battery (not connected to charging cable) to never (0)
    subprocess.run(
      # command to make this work when running in the background with systemctl 
      # "adi": user name 
      # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
      'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
      'dconf write /org/cinnamon/settings-daemon/plugins/power/sleep-inactive-battery-timeout "0"',
      shell=True
    )
    # sets the inactivity time until the PC goes to sleep when charging (ac connected) to never (0)
    subprocess.run(
      # command to make this work when running in the background with systemctl 
      # "adi": user name 
      # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
      'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
      'dconf write /org/cinnamon/settings-daemon/plugins/power/sleep-inactive-ac-timeout "0"', 
      shell=True
    )
    if keep_screen_on:
      # sets the inactivity time until the screen goes black when running on battery (not connected to charging cable) to never (0)
      subprocess.run(
        # command to make this work when running in the background with systemctl 
        # "adi": user name 
        # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
        'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
        'dconf write /org/cinnamon/settings-daemon/plugins/power/sleep-display-battery "0"',
        shell=True
      )
      # sets the inactivity time until the screen goes black when charging (ac connected) to never (0)
      subprocess.run(
        # command to make this work when running in the background with systemctl 
        # "adi": user name 
        # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
        'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
        'dconf write /org/cinnamon/settings-daemon/plugins/power/sleep-display-ac "0"', 
        shell=True
      )

# checks if cpu is "working hard" (cpu% > inhibit_percentage)
def cpu_working_hard(time_checking, inhibit_percentage):
  # Calling psutil.cpu_precent() for [time_checking] seconds
  usage = psutil.cpu_percent(time_checking)
  print("cpu usage:", usage)
  # update time_inactive (important if user changed it)
  if list(get_time_inactive()["sleep"].values()) != [0, 0]:
    global time_inactive
    time_inactive = get_time_inactive()
  return usage > inhibit_percentage

# starts the program/checking for cpu percentage
try:
  while True:
    print("new run")
    if cpu_working_hard(SLEEP_INTERVAL_SECONDS, inhibit_percentage):
      inhibit()
    else:
      print("resetting to user settings: \nsleep:")
      print("dechargind:", time_inactive["sleep"]["decharging"], "charging:", time_inactive["sleep"]["charging"])
      print("screen:")
      print("dechargind:", time_inactive["screen"]["decharging"], "charging:", time_inactive["screen"]["charging"])
      # resetting settings to user settings because cpu is not working hard:
      # sets the inactivity time until the PC goes to sleep when running on battery (not connected to charging cable) to the stored value
      subprocess.run(
        # command to make this work when running in the background with systemctl 
        # "adi": user name 
        # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
        'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
        'dconf write /org/cinnamon/settings-daemon/plugins/power/sleep-inactive-battery-timeout "' + str(time_inactive["sleep"]["decharging"]) + '"', 
        shell=True
      )
      # sets the inactivity time until the PC goes to sleep when charging (connected to charging cable) to the stored value
      subprocess.run(
        # command to make this work when running in the background with systemctl 
        # "adi": user name 
        # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
        'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
        'dconf write /org/cinnamon/settings-daemon/plugins/power/sleep-inactive-ac-timeout "' + str(time_inactive["sleep"]["charging"]) + '"', 
        shell=True
      )
      # sets the inactivity time until the screen goes black when running on battery (not connected to charging cable) to the stored value
      subprocess.run(
        # command to make this work when running in the background with systemctl 
        # "adi": user name 
        # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
        'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
        'dconf write /org/cinnamon/settings-daemon/plugins/power/sleep-display-battery "' + str(time_inactive["screen"]["decharging"]) + '"', 
        shell=True
      )
      # sets the inactivity time until the screen goes black when charging (connected to charging cable) to the stored value
      subprocess.run(
        # command to make this work when running in the background with systemctl 
        # "adi": user name 
        # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
        'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
        'dconf write /org/cinnamon/settings-daemon/plugins/power/sleep-display-ac "' + str(time_inactive["screen"]["charging"]) + '"', 
        shell=True
      )
except KeyboardInterrupt:
    pass
