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
            i.calculateNumberOfWords()
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

def loadCitieslist():
    import urllib2
    import json
    data = urllib2.urlopen("https://raw.githubusercontent.com/mahemoff/geodata/master/cities_with_countries.txt")
    d = json.load(data)
    cities = []
    countries = []
    for i in d:
        cities.append(i['city'].upper())
        countries.append(i['country'])

    return cities

cities = loadCitieslist()

def loadCountriesList():
    import urllib2
    import json
    data = urllib2.urlopen("http://restcountries.eu/rest/v1/all")
    d = json.load(data)
    countries = ["STATES"] ##catch united states via this hack
    for i in d:
        countries.append(i['name'].upper())
    return countries
countries = loadCountriesList()

###News Analysis Tools
class TimeSeriesAnalysis():
    def __init__(self, newsObj):
        ##Loads a news object
        self.raw = newsObj
        self.sentiments = []
        self.cityCounts = {}
        self.countryCounts = {}
    def dailySentiment(self, normalize = False):
        print "Analyzing daily sentiment."
        from textblob import TextBlob
        sentiments = {}
        for day in self.raw.content:
            ##Aggregate this day's text
            allText = ""
            for article in day.content:
                articleText= article.text
                allText += articleText
            blob = TextBlob(allText)
            sentiments[day.date] = blob.sentiment
        self.sentiments = sentiments
        return sentiments

    def dailyCitiesReferences(self):
        print "Finding daily city references..."
        from textblob import TextBlob
        days = {}
        for day in self.raw.content:
            allText = ""
            for article in day.content:
                articleText = article.text
                allText += articleText
            blob = TextBlob(allText)
            words = blob.words
            cityCounts = {}
            for word in words:
                if word.upper() in cities:
                   print word.upper()
                   if word.upper() not in cityCounts.keys():
                       cityCounts[word.upper()] = 1
                   else:
                       cityCounts[word.upper()] +=1
            days[day.date] = cityCounts
        self.cityCounts = days
        return days

    def dailyCountryReferences(self):
        print "Finding daily country references..."
        from textblob import TextBlob
        days = {}
        for day in self.raw.content:
            allText = ""
            for article in day.content:
                articleText = article.text
                allText += articleText
            blob = TextBlob(allText)
            words = blob.words
            countryCounts = {}
            for word in words:
                if word.upper() in countries:
                   if word.upper() not in countryCounts.keys():
                       countryCounts[word.upper()] = 1
                   else:
                       countryCounts[word.upper()] +=1
            days[day.date] = countryCounts
        self.countryCounts = days
        return days

    def writeToDisk(self, filename="default"):
        print "Writing to disk."
        import json
        if filename == 'default':
            import os
            docsFolder = os.environ['HOME'] + "/documents"
            filename = docsFolder + "/TimeSeries.dat"
        output = {"CityCounts" : self.cityCounts, "Sentiments" : self.sentiments, "CountryCounts" : self.countryCounts}
        out = json.dumps(output)
        f = open(filename, 'w')
        f.write(out)
        f.close()




class AggregateAnalysis():
    def __init__(self, rawObj):
        self.raw = rawObj
        self.allText= ""
        ##aggregate all text
        for day in self.raw.content:
            for article in day.content:
                articleText = article.text
                self.allText += articleText
        self.cityCounts = []
        self.countryCounts = []
        self.sentiment = (0,0)
        self.keyword = self.raw.searchTerm
        self.startDate = self.raw.startDate
        self.endDate = self.raw.endDate
    def countryMentions(self):
        from collections import Counter
        from textblob import TextBlob
        mentions = []
        print "Finding country mentions..."
        blob = TextBlob(self.allText)
        for word in blob.words:
            if word.upper() in countries:
                mentions.append(word.upper())
        c = Counter(mentions)
        self.countryCount = c
        return c
    def cityMentions(self):
        from collections import Counter
        from textblob import TextBlob
        mentions = []
        print "Finding city mentions..."
        blob = TextBlob(self.allText)
        for word in blob.words:
            if word.upper() in cities:
                mentions.append(word.upper())
        c = Counter(mentions)
        self.cityCount = c
        return c
    def aggregateSentiment(self):
        print "Analyzing sentiment"
        from textblob import TextBlob
        blob = TextBlob(self.allText)
        self.sentiment = blob.sentiment
        return blob.sentiment

    def writeToDisk(self, filename='defualt'):
        print "Saving to disk."
        if filename == ' default':
            import os
            docsFolder = os.environ['HOME'] + "/documents"
            filename = docsFolder + "/Aggregate.dat"
        import json
        output = {'CityCounts' : self.cityCount, 'CountryCounts' : self.countryCount, 'Sentiments' : self.sentiment}
        out = json.dumps(output)
        f = open(filename, 'w')
        f.write(out)
        f.close()


