#!/usr/bin/env python3
import subprocess
import psutil
import settings
import mywake
import threading
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

time_inactive = settings.default_time_inactive
# get the current time_inactive (power) settings
def get_time_inactive():
  return  {
    "sleep": {
      "decharging":
        # getting the inactivity time unitl the PC goes to sleep when running on battery (not connected to charging cable)
        get_settings_subprocess('sleep-inactive-battery-timeout'),
      "charging":
        # getting the inactivity time unitl the PC goes to sleep when charging (ac connected)
        get_settings_subprocess('sleep-inactive-ac-timeout')
      },
    "screen": {
      "decharging":
        # getting the inactivity time unitl the screen goes blank when running on battery (not connected to charging cable)
        get_settings_subprocess('sleep-display-battery'),
      "charging":
        # getting the inactivity time unitl the screen goes blank when charging (ac connected)
        get_settings_subprocess('sleep-display-ac')
    },
  }

def update():
  try:
    while True:
      print("new run")
      if cpu_working_hard(settings.SLEEP_INTERVAL_SECONDS, settings.inhibit_percentage):
        mywake.change_inhibit(True)
      else:
        mywake.change_inhibit(False)
  except KeyboardInterrupt:
    print("exit via key press")
# thread needed because mywake has to be imported but imports this script
def start_checking():
  thread = threading.Thread(target=update)
  thread.daemon = True
  thread.start()
def get_settings_subprocess(setting):
  return int(subprocess.run(
  # command to make this work when running in the background with systemctl 
  # "adi": user name 
  # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
  'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
  'dconf read /org/cinnamon/settings-daemon/plugins/power/' + setting, 
  shell=True,
  stdout=subprocess.PIPE
  ).stdout.strip().decode())
