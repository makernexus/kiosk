#!/bin/bash
#this file gets overwritten by createURLList.py
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk \
 http://localhost \
 http://rfid.makernexuswiki.com/rfidcurrentcheckins.php \
 https://www.makernexus.com/kiosk-1 &

