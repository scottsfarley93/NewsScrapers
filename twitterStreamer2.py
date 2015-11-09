outfileName = "/Users/scottsfarley/documents/tweets.csv"


print "Starting up..."
try:
    import tweepy
except ImportError:
    import pip
    pip.main(['install', 'tweepy'])

import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
import csv

accessToken = "3609701009-mDbbwgQkNbvumolwMn43cOHBfNE4mun49lEdqeJ"
accessSecret ="Khjzhlfp6pkbeB5urxbWfYfQCIX3BWOKFLMjm9cpQTTZ7"
api_key ="BM3NAGuWx4iMpaYBB29hoyJeH"
api_secret = "lzsHayWBop09eNwuKL7fDLTevN1X6pEqQykicmij4XcToPdWwj"


##Setup write to file
#
import time
f = open(outfileName, 'w')
f.write("TERM: SYRIA\n")
f.write("STARTED: ")
f.write(str(time.time()))
f.write("\n")
csvWriter = csv.writer(f)

##Authorize
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(accessToken, accessSecret)
api = tweepy.API(auth)
print "Authorized."
print "Running..."


class tweetStreamer(StreamListener):
    def on_status(self, status):
        print status

    def on_data(self, data):
        try:
            d = json.loads(data)
            creation = d['created_at']
            id = d['id']
            text = d['text'].encode("UTF-8")
            name = d['user']['name'].encode("UTF_8")
            screen_name = d['user']['screen_name'].encode("UTF-8")
            lang = d['user']['lang']
            #print d['coordinates']
            row = creation, id, name, screen_name, lang, text
            csvWriter.writerow(row)
        except:
            pass
        return True


    def on_error(self, status_code):
        print status_code
        return True

    def on_timeout(self):
        print "Timeout..."
        return True


streamer = Stream(auth, tweetStreamer())
streamer.new_session()
streamer.filter(track=["Syria"])
