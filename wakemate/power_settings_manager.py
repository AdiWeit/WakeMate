
import subprocess
from . import settings
import os
def read_setting(setting):
  return int(subprocess.run(
  'dconf read /org/cinnamon/settings-daemon/plugins/power/' + setting, 
  shell=True,
  stdout=subprocess.PIPE
  ).stdout.strip().decode())
def write_setting(setting):
  subprocess.run(
  'dconf write /org/cinnamon/settings-daemon/plugins/power/' + setting, 
  shell=True
  )
time_inactive = settings.default_time_inactive
# get the current time_inactive (power) settings
def get_time_inactive():
  return  {
    "sleep": {
      "decharging":
        # getting the inactivity time unitl the PC goes to sleep when running on battery (not connected to charging cable)
        read_setting('sleep-inactive-battery-timeout'),
      "charging":
        # getting the inactivity time unitl the PC goes to sleep when charging (ac connected)
        read_setting('sleep-inactive-ac-timeout')
      },
    "screen": {
      "decharging":
        # getting the inactivity time unitl the screen goes blank when running on battery (not connected to charging cable)
        read_setting('sleep-display-battery'),
      "charging":
        # getting the inactivity time unitl the screen goes blank when charging (ac connected)
        read_setting('sleep-display-ac')
    },
  }
def update_time_inactive():
  # update time_inactive (important if user changed it)
  if list(get_time_inactive()["sleep"].values()) != [0, 0]:
    global time_inactive
    time_inactive = get_time_inactive()
def inhibit():
  global time_inactive
  # update time_inactive (important if user changed it)
  if list(get_time_inactive()["sleep"].values()) != [0, 0]:
    time_inactive = get_time_inactive()
  # inhibit PC
  if settings.lock_screen:
    os.system('sudo systemd-inhibit --why "MyWake" sleep ' + str(settings.SLEEP_INTERVAL_SECONDS + 1))
  else:
    # sets the inactivity time until the PC goes to sleep when running on battery (not connected to charging cable) to never (0)
    write_setting('sleep-inactive-battery-timeout "0"')
    # sets the inactivity time until the PC goes to sleep when charging (ac connected) to never (0)
    write_setting('sleep-inactive-ac-timeout "0"')
    if settings.keep_screen_on:
      # sets the inactivity time until the screen goes black when running on battery (not connected to charging cable) to never (0)
      write_setting('sleep-display-battery "0"')
      # sets the inactivity time until the screen goes black when charging (ac connected) to never (0)
      write_setting('sleep-display-ac "0"')
def uninhibit():
  print("resetting to user settings: \nsleep:")
  print("decharging:", time_inactive["sleep"]["decharging"], "charging:", time_inactive["sleep"]["charging"])
  print("screen:")
  print("decharging:", time_inactive["screen"]["decharging"], "charging:", time_inactive["screen"]["charging"])
  # resetting settings to user settings because cpu is not working hard:
  # sets the inactivity time until the PC goes to sleep when running on battery (not connected to charging cable) to the stored value
  write_setting('sleep-inactive-battery-timeout "' + str(time_inactive["sleep"]["decharging"]) + '"')
  # sets the inactivity time until the PC goes to sleep when charging (connected to charging cable) to the stored value
  write_setting('sleep-inactive-ac-timeout "' + str(time_inactive["sleep"]["charging"]) + '"')
  # sets the inactivity time until the screen goes black when running on battery (not connected to charging cable) to the stored value
  write_setting('sleep-display-battery "' + str(time_inactive["screen"]["decharging"]) + '"')
  # sets the inactivity time until the screen goes black when charging (connected to charging cable) to the stored value
  write_setting('sleep-display-ac "' + str(time_inactive["screen"]["charging"]) + '"')
