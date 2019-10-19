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
FILE=/home/pi/start_browser.sh

#remove file if it already exists
if [ -d "$FILE" ]; then
   rm "$FILE"
fi

#run createURLList.py script to get URLS from web
#
#this is done in a loop because sometimes the 
#internet connection takes a while to establish
#so we keep trying until the file is created.
while [ ! -f "$FILE" ]
do 
   python3 /home/pi/createURLList.py
   sleep 5
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

