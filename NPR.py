__author__ = 'scottsfarley'
##NPR uses xml to distribute their transcripts --> much faster than parsing all of the html junk.
from utils import *
from Config import NPR
import urllib2
import json
import pprint
import xml.etree.ElementTree as ET


def getDay(searchTerm, day):
    D = Day(day)
    ##build api call
    apiKey = NPR.apiKey
    endpoint = "http://api.npr.org/query?"
    url = endpoint + "searchTerm=" + searchTerm
    url += "&startDate=" + rawDatestringToURLdateString(day)
    url += "&endDate=" + rawDatestringToURLdateString(day)

    ##write in JSON format
    url += '&output=JSON'

    url += "&apiKey=" + apiKey
    print url

    response = urllib2.urlopen(url)
    data = json.load(response)
    l = data['list']
    story = l['story']
    content = []
    for item in story:
        try:
            C = Content()
            C.title = item['title']
            trans = item['transcript'] ##XML document with story transcript
            ##Since its XML we have to do it by hand here, instead of using the scraper function in utils
            link = trans['link']
            url = link['$text']
            C.url = url
            xmlData = urllib2.urlopen(url)
            tree = ET.parse(xmlData)
            root = tree.getroot()
            rawText = "" ##put the transcript into this string
            for child in root:
                rawText += child.text
            C.text = rawText
            C.numberOfWords = len(rawText.split())
            C.date = day
            content.append(C)
        except KeyError:
            pass
    D.content = content
    D.calculateNumberOfContent()
    D.calculateNumberOfWords()
    return D


def getRange(term, startDate, endDate):
    Out = Output(term, startDate, endDate) ##build output
    endString = dateToRawString(endDate)
    currentString = dateToRawString(startDate) ##running
    currentString = int(currentString)
    endString = int(endString)
    content = []
    while currentString <= endString:
        print currentString, endString
        dayResults = getDay(term, currentString)
        content.append(dayResults)
        currentString = int(getNextDate(currentString)) ##advance the loop
    Out.content = content
    Out.calculateTotalWords()
    Out.calculateTotalDays()
    Out.calculateTotalContent()
    print "Total Content is: ", Out.totalContent
    print "Total Number of Words is: ", Out.totalWords
    print "Number of Days is: ", Out.totalDays
    return Out
