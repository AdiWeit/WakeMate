#!/usr/bin/env python3
import settings
import cpu_utilization
import subprocess
import os
inhibiting = {}
def inhibit():
  global time_inactive
  # update time_inactive (important if user changed it)
  if list(cpu_utilization.get_time_inactive()["sleep"].values()) != [0, 0]:
    time_inactive = cpu_utilization.get_time_inactive()
  # inhibit PC
  if settings.lock_screen:
    os.system('sudo systemd-inhibit --why "{}" --what "sleep" script'.format("cpu level or open window(s)"))
  else:
    # sets the inactivity time until the PC goes to sleep when running on battery (not connected to charging cable) to never (0)
    run_subprocess('sleep-inactive-battery-timeout "0"')
    # sets the inactivity time until the PC goes to sleep when charging (ac connected) to never (0)
    run_subprocess('sleep-inactive-ac-timeout "0"')
    if settings.keep_screen_on:
      # sets the inactivity time until the screen goes black when running on battery (not connected to charging cable) to never (0)
      run_subprocess('sleep-display-battery "0"')
      # sets the inactivity time until the screen goes black when charging (ac connected) to never (0)
      run_subprocess('sleep-display-ac "0"')
def uninhibit():
  print("resetting to user settings: \nsleep:")
  print("decharging:", cpu_utilization.time_inactive["sleep"]["decharging"], "charging:", cpu_utilization.time_inactive["sleep"]["charging"])
  print("screen:")
  print("decharging:", cpu_utilization.time_inactive["screen"]["decharging"], "charging:", cpu_utilization.time_inactive["screen"]["charging"])
  # resetting settings to user settings because cpu is not working hard:
  # sets the inactivity time until the PC goes to sleep when running on battery (not connected to charging cable) to the stored value
  run_subprocess('sleep-inactive-battery-timeout "' + str(cpu_utilization.time_inactive["sleep"]["decharging"]) + '"')
  # sets the inactivity time until the PC goes to sleep when charging (connected to charging cable) to the stored value
  run_subprocess('sleep-inactive-ac-timeout "' + str(cpu_utilization.time_inactive["sleep"]["charging"]) + '"')
  # sets the inactivity time until the screen goes black when running on battery (not connected to charging cable) to the stored value
  run_subprocess('sleep-display-battery "' + str(cpu_utilization.time_inactive["screen"]["decharging"]) + '"')
  # sets the inactivity time until the screen goes black when charging (connected to charging cable) to the stored value
  run_subprocess('sleep-display-ac "' + str(cpu_utilization.time_inactive["screen"]["charging"]) + '"')
def change_inhibit(state, reason="cpu working hard"):
   global inhibiting
   inhibiting[reason] = state
   print("inhibiting:", inhibiting)
   check_inhibit()
def check_inhibit():
  global inhibiting
  if any(inhibiting.values()):
    inhibit()
  else:
    uninhibit()
def run_subprocess(setting):
  subprocess.run(
  # command to make this work when running in the background with systemctl 
  # "adi": user name 
  # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
  'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ' + 
  'dconf write /org/cinnamon/settings-daemon/plugins/power/' + setting, 
  shell=True
  )
