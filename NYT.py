__author__ = 'scottsfarley'

from utils import *
import Config
import urllib2
import json


def getDay(term, day):
    D = Day(day)
    endpoint = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
    term = term.replace(" ", "%20")
    url = endpoint + "?fq=" + term
    url += "&begin_date=" + str(day) + "&end_date=" + str(day)
    apiKey = Config.NYT.apiKey
    url += "&api-key=" + apiKey
    print url
    content = []
    response = urllib2.urlopen(url)
    data = json.load(response)['response']
    meta = data['meta']
    numHits = meta['hits']
    numPages = numHits / 10
    page = 0
    while page < numPages:
        url = endpoint + "?fq=" + term + "&begin_date=" + str(day) + "&end_date=" + str(day) + "&api-key=" + apiKey + "&page=" + str(page)
        response = urllib2.urlopen(url)
        data = json.load(response)
        articles = data['response']['docs']
        for item in articles:
            web_url = item['web_url']
            t = item['type_of_material']
            doctype = item['document_type']
            source = item['source']
            body = getHTMlBodyText(web_url, 'p')
            print body
            C = Content()
            C.title = item['headline']['main']
            C.text = body[0]
            C.source = source
            C.url = web_url
            C.numberOfWords = len(body[0].split())
            content.append(C)
        page += 1
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