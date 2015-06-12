# -*- coding: utf-8 -*-
###
# Author: Daniel Waller <2waller@informatik.uni-hamburg.de>
#
# The Author is in no way affiliated with, nor in official cooperation with either
# OMG! Ubuntu! or the Ubuntu project.
#
# OMG! Ubuntu! is a member of the Ohso Ltd Network.
# © 2015 Ohso Ltd. All rights reserved.
#
# Ubuntu is a registered trademark of Canonical Ltd.
###

import urllib3 as urllib
import xml.etree.ElementTree as ET
import time, htmlParser

### Global variables
g_apiRoot = "http://www.omgubuntu.co.uk/rss"
g_lastTimestamp = None

###
# Establishes a connection to omgubuntu.co.uk/rss and attempts to retrieve
# the xml feed
# Could definitely do with some more graceful error/failure handling
#
# @return str – an rss xml feed || boolean – false if http status != 200
###
def requestXMLContent():
    http = urllib.PoolManager()
    r = http.request('GET', g_apiRoot)

    if r.status != 200:
        print("Request to {1} failed with status: {2}".format(g_apiRoot, r.status))
        return false
    else:
        data = r.data
        return data

###
# Helper function to keep the body of the parseXMLtoJSON function less cluttered
# Creates an HTMLParser instance for every rss item that is passed to it and
# retrieves the desired information that has been parsed from the contained html
#
# @param str – the <description> part of an <item> from the source xml
# @return str, str, str, str – the long description, short description, author,
# and thumbnail url as parsed from the html
###
def parseDescriptionString(description_string):
    s = cleanString(description_string)
    parser = htmlParser.customHTMLParser()
    parser.feed(s)
    return parser.retrieve_info()

###
# Not sure if completely necessary, but I got strange errors before, that
# apparently stemmed from escaped html entities and utf-8 chars
# This function cleans out the most common things I encountered
#
# @param str – a string to be cleaned of special chars that might cause problems
# @return str – a cleaned string
###
def cleanString(xmlString):
    out = str(xmlString)
    out = out.replace("\xc2\xa0", " ")
    out = out.replace("\xa0", " ")
    out = out.replace("\\'", "'")
    out = out.replace("\xe2\x80\xa6", "...")
    out = out.replace("\xe2\x80\x93", " - ")
    out = out.replace("\xe2\x80\x94", " - ")
    out = out.replace("&#8217;", "'") #combining right and left single quotation mark
    out = out.replace("&#8216;", "'")
    out = out.replace("&rsquo;", "'")
    out = out.replace("&#8230;", "...")

    return str(out)

###
# Main logic of the service. Reads the timestamp from the retrieved xml and decides
# whether or not the json files have to be rebuilt.
# If yes, retrieves all <item> tags from the rss feed and processes each item
# individually by extracting 'title', 'link' to the original content, and passes
# the description body on to a helper function that communicates with the htmlParser
# to retrieve information about the article such as author and thumbnail.
# Finally builds a json string for each element and appends them to a json object
#
# @param str – the complete xml document retrieved from omgubuntu.co.uk/rss
# @return str – a complete json object representing all the relevant data from the rss feed
###
def parseXMLtoJSON(xmlData):
    root = ET.fromstring(xmlData)
    time_text = root[0].find('lastBuildDate').text.split(" ")
    #rearanging the timestamp to fit strptimes "%a %b %d %H:%M:%S %Y" pattern
    timestamp = time.strptime(time_text[0][:-1] + " " +  time_text[2] + " " + time_text[1] + " " + time_text[4] + " " + time_text[3])

    global g_lastTimestamp

    if not g_lastTimestamp: #when the service is started for the first time
        g_lastTimestamp = timestamp
    else:
        if g_lastTimestamp == timestamp:
            print("DEBUG: last timestamp: {0}, current timestamp: {1}".format(time.strftime("%a %b %d %H:%M:%S %Y", g_lastTimestamp), time.strftime("%a %b %d %H:%M:%S %Y", timestamp)))
            #nothing has changed since last update, so we can return
            return

    #getting all <item> tags from the root
    items = root[0].findall('item')
    jsonString = """{""" #opening the jsonString
    item_id = 0

    for item in items:
        title = item.find('title').text
        url = item.find('link').text

        desc, short_desc, author, image = parseDescriptionString(item.find('description').text[:-1]) #cutting the last character as it is a new line ("\n")

        if item == items[-1]: #If we're at the last item in the list, don't put a comma after the element
            jsonString += """\"{0}\" : [{{\"title\": \"{1}\", \"description\":\"{2}\", \"short-desc\": \"{3}\", \"author\": \"{4}\", \"image\": \"{5}\", \"ressource-url\":\"{6}\"}}]""".format(item_id, title, desc, short_desc, author, image, url)
        else:
            jsonString += """\"{0}\" : [{{\"title\": \"{1}\", \"description\":\"{2}\", \"short-desc\": \"{3}\", \"author\": \"{4}\", \"image\": \"{5}\", \"ressource-url\":\"{6}\"}}], """.format(item_id, title, desc, short_desc, author, image, url)
        item_id += 1

    jsonString = jsonString + """}""" #closing the jsonString

    return str(jsonString)

###
# Just for quick testing purposes. This will be rewritten into a class
# and started as a daemon on my server
###
if __name__ == "__main__":
    data = requestXMLContent
    json = parseXMLtoJSON(data)
    with open("omgubuntu.json", "w") as of:
        of.write(json)
