#!/usr/bin/env python3
import subprocess
import settings
import os
import time

xvfb = subprocess.Popen(['Xvfb', ':0'])
os.environ['DISPLAY'] = ':0'
# start windows_filter script with needed simulated Display
windows_filter_subprocess = subprocess.Popen(
  # command to make this work when running in the background with systemctl 
  # "adi": user name 
  # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
  'export DISPLAY=:0; sudo -H -u adi DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus '
    + 'python3 /home/adi/Downloads/MprisWake-main/windows_filter.py', 
    shell=True
)
# keep this script running
while True:
  try:
    time.sleep(max(settings.SLEEP_INTERVAL_SECONDS - 3, 1))
  except KeyboardInterrupt:
    # Handle keyboard interrupt e.g. exit gracefully
    windows_filter_subprocess.kill()
    xvfb.kill()
    break
import windows_filter
