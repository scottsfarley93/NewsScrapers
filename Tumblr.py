__author__ = 'scottsfarley'

from utils import *
from Config import Tumblr
import urllib2
import json
import datetime


def getDay(term, day):
    D = Day(day)
    ##Find all tumblr posts between the 12am and 11:59 pm of a day
    startTime = timeFromDateString(day)
    nextDay = getNextDate(day)
    endTime = timeFromDateString(nextDay)
    #D = Day(day)
    apiKey = Tumblr.apiKey.strip()
    endpoint = "http://api.tumblr.com/v2/tagged"
    url = endpoint + "?tag=" + term
    url += "&api_key=" + apiKey + "&filter=text"
    runningTime = endTime
    content = []
    while runningTime >= startTime:
        apiCall = url + "&before=" + str(runningTime) ##separate so we don't keep adding to the url
        print apiCall
        response = urllib2.urlopen(apiCall)
        data = json.load(response)
        r = data['response']
        timestamps = []
        for blog in r:
            C = Content()
            timestamp = blog['timestamp']
            if timestamp >= startTime: ##only add if it is in this day
                timestamps.append(int(timestamp))
                if 'body' in blog.keys():
                    text = blog['body']
                    C.text = text
                    C.url = blog['short_url']
                    C.title = blog['title']
                    print C.title
                    C.other = blog['blog_name']
                    C.date = datetime.datetime.fromtimestamp(timestamp)
                    C.numberOfWords = len(text.split())
                    content.append(C)
        try:
            timestamp =  min(timestamps)
            runningTime = timestamp
        except:
            break
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
