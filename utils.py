from bs4 import BeautifulSoup as BS
import requests



##Output, Content and Entity classes to be used across apis
##Build these classes and then convert them to json for output
class Output():
    """This is the highest class in the output structure, and contains both the summary of the run (terms and time periods)
    and the content returned by the run"""
    def __init__(self, searchTerm, startTuple, endTuple):
        self.searchTerm = searchTerm
        self.startDate = startTuple
        self.endDate = endTuple
        self.totalDays = 0
        self.totalContent = 0
        self.totalWords = 0
        self.content = []
    def calculateTotalContent(self):
        s = 0
        for i in self.content:
            s += i.numberOfContent
        self.totalContent = s

    def calculateTotalWords(self):
        s = 0
        for i in self.content:
            i.calculatNumberOfWords()
            s += i.numberOfWords
        self.totalWords = s

    def calculateTotalDays(self):
        self.totalDays = len(self.content)


class Day():
    """This is the class for holding pieces of content within the output.
    Each instance represents a different day of the analysis"""
    def __init__(self, date):
        self.date = date
        self.numberOfWords = 0
        self.numberOfContent = 0
        self.content = []

    def calculateNumberOfContent(self):
        self.numberOfContent = len(self.content)

    def calculateNumberOfWords(self):
        s = 0
        for i in self.content:
            s += i.numberOfWords
        self.numberOfWords = s

class Content():
    """This holds each piece of content in its own instance, so we keep metadata about the individual piece"""
    ##bottom class in hierarchy
    def __init__(self):
        self.date = ""
        self.numberOfWords = 0
        self.title = ""
        self.URL = ""
        self.text = ""
        self.author = ""
        self.location = ""
        self.other = ""



##Utility functions to be used across APIs

def dateToURLString(dateTuple):
    ##yyyy-mm-dd
    year = dateTuple[0]
    month = dateTuple[1]
    day = dateTuple[2]
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        assert(year <= 2017)
        assert(year > 1900)
        assert(month < 13)
        assert(month > 0)
        assert(day > 0)
        assert(day < 32)
        return str(year) + "-" + str(month) + "-" + str(day)
    except:
        return False

def dateToRawString(dateTuple):
    ##yyyymmdd
    year = dateTuple[0]
    month = dateTuple[1]
    day = dateTuple[2]
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        assert(year <= 2017)
        assert(year > 1900)
        assert(month < 13)
        assert(month > 0)
        assert(day > 0)
        assert(day < 32)
        if month < 10:
            monthStr = "0" + str(month)
        else:
            monthStr = str(month)

        if day<10:
            dayString = "0" + str(day)
        else:
            dayString = str(day)
        return str(year) + monthStr + dayString
    except:
        return False

def rawDatestringToURLdateString(dateString):
    ##yyyymmdd --> yyyy-mm-dd
    dateString = str(dateString)
    year = dateString[0:4]
    month = dateString[4:6]
    day = dateString[6:8]
    r = year + "-" + month + "-" + day
    return r

def URLDateStringToRawDateString(urlDate):
    ##yyyy-mm-dd to yyyymmdd
    return urlDate.replace("-", "")

def timeFromDateString(dateString):
    """Return unix time from a datestring (12am)"""
    import datetime
    import time
    dateString = str(dateString)
    year = int(dateString[0:4])
    month = int(dateString[4:6])
    day = int(dateString[6:8])
    dt = datetime.datetime(year, month, day)
    t = time.mktime(dt.timetuple())
    return t

def getHTMlBodyText(url, tag):
    """Get the body text of a url webpage with the given tag.  Returns a string of the text"""
    r = requests.get(url)
    data = r.text
    soup = BS(data)
    body = soup.html.body
    title = soup.html.head.title.text
    title = title.replace("| The Guardian", "")
    story = soup.select(tag)
    article_text = ""
    i = 0
    while i < len(story) - 2:
        ##Story might be split into multiple html elements
        s = story[i].string ##gives the value inside of the tagged element
        try:
            value = "".join([x if ord(x) < 128 else '?' for x in s])
            value = value.replace("?", " ")
            if value != "Go to Home Page": ##This is the text if the article is no longer online at nyt.com
                article_text += value + " "
        except:
            pass
        i += 1
    return [title, article_text]


def getNextDate(dateString):
    """Returns the string of the next day in the calendar --> deals with month and year changes"""
    dateString = str(dateString)
    year = dateString[0:4]
    month = dateString[4:6]
    day = dateString[6:8]

    daysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]##doesnt deal with leap years
    monthNumber = int(month)
    dayNumber = int(day)
    yearNumber = int(year)
    daysInThisMonth = daysInMonths[monthNumber - 1] ##correct for index
    ##year changes
    if monthNumber == 12 and dayNumber >= 31:
        yearNumber += 1
        monthNumber = 1
        dayNumber = 1
    else:
        ##month changes
        if dayNumber >= daysInThisMonth:
            monthNumber += 1
            dayNumber = 1
        else:
            dayNumber +=1
    yearString = str(yearNumber)
    ##format with zeros
    if monthNumber < 10:
        monthString = "0" + str(monthNumber)
    else:
        monthString = str(monthNumber)
    if dayNumber < 10:
        dayString = "0" + str(dayNumber)
    else:
        dayString = str(dayNumber)
    return yearString + monthString + dayString


def writeOutputToFile(output, filename):
    """Accepts an Output object and writes it out to the specified filename"""
    import pickle
    f = open(filename, 'w')
    pickle.dump(output, f)
    f.close()

def importFile(filename):
    import pickle
    f = open(filename, 'r')
    a = pickle.load(f)
    f.close()
    return a