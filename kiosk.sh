#!/bin/bash
xset s noblank
xset s off
xset -dpms

unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

#this file will be created by createURLList.py
#and will contain the bash script used
#to open Chromium with the tabs populated
FILE=/home/pi/kiosk/start_browser.sh

B_SUCCESS=false
#have to initialize retCode, if not then later statement will always be 0
retCode=2

while [ ! $B_SUCCESS = true ]
do
   python3 /home/pi/kiosk/createURLList.py
   #get return code
   retCode=$?
    
   if [ $retCode = 0 ]; then
      B_SUCCESS=true
   else
      B_SUCCESS=false
      sleep 5
   fi
 
done

#Make file executable
chmod +x "$FILE"

#And execute it. The & makes it run in it's own session
source "$FILE" &

#this will issue a ctrl-TAB every xx seconds which will cycle
#through the pages on Chromium
while true; do
   xdotool keydown ctrl+Tab; xdotool keyup ctrl+Tab;
   sleep 8
done

