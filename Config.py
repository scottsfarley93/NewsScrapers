class Configuration():
    def __init__(self, apiKey = "", apiSecret="", consumerSecret="", consumerKey=""):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.consumerSecret = consumerSecret
        self.consumerKey = consumerKey
    def loadFromFile(self, filename):
        f = open(filename, 'r')
        self.apiKey = ""
        self.apiSecret = ""
        self.consumerKey = ""
        self.consumerSecret = ""
        i = 0
        for row in f:
            if i == 0:
                self.apiKey = row
            if i == 1:
                self.apiSecret = row
            if i == 2:
                self.consumerSecret = row
            if i == 3:
                self.consumerKey = row
            i +=1

Twitter = Configuration()
Twitter.loadFromFile("keys/twitterKeys.txt")
Guardian = Configuration()
Guardian.loadFromFile("keys/guardianKey.txt")
NPR = Configuration()
NPR.loadFromFile("keys/NPRKey.txt")
Tumblr = Configuration()
Tumblr.loadFromFile("keys/TumblrKeys.txt")
NYT = Configuration()
NYT.loadFromFile("keys/NYTKey.txt")
print "Loaded all API Keys from Keystore"


