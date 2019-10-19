# kiosk
Raspberry Pi Kiosk Display

This document describes the use of a Raspberry Pi to display a web page that shows the current members checked-in with their RFID.
 
Basically this is a full screen web browser displaying the page
http://rfid.makernexuswiki.com/rfidcurrentcheckins.php

If you have any questions contact craig.colvin@makernexus.org

This Kiosk is based primarily on these instructions
https://pimylifeup.com/raspberry-pi-kiosk/


The basic steps are:
- Install Raspbian on Raspberry Pi
- Connect to MakerNexus wifi
- Install additional packages on RPi such as xdotool, unclutter, and sed
- Create a kiosk.sh script file that prevents power management and what to display
- Making the kiosk run at bootup as a service

---------------------------
Installing Additional Tools
---------------------------
On the RPi we run the following command

sudo apt-get install xdotool unclutter sed

This installs the following
- xdotool which allows our bash script to execute key presses without anyone being on the device. 
- unclutter package, will enable us to hide the mouse from the display.
- sed is used to change settings in the browser to deal with any errors

---------------------
The Kiosk.sh Script
---------------------
xset at the beginning prevent the RPi power management from blanking the display.
Unclutter hides the mouse button after 0.5 seconds of inactivity.
The sed commands make the Chromium browser not display warning bars and if it crashes to restart.

The next section runs a python script to create the file start_browser.sh
It parses the web page located at http://makernexus.org/kiosk-links and extracts the URLs that will open in tabs in Chromium. The start_browser.sh script
will start Chromium in kiosk mode with the tabs found on the kiosk-links page.

The final portion of the script uses xdotool to simulate keystrokes to cycle through the tabs at a 8 second interval.


--------------------------------------
Setting Up the Kiosk to Start at Boot
--------------------------------------
We are now going to create a service file that will be used at startup.

Create the Kiosk service file using the nano editor

sudo nano /lib/systemd/system/kiosk.service

The following is the contents of the file

------------------------------------------------------------------------------------
[Unit]
Description=Chromium Kiosk
Wants=graphical.target
After=graphical.target

[Service]
Environment=DISPLAY=:0.0
Environment=XAUTHORITY=/home/pi/.Xauthority
Type=simple
ExecStart=/bin/bash /home/pi/kiosk/kiosk.sh
Restart=on-abort
User=pi
Group=pi

[Install]
WantedBy=graphical.target

------------------------------------------------------------------------------------

Now we set the service to run at bootup

sudo systemctl enable kiosk.service

Now when we reboot we get a full screen web page displayed.

------------
Final Points
------------
If you want to cancel the full screen web page press ctrl-shift-w to close Chromium
