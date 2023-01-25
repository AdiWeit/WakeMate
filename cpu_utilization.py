#!/usr/bin/env python3
import psutil
from rich import print
from . import settings
from . import power_settings_manager
import threading
def cpu_working_hard(time_checking, inhibit_percentage):
  """"
  checks if cpu is "working hard" (cpu % > inhibit_percentage)
  """
  # checking utilization average the cpu average for [time_checking] seconds
  usage = psutil.cpu_percent(time_checking)
  print("cpu usage:", usage)
  power_settings_manager.update_time_inactive()
  return usage > inhibit_percentage

def update(callback):
  """
  checks if the cpu is working hard every [settings.SLEEP_INTERVAL_SECONDS] seconds
  """
  try:
    while True:
      callback({"type": "cpu working hard", "state": cpu_working_hard(settings.SLEEP_INTERVAL_SECONDS, settings.inhibit_percentage)})
  except KeyboardInterrupt:
    print("exit via key press")
# thread needed because of endless loop in update function
def start_checking(callback):
  thread = threading.Thread(target=update, args=(callback,))
  thread.daemon = True
  thread.start()
