# -*- coding: utf-8 -*-

import urllib3 as urllib
import xml.etree.ElementTree as ET
import time, htmlParser

g_apiRoot = "http://www.omgubuntu.co.uk/rss"
g_lastTimestamp = None

def requestXMLContent():
    http = urllib.PoolManager()
    r = http.request('GET', g_apiRoot)

    if r.status != 200:
        print("Request to {1} failed with status: {2}".format(g_apiRoot, r.status))
        return false
    else:
        data = r.data
        return data


def parseDescriptionString(description_string):
    s = cleanString(description_string)
    parser = htmlParser.customHTMLParser()
    parser.feed(s)
    return parser.retrieve_info()

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

def parseXMLtoJSON(xmlData):
    root = ET.fromstring(xmlData)
    time_text = root[0].find('lastBuildDate').text.split(" ")
    timestamp = time.strptime(time_text[0][:-1] + " " +  time_text[2] + " " + time_text[1] + " " + time_text[4] + " " + time_text[3])

    global g_lastTimestamp
    if not g_lastTimestamp:
        g_lastTimestamp = timestamp

    else:
        if g_lastTimestamp == timestamp:
            print("DEBUG: last timestamp: {0}, current timestamp: {1}".format(time.strftime("%a %b %d %H:%M:%S %Y", g_lastTimestamp), time.strftime("%a %b %d %H:%M:%S %Y", timestamp)))
            #nothing has changed since last update, so we can return
            return

    #getting all items
    items = root[0].findall('item')
    jsonString = """{"""
    item_id = 0

    for item in items:
        title = item.find('title').text
        url = item.find('link').text

        desc, short_desc, author, image = parseDescriptionString(item.find('description').text[:-1])

        if item == items[-1]:
            jsonString += """\"{0}\" : [{{\"title\": \"{1}\", \"description\":\"{2}\", \"short-desc\": \"{3}\", \"author\": \"{4}\", \"image\": \"{5}\", \"ressource-url\":\"{6}\"}}]""".format(item_id, title, desc, short_desc, author, image, url)
        else:
            jsonString += """\"{0}\" : [{{\"title\": \"{1}\", \"description\":\"{2}\", \"short-desc\": \"{3}\", \"author\": \"{4}\", \"image\": \"{5}\", \"ressource-url\":\"{6}\"}}], """.format(item_id, title, desc, short_desc, author, image, url)
        item_id += 1

    jsonString = jsonString + """}"""
    return str(jsonString)

if __name__ == "__main__":
    data = requestXMLContent
    json = parseXMLtoJSON(data)
    with open("omgubuntu.json", "w") as of:
        of.write(json)
