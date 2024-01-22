# RD2024 Mobile Robot Workshop


## Connection

1. Starten Turtlebot
2. PC mit Router verbinden
3. SSH verbinden
    ```
    ssh username@ip_address
    ```
4. Falls nicht gestartet auf turtlebot
   ```
    roslaunch turtlebot3_bringup turlebot3_robot.launch
   ```
6. ROS launch file starten

## Remote Connection

Verbindung aufsetzen wie [hier](http://wiki.ros.org/turtlebot/Tutorials/indigo/Network%20Configuration) beschrieben.

Im `~/.bashrc` folgendes ergänzen:
```BASH
export ROS_MASTER_URI=http://IP_OF_TURTLEBOT:11311
export ROS_HOSTNAME=IP_OF_PC    # IP von ifconfig
```

## Benutzerdaten
username: ubuntu
password: MR-Robots
ip_adresse: 192.168.100.5X

WLan Daten
Name: TurtlebotX
Passwort von Zettel WLAN-Netzwerkschlüssel
