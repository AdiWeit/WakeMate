#!/usr/bin/env python3
import mywake
import settings
import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck
from gi.repository import Gtk
def on_window_opened(screen, window):
  # windows = screen.get_windows()
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

# checks if window_filter windows are open
wlist = []
def filtered_window_open():
  w_counter = {}
  for w in wlist:
    # if you want to check out how the open windows on your desktop are, you can uncomment the lines below and run the script in a termianl. 
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
      # if w.is_visible_on_workspace(active_wspace):
      #     # print(w.get_name())
# start the GTK main loop
Gtk.main()
