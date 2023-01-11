# sleep-inhibitor-on-high-cpu-utilization
This python script checks your PC's cpu utilization percentage and inhibits the PC if the in the script specified percentage ("inhibit_percentage") is passed. 
Moreover, it can inhibit the PC if a specified application has too many (count can be specified) open windows or a window with a specified title is open. 

You can also change the inhibit behavior a little bit in the script "settings.py"). 

Because the script is written for Linux Mint Cinnamon, most of the settings regarding the inhibiting are only realizable with Cinnamon specific commands, although they might be adaptable for other distors. 

The only option which seems to not involve Cinnamon commands is to have a black screen and the screen locked when inhibiting ("lock_screen = True").

## installation: 
1. download the whole repository (as a zip and unpack it)

2. open the files ```main.py```, ```cpu_utilization``` and ```mywake.py``` with a text or code editor and edit the following: 

2.1 change the username from "adi" to your username in all lines "adi" is mentioned

2.2 change the uid (user id?) from "1000" to your id (possible ids can be found as foldernames at "/run/user") in the same lines

2.3 edit the settings or at least go over them (can be found in the file ```settings.py```)

3. set up systemctl (daemon)

3.1 create a file with the service name and ".service" in the end. Open the file with a text/code editor and write the following (and save it): 
```
[Unit]
Description=<<put service name here>> daemon

[Service]
ExecStart= <<path to the ```main.py``` file you downloaded (including the file name, you can rename the file if you want, but remember to change the path accordingly!)>>
Restart=always
RestartSec=10min

[Install]
WantedBy=default.target
```
3.2.1 open the path ```/etc/systemd/system``` 

3.2.2 right click on a blank space and click ```open as system manager```. It will ask you for your password, so you have to enter it. 

3.2.3 create a link to the service file you created (or copy paste it there).  It has to have the same name as the original file. 

3.3 open the terminal and 

3.4 Reload the system manager configuration: ```sudo systemctl daemon-reload```

3.5 Enable the service to start on boot: ```systemctl enable --now <<put service name here>>.service```

3.6 Start the service: ```sudo systemctl start <<put service name here>>.service```

The script should now be running as a service and will start automatically on boot. 

You can check the status of the service with ```sudo systemctl status --now <<put service name here>>.service``` and 

stop the service with ```sudo systemctl stop <<put service name here>>.service```.

To see the logs of the currently running service, you can type ```journalctl -u <<put service name here>>.service -b`


Like I said, most of it is Cinnamon specific because I had to type in the path to the power settings I have to change via commands. If you find a better way to change the settings or found a path/command for other distors, feel free to open up an issue or make a pull request!
If you have issues or a feature request, you can of course write that in an issue as well. 
