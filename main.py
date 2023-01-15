#!/usr/bin/env python3
import subprocess
import settings
import time
import os
import cpu_utilization
xvfb = subprocess.Popen(['Xvfb', ":1"])
os.environ['DISPLAY'] = ":1"
# start windows_and_audio_filter script with simulated Display
windows_and_audio_filter_subprocess = subprocess.Popen(
  # command to make this work when running in the background with systemctl 
  # "adi": user name 
  # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
  'sudo -u adi env DISPLAY=:1 python3 /home/adi/Downloads/MprisWake-main/windows_and_audio_filter.py',
  shell=True,
  stderr=subprocess.PIPE
)
stderr = windows_and_audio_filter_subprocess.communicate()
if stderr:
  print("Error while initiating windows filter! Retrying with other simulated screen...")
  windows_and_audio_filter_subprocess = subprocess.Popen(
  # command to make this work when running in the background with systemctl 
  # "adi": user name 
  # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
  'sudo -u adi env DISPLAY=:0 python3 /home/adi/Downloads/MprisWake-main/windows_and_audio_filter.py',
  shell=True,
  )
cpu_utilization.start_checking()
# keep this script running
while True:
  try:
    time.sleep(max(settings.SLEEP_INTERVAL_SECONDS - 3, 1))
  except KeyboardInterrupt:
    windows_and_audio_filter_subprocess.kill()
    xvfb.kill()
    break
# import windows_and_audio_filter
