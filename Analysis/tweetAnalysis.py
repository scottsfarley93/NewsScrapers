__author__ = 'scottsfarley'




def readTweets():
    import csv
    from textblob import TextBlob
    negWords = loadNegativeWords()
    posWords = loadPositiveWords()
    tweetfile = "/Users/scottsfarley/downloads/tweetsOut2.csv"
    f = open(tweetfile, 'r')
    dates = []
    users = []
    lang = []
    text = []
    totalChars = 0
    totalTweets = 0
    hashtags = []
    retweets = 0
    csvreader = csv.reader(f)
    j = 0
    for tweet in csvreader:
        if  j < 10:
            try:
                if len(tweet) == 1: ##get rid of header
                    continue
                #dates.append(tweet[0]) ##created_at
                #users.append(tweet[2]) ##real user name
                #lang.append(tweet[4]) ##language
                #text.append(tweet[5]) ##tweet text
                totalTweets +=1
                tweetText = tweet[5]
                totalChars  += len(tweetText)
                t = TextBlob(tweetText)
                if t[0:2] == "RT":
                    retweets +=1
                tweetScore = 0
                for word in t.words:
                    if word in negWords:
                        print "NEGATIVE"
                        tweetScore -= 1
                    elif word in posWords:
                        print "POSITIVE"
                        tweetScore +=1
                print tweetScore
            except UnicodeDecodeError:
                print "Failed to decode unicode for tweet: ", j
        else:
            break
        j +=1

    f.close()


    print "Total Characters: ", totalChars
    print "Total Tweets: ", totalTweets
    print "Retweets: ", retweets

def loadPositiveWords():
    import urllib2
    positiveWords = []
    f = urllib2.urlopen("http://www.idiap.ch/~apbelis/hlt-course/positive-words.txt")
    count = 0
    for i in f:
        if i[0] == ";":
            continue
        word = i.rstrip("\n")
        positiveWords.append(word)
        count +=1
    print "Total number of positive words: ", count
    return positiveWords



def loadNegativeWords():
    import urllib2
    f = urllib2.urlopen("http://www.idiap.ch/~apbelis/hlt-course/negative-words.txt")
    negativeWords = []
    count = 0
    for i in f:
        if i[0] ==";":
            continue
        word  = i.rstrip("\n")
        negativeWords.append(word)
        count +=1
    print "Total number of negative words: ", count
    return negativeWords


def loadCities():
    import urllib2
    import json
    f = urllib2.urlopen("https://raw.githubusercontent.com/David-Haim/CountriesToCitiesJSON/master/countriesToCities.json")
    data = json.load(f)
    print data

#loadCities()

#readTweets()

def process():
    with open("/Users/scottsfarley/downloads/tweetsOut2.csv", 'r') as r:
        with open("/Users/scottsfarley/documents/tweets1.csv", 'w') as w:
            r.next()
            r.next()
            for line in r:
                w.write(line)
    r.close()
    w.close()
#process()

def loadIntoPandas():
    import pandas as pd
    import collections
    from matplotlib import pyplot as plt
    import numpy

    f = pd.read_csv("/Users/scottsfarley/documents/tweets1.csv")
    f.columns = ['Date', 'tweetID', 'User_Name', "Screen_Name", "Language", "Text"]
    f['Date'] = pd.to_datetime(f['Date'])
    f.index = f['Date']
    langs = f['Language']
    c = collections.Counter(langs)
    #print c
    rs = f.resample('T', how=['count'])
    rs.plot(kind='line')
    plt.show()

loadIntoPandas()