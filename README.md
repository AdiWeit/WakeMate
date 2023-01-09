# sleep-inhibitor-on-high-cpu-utilization
This python script checks your PC's cpu utilization percentage and inhibits the PC if the in the script specified percentage ("inhibit_percentage") is passed. 

You can also change the inhibit behavior a little bit in the script ("user settings", beginning in line 6). 

The script is written for Linux Mint, but it might work for other cinnamon users as well. 

The only option which seems to not be specifically for cinnamon users is to have a black screen and the screen locked when inhibiting ("lock_screen = True").

## installation: 
1. download the main.py file or the whole repository

2. open the file with a text editor and edit the following: 

2.1 change the username from "adi" to your username in all lines "adi" is mentioned

2.2 change the uid (user id?) from "1000" to your id (possible ids can be found as foldernames at "/run/user")

2.3 edit the settings if you'd like to (can be found below the ```user settings``` comment)

3. set up systemctl (daemon)

3.1 create a file with the service name and ".service" in the end. Open the file with a text editor and write the following (and save it): 
```
[Unit]
Description=<<put service name here>> daemon

[Service]
ExecStart= <<path to the file you downloaded (main.py) (including the file name, you can rename the file if you want, but remember to change the path accordingly!)>>
Restart=always
RestartSec=10min

[Install]
WantedBy=default.target
```
3.2 open the terminal and 

3.3 Reload the system manager configuration: ```sudo systemctl daemon-reload```

3.4 Enable the service to start on boot: ```systemctl enable --now <<put service name here>>.service```

3.5 Start the service: ```sudo systemctl start <<put service name here>>.service```

The script should now be running as a service and will start automatically on boot. 

You can check the status of the service with ```sudo systemctl status --now <<put service name here>>.service``` and 

stop the service with ```sudo systemctl stop <<put service name here>>.service```.

To see the logs of the currently running service, you can type ```journalctl -u <<put service name here>>.service -b`


Most of it is cinnamon specific because I had to type in the path to the power settings I had to change. If you find you a better way to change the settings feel free to open up an issue or make a pull request!
If you have issues or a feature request, you can of course write that in an issue as well. 
