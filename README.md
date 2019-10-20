# kiosk #
Raspberry Pi Kiosk Display

This document describes the use of a Raspberry Pi to display a series of web pages to Maker Nexus memebrs that might include the current members checked-in with their RFID, the calender, and any other pertient information 
 
This Kiosk is based primarily on these instructions
https://pimylifeup.com/raspberry-pi-kiosk/

If you have any questions contact **craig.colvin@makernexus.org**


Installation
-------------

The basic steps are:
- Install Raspbian on Raspberry Pi
- Connect to MakerNexus wifi
- Install additional packages on RPi such as xdotool, unclutter, and sed
- download files into the directory /home/pi/kiosk
- Move kiosk.service file to system directory
- Register kiosk.service so it runs at bootup as a service
- Generate list of web pages to display


Installing Additional Tools
---------------------------
On the RPi we run the following command

 `sudo apt-get install xdotool unclutter sed

This installs the following
- xdotool which allows our bash script to execute key presses without anyone being on the device. 
- unclutter package, will enable us to hide the mouse from the display.
- sed is used to change settings in the browser to deal with any errors


The Kiosk.sh Script
---------------------
This script file is what is run by the service at boot. 

Some items that you might want to edit
- The hardcoded directory */home/pi/kiosk*
- The number of seconds to wait before displaying a new page


Setting Up the Kiosk to Start at Boot
--------------------------------------

- Move the kiosk.service file to
    `/lib/systemd/system/`

- Set the service to run at bootup

  `sudo systemctl enable kiosk.service`

Now when we reboot we get a full screen web page displayed.

Some items that you might want to edit
- The hardcoded directory */home/pi/kiosk*


Listing What Web Pages to Display
----------------------------------
The web page http://makernexus.com/kiosk-links contains a list of URLS located between the tags
**kiosk_list_start** and **kiosk_list_stop**. Any html links located between those two tags will be displayed
on the kiosk.

One other weird hack to note. 
Wix will not allow just any URL to be assigned as a HTML link. The Maker Nexus Calendar is supposed to be http://localhost but Wix won't allow it. So I did another hack to work around that. When the code encounters the URL http://mncalendar.html it will replace it with http://localhost


createURLList.py
----------------
This Python script is what parses the web page kiosk-links and creates a script file that will load each page in a tab in Chromium.

Some items that you might want to edit
- The hardcoded directory */home/pi/kiosk*
- The URL of kiosk-links (currently https://www.makernexus.com/kiosk-links)

Final Points
------------
If you want to cancel the full screen web page press **ctrl-shift-w** to close Chromium

If the kiosk doesn't run you can use the following command to see the error messages

    sudo systemctl status kiosk.service
