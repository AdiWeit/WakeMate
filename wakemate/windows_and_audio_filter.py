import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Wnck', '3.0')
from gi.repository import Gtk
from gi.repository import Wnck

from rich import print
from . import settings
import time
import subprocess
import threading

def on_window_opened(screen, window):
    # windows = screen.get_windows()
    global wlist
    wlist.append(window)

def on_window_closed(screen, window):
    # windows = screen.get_windows()
    global wlist
    wlist.remove(window)
screen = Wnck.Screen.get_default()
assert screen, "Error: unable to get the default screen!"
screen.connect("window-opened", on_window_opened)
screen.connect("window-closed", on_window_closed)
wlist = []

def filtered_window_open():
    """
    checks if filtered windows (window_filter) are open
    """
    w_counter = {}
    for w in wlist:
        # if you want to check out as the open windows (applications) on your desktop are called, you can uncomment the lines below and run the script in a termianl.
        # print("new window:")
        # print("application name: ", w.get_application().get_name())
        # print("class group: ", w.get_class_group_name())
        # print("window name: ", w.get_name())
        for settings_w in settings.window_filter.keys():
            if settings_w in w.get_application().get_name() or settings_w in w.get_class_group_name():
                if not settings_w in w_counter:
                    w_counter[settings_w] = 0
                w_counter[settings_w] += 1
                if ("count" in settings.window_filter[settings_w].keys() and w_counter[settings_w] >= settings.window_filter[settings_w]["count"]) or ("title" in settings.window_filter[settings_w].keys() and settings.window_filter[settings_w]["title"] in w.get_name()):
                    return True
    return False


def windows_and_audio_checker(callback):
  """
  checks if filetered windows are open or audio is playing (in filtered windows)
  """
  while True:
      # checks if filetered windows are open
      callback({"type": "window open", "state": filtered_window_open()})
      try:
          output = subprocess.run(
            # 1000: uid (user id?)
              "env XDG_RUNTIME_DIR=/run/user/1000 pactl list sink-inputs", shell=True, capture_output=True, text=True)
          outputs = str(output).split(" #")
      except Exception as err:
          print(err)
      try:
          for window_output in outputs:
              for window in wlist:
                # checking if window_output (audio) is running
                  if str(window.get_pid()) in window_output and ("state: RUNNING" in window_output or "Unterbrochen: nein" in window_output):
                      print("Audio played by application " +
                            window.get_application().get_name())
                      # checking if filter requirements are fulfilled
                      if settings.audio_filter == "all":
                          callback({"type": "audio playing", "state": True})
                          raise Exception("end loop")
                      elif type(settings.audio_filter) == list:
                          for app in settings.audio_filter:
                              if app in window.get_application().get_name() or app in window.get_class_group_name():
                                  callback(
                                      {"type": "audio playing", "state": True})
                                  raise Exception("end loop")
      except:
          pass
      else:
          callback({"type": "audio playing", "state": False})
          pass

      time.sleep(settings.SLEEP_INTERVAL_SECONDS)

def start_checking(callback):
    thread = threading.Thread(
        target=windows_and_audio_checker, args=(callback,))
    thread.daemon = True
    thread.start()
    thread = threading.Thread(
        target=Gtk.main)
    thread.daemon = True
    thread.start()