#####ANALYSIS UTILITIES

##For timeseries

def getCitySet(TSObj):
    """Return a list of unique cities mentioned in the time series analysis object"""
    cityCounts = TSObj['CityCounts']
    citySet = []
    for day in cityCounts:
        for city in cityCounts[day]:
            citySet.append(city)
    return set(citySet)

def getCountrySet(TSObj):
    """Return a list of unique countries mentioned in the time series analysis"""
    print TSObj.keys()
    countryCounts = TSObj['CountryCounts']
    countrySet = []
    for day in countryCounts:
        for country in countryCounts[day]:
            countrySet.append(country)
    return set(countrySet)



def getDailyCityOccurrenceMatrix(tsobject):
    """Returns a pandas dataframe of daily occurrences of mentions of cities over the period of the analysis"""
    import pandas as pd
    theMatrix = []
    header = ['Date']
    header += getCitySet(tsobject) ##unique cities within the object
    theMatrix.append(header)
    dates = ["Date"]
    for day in tsobject['CityCounts']:
        date = pd.to_datetime(day)
        dates.append(date)
        blankRow = [date]
        key = day
        dayData = tsobject['CityCounts'][day]
        for city in header:
            if city in dayData.keys():
                blankRow.append(dayData[city])
            else:
                blankRow.append(0)
        theMatrix.append(blankRow)
    theMatrix = pd.DataFrame(theMatrix, index = dates)
    theMatrix.columns = header + ["NaN"]
    theMatrix = theMatrix.ix[1:]
    return theMatrix

def getDailyCountryOccurrenceMatrix(tsobject):
    """Returns a pandas dataframe of daily occurrences of all of the countries mentioned over the period of the analysis"""
    import pandas as pd
    theMatrix = []
    header = ['Date']
    header += getCountrySet(tsobject) ##all countries
    theMatrix.append(header)
    dates = ['Date']
    for day in tsobject['CountryCounts']:
        date = pd.to_datetime(day)
        dates.append(date)
        blankRow = [date]
        dayData = tsobject['CountryCounts'][day]
        for country in header:
            if country in dayData.keys(): ##if it is in the day's mentioned
                blankRow.append(dayData[country]) ##add that number to the day's row in the dataframe
            else:
                blankRow.append(0) ##otherwise there were no mentions
        theMatrix.append(blankRow)
    theMatrix = pd.DataFrame(theMatrix, index = dates)
     ##fix header info
    theMatrix.columns = header+ ["NaN"]
    theMatrix = theMatrix.ix[1:]
    return theMatrix

def getDailySentimentMatrix(tsobject):
    import pandas as pd
    theMatrix = []
    header = ["Date", "Polarity", "Subjectivity"]
    dates = []
    for day in tsobject['Sentiments']:
        date = pd.to_datetime(day)
        dates.append(date)
        blankRow = [date]
        dayData = tsobject["Sentiments"][day]
        polarity = dayData[0]
        subjectivity = dayData[1]
        blankRow.append(polarity)
        blankRow.append(subjectivity)
        theMatrix.append(blankRow)
    theMatrix = pd.DataFrame(theMatrix, index = dates, columns=header)
    return theMatrix


##For aggregate

def getAggregateCountryMentions(aggobject):
    """Returns 1-column pandas dataframe of country mention occurrences aggregated over analysis period"""
    import pandas as pd
    theMatrix = []
    header = ["Count"]
    countries = []
    countryCounts = aggobject['CountryCounts']
    for country in countryCounts:
        row = []
        count = countryCounts[country]
        countries.append(country)
        row.append(count)
        theMatrix.append(row)
    theMatrix = pd.DataFrame(theMatrix, columns = header, index=countries)
    return theMatrix


def getAggregateSentiment(aggobject):
    """Return the sentiment analysis aggregated over the whole analysis period.
        Return as tuple (polarity, subjectivity)"""
    print aggobject['Sentiments']


def getAggregateCityMentions(aggobject):
    """Returns a 1-column pandas dataframe with the city frequencies aggregated over the whole analysis period"""
    import pandas as pd
    theMatrix = []
    header = ["Count"]
    cityList = []
    cityCounts = aggobject['CityCounts']
    for city in cityCounts:
        row = []
        count = cityCounts[city]
        cityList.append(city)
        row.append(count)
        theMatrix.append(row)
    theMatrix = pd.DataFrame(theMatrix, columns=header, index=cityList)
    return theMatrix



def importAnalysisFile(filename):
    """Brings a json analysis file into memory"""
    import json
    import pandas as pd
    f = open(filename, 'r')
    data = json.load(f)
    return data

