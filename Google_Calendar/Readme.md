# Google Calendar in Kiosk #
Displaying the Maker Nexus Google Calendar in one of the Kiosk tabs

Most of the below is from https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md

Basically we need to create a web server on the Raspberry Pi and create a web page to display which will show the Google calendar.

Steps
-----
- Install Apache
- Put the file index.html into the folder

    `/var/www/html`
    
- Call the web page using *http://localhost*

Installing Apache
-----------------
Update the available packages

    sudo apt update
    
Then install apache2

    sudo apt install apache2 -y

#To Get Rid of Scroll Bars#
Use these dimensions when creating the embedded Google calendar

    Height = 1050
    Width = 1900

