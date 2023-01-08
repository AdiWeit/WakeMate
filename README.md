# sleep-inhibitor-on-high-cpu-utilization
This python script checks your PC's cpu utilization percentage and inhibits the PC if the in the script specified percentage ("inhibit_percentage") is passed. 

You can also change the inhibit behavior a little bit in the script ("user settings", beginning in line 6). 

The script is written for Linux Mint, but it might work for other cinnamon users as well. 

The only option which seems to not be specifically for cinnamon users is to have a black screen and the screen locked when inhibiting ("lock_screen = True").

## installation: 
1. download the main.py file or the whole repository
2. set up systemctl (daemon)

2.1 create a file with the service name and ".service" in the end. In the file, write the following (and save it): 
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
2.2 open the terminal and 

2.3 Reload the system manager configuration: ```sudo systemctl daemon-reload```

2.4 Enable the service to start on boot: ```systemctl enable --now <<put service name here>>.service```

2.5 Start the service: ```sudo systemctl start <<put service name here>>.service```

The script should now be running as a service and will start automatically on boot. 

You can check the status of the service with ```sudo systemctl status --now <<put service name here>>.service``` and 

stop the service with ```sudo systemctl stop <<put service name here>>.service```.

To see the logs of the currently running service, you can type ```journalctl -u <<put service name here>>.service -b`


Most of it is cinnamon specific because I had to type in the path to the power settings I had to change. If you find you a better way to change the settings feel free to open up an issue or make a pull request!
If you have issues or a feature request, you can of course write that in an issue as well. 
