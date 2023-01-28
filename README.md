# WakeMate
This python script checks your PC's cpu utilization percentage and inhibits the PC if the in the script specified percentage (`inhibit_percentage`) is passed. 

Moreover, it can inhibit the PC if a specified application has too many (count can be specified) open windows or a window with a specified title is open. 

Furthermore, it can inhibit the PC if it detects audio playing in an open window (windows can be specified). 

You can also change the inhibit behavior a little bit in the script [`settings.py`](wakemate/settings.py)) script (located in the subfolder [`makemate`](wakemate/)). 

Because the script is written for Linux Mint Cinnamon, most of the settings regarding the inhibiting are only realizable with Cinnamon specific commands, although they might be adaptable for other distors. For example, for GNOME users it should be `gsettings set org.gnome.`...

The only option which seems to not involve Cinnamon commands is to have a black screen and the screen locked (at least on my PC) when inhibiting (`lock_screen = True`).

## installation: 
1. download the whole repository (as a zip and unpack it)

2. open the file [`WakeMate.service`](WakeMate.service) with a text or code editor and enter your path to the [`main.py`](`wakemate/main.py`) (you will find my path entered already, but you will have to edit it) 

2.1 open the file [`windows_and_audio_filter.py`](wakemate/windows_and_audio_filter.py) (located in the subfolder [`makemate`](wakemate/)) with a text or code editor and replace the 1000 with your uid (user id?) (possible ids can be found as foldernames at `/run/user/`) in the lines mentioned. 

2.2 edit the settings or at least go through them (can be found in the file [`settings.py`](wakemate/settings.py) located in the subfolder [`makemate`](wakemate/))

You may need to allow the [`main.py`](`wakemate/main.py`) script to be executed. 

3. set up systemctl (daemon)

3.1 open the folder you unpacked and create a link to the [`WakeMate.service`](WakeMate.service) file and copy it (or copy the file itself. A link should be prefered if you might edit the service file). If you want to give the service anther name, rename the file first. If you rename the file, you will have to replace the "WakeMate" with your service name in the following commands. 

3.2.1 open the path `/etc/systemd/user` 

3.2.2 right click on a blank space and click `open as system manager`. It will ask you for the (root) password, so you have to enter it. 

3.2.3 paste the [`service file`](WakeMate.service) you copied. It has to have the same name as the original file. 

3.3 open the terminal and 

3.4 Reload the system manager configuration: `systemctl --user daemon-reload`

3.5 Enable the service to start on boot: `systemctl enable --user --now WakeMate.service`

3.6 Start the service: `systemctl start --user --now WakeMate.service`

To restart the service, use `systemctl restart --user --now WakeMate.service`

You only have to do 4. if you want to set `lock_screen` to true. 

4. run `sudo visudo` in the terminal. It will ask for the password, so enter it.

note that the following key combinations might vary due to different editors that might be run. The key combinations should work for GNU nano. 

4.1 add the line "`username here` ALL=(ALL) NOPASSWD: /usr/bin/systemd-inhibit" (when you open the file manager (in nemo at least) and click on "personal", your username is the last bit of the path to the folder you are in)
  
  This line should make commands influencing systemd-inhibit (which is used for inhibiting the PC if `lock_screen = True` in the settings file) executable  without entering the sudo password for the entered user
  
4.2 exit the editor with ctrl + x
  
4.3 press "y" (english: yes, depends on the language) to save the changes
  
4.4 press enter to exit the editor

You may need to install rich (python library): `pip install rich`
 

The script should now be running as a service and will start automatically on boot. 

You can check the status of the service with `systemctl status --user WakeMate.service` and 

You can disable the service with `systemctl --user disable WakeMate.service`. This will stop the script and disable it, so it will not be started automatically after a reboot. If you want to enable it again (let it start on reboot), you have to type the command again (3.5)

If it is stuck (doesn't finish the process) enabling or starting the process, you can try disabling the script (with the command mentioned above) and following the steps from 3.4 to 3.6 again.

To see the logs created of the currently running service, you can type `journalctl --user -u WakeMate.service -b`

Like I said, most of it is Cinnamon specific because I had to type in the path to the power settings I have to change via commands. If you find a better way to change the settings or found a path/command for other distors, feel free to open up an issue or make a pull request!
If you have issues or a feature request, you can of course write that in an issue as well. 

Special thanks to [Nicolai Weitkemper](https://github.com/NicoWeio) for contributing to this project, espacially helping me with the restructuring of the architecture. 
