#!/usr/bin/env python3
import mywake
import settings
import gi
import time
import subprocess
import threading
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
from gi.repository import Gtk
windows_detected = False
def on_window_opened(screen, window):
  # windows = screen.get_windows()
  global windows_detected
  windows_detected = True
  global wlist
  wlist.append(window)
  if (filtered_window_open()):
    mywake.change_inhibit(True, "filtered window open")
def on_window_closed(screen, window):
  # windows = screen.get_windows()
  global wlist
  wlist.remove(window)
  if (not filtered_window_open()):
    mywake.change_inhibit(False, "filtered window open")
screen = Wnck.Screen.get_default()
screen.connect("window-opened", on_window_opened)
screen.connect("window-closed", on_window_closed)

wlist = []
# checks if window_filter windows are open
def filtered_window_open():
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
def check_windows_detected():
  time.sleep(6)
  if not windows_detected:
    Gtk.main_quit()
    thread.stop()
    print("No windows detected! retrying with other virtual display...")
    subprocess.Popen(
    # command to make this work when running in the background 
    # "adi": user name 
    # "1000": uid (user id?, possible ids can be found as foldernames at "/run/user"))
    'sudo -u adi env DISPLAY=:0 python3 /home/adi/Downloads/MprisWake-main/windows_and_audio_filter.py',
    shell=True,
    )
  else:
    print("windows detected!")
    thread1 = threading.Thread(target=check_audio_playing)
    thread1.daemon = True
    thread1.start()
def check_audio_playing():
  try:
    output = subprocess.run("sudo -u adi env XDG_RUNTIME_DIR=/run/user/1000 pactl list sink-inputs", shell=True, capture_output=True, text=True)
    outputs = str(output).split(" #")
  except Exception as err:
    print(err)
  try:
    for window_output in outputs:
      for window in wlist:
        if str(window.get_pid()) in window_output and ("state: RUNNING" in window_output or "Unterbrochen: nein" in window_output):
          print("Audio played by application " + window.get_application().get_name())
          if settings.audio_filter == "all":
            mywake.change_inhibit(True, "music playing")
            raise Exception ("end loop")
          elif type(settings.audio_filter) == list:
            for app in settings.audio_filter:
              if app in window.get_application().get_name() or app in window.get_class_group_name():
                mywake.change_inhibit(True, "music playing")
                raise Exception ("end loop")

  except:
    pass
  else:
    mywake.change_inhibit(False, "music playing")
  time.sleep(settings.SLEEP_INTERVAL_SECONDS)
  check_audio_playing()
# start check_windows_detected function in a thread in order to be able to execute Gtk.main() (is also an endless loop)
thread = threading.Thread(target=check_windows_detected)
thread.daemon = True
thread.start()
subprocess.run(['python', '-c', 'check_windows_detected()'])
# start the GTK main loop
Gtk.main()
