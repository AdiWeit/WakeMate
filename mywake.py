from . import windows_and_audio_filter
from . import cpu_utilization
from . import power_settings_manager
from rich import print
import time
checked_states = {}

def callback(state):
    checked_states[state["type"]] = state["state"]
    print(checked_states)
    if any(checked_states.values()):
      power_settings_manager.inhibit()
    else:
      power_settings_manager.uninhibit()

def start_checking():
    windows_and_audio_filter.start_checking(callback)
    cpu_utilization.start_checking(callback)
    while True:
        time.sleep(60)
