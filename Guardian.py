__author__ = 'scottsfarley'


from utils import *
from Config import Guardian
import json
import urllib2
import pprint

def getDay(searchTerm, date):
    ##Date is datestring yyyymmdd
    ##Start building the output
    D = Day(date)

    apiKey = Guardian.apiKey ##Only api key is needed for this api --> stored in config module
    ##build the api search query
    endpoint = "http://content.guardianapis.com/search?"

    url = endpoint + "api-key=" + apiKey
    ##url encode the search term
    searchTerm = searchTerm.replace(" ", "%20")
    url += "&q="  + searchTerm
    url += "&"

    ##from date and to date
    url += "from-date=" + rawDatestringToURLdateString(date)
    url += "&"
    url += "to-date=" + rawDatestringToURLdateString(date)

    ##sort by newest --> seems to make more sense than by relevance since we want them all anyways
    url += "&"
    url += "order-by=newest"
    response = urllib2.urlopen(url)
    data = json.load(response)
    totalResults = data['response']['total']
    numPages = data['response']['pages']
    ##iterate through the pages in the response
    content = [] ##store all the content here for later
    currentPage = 1 ##1 indexed
    while currentPage <= numPages:
        ##build a new api call with the same params, but passing in the pages argument
        url += "&page" + str(currentPage)
        response = urllib2.urlopen(url)
        data = json.load(response)
        results = data['response']['results']
        ##iterate through results on page
        j = 0
        while j < len(results):
            ##Make a new Content instance
            C = Content()
            item = results[j]
            C.title = item['webTitle']
            C.url = item['webUrl']
            htmlResults = getHTMlBodyText(C.url, 'p')
            C.text = htmlResults[1]
            C.title = htmlResults[0]
            C.numberOfWords = len(C.text.split())
            content.append(C)
            j +=1
        currentPage += 1
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




a = getRange("Syria", (2015, 10, 1), (2015, 10, 24))
writeOutputToFile(a, "/Users/scottsfarley/documents/Syria_Guardian_20151001-20151024.dat")






