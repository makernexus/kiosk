# testParseOfKioskList
#
# This will open the web page kiosk-list located on the makernexus.org server and
# will save the URLs of all links on that page that are between the text
# kiosk_list_start and kiosk_list_stop. This is a hack to deal with weirdness in
# the Maker Nexus website host Wix in that it needs to include headers/footers on every page
# (even if they aren't visible). If kiosk-list is moved to a web server that allows
# straight HTML pages then the kisok_list_start/stop requirement could be removed
#
# this type of code will be used to generate the list of URLs that the kiosk
# will display in the Chromium broswer

import urllib.request
import os
import sys
from html.parser import HTMLParser

listOfURLS = []

class MyHTMLParser(HTMLParser):
    bInList = False
    def handle_starttag(self, tag, attrs):

        if self.bInList == False:
            return

        #encountered start tag test if is a an 'a' tag
        if tag != 'a':
            return
        attr = dict(attrs)

        #add URL to list
        #print(attr['href'])

        #This is a hack to get around the fact that Wix won't allow a URL with //localhost so we 
        #use http://mncalendar.html in Wix and then change here in the code. 
        url = attr['href']
        if "mncalendar" in url:
            url="http://localhost"

        #listOfURLS.append(attr['href'])
        listOfURLS.append(url)
        
    def handle_endtag(self, tag):
        return
        

    def handle_data(self, data):
        #only want to parse a href tags specific to the kiosk
        #so add text before and after our URLs to indicate
        #where to start and stop parsing

        if "kiosk_list_start" in data:
            self.bInList = True

        if "kiosk_list_stop" in data:
            self.bInList = False

# create a parser object
myParser = MyHTMLParser()

# Attempt to read kiosk-list web page and then extract all URLs
try:
    response = urllib.request.urlopen('https://www.makernexus.com/kiosk-links')
    #print(response.info())
    
    # Get raw HTML data
    rawHtmlFromKioskList = response.read()
 
    response.close()  # best practice to close the file

    # feed html data into parser and extract '<a href>'
    myParser.feed(str(rawHtmlFromKioskList))

    # this is a hack to create write permissions for the file
    # if it was just created. Running this code directly from
    # bash gave the file the correct permissions but did not
    # when running as a service 
    #startFile = open("start_browser.sh", "w")
    #startFile.close()
    #os.chmod("start_browser.sh", 0o777)


    startFile = open("/home/pi/kiosk/start_browser.sh", "w")
    print("Made it here")
    startFile.write("#!/bin/bash\n")
    startFile.write("#This file is overwritten every reboot by createURLList.py\n")
    startFile.write("/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk \\\n")


    # Parser created a list of URLs, print them out
    for urlIndex in range(len(listOfURLS)): 
        strURL=listOfURLS[urlIndex]
        startFile.write(strURL)
        startFile.write(" \\\n")
        print(strURL) 

    startFile.write("&")

    #clean up and exit
    startFile.close()
    sys.exit(0)

except Exception as e:
    print("Encountered an error")
    print(str(e))
    sys.exit(2)