class Configuration():
    def __init__(self, apiKey = "", apiSecret="", consumerSecret="", consumerKey=""):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.consumerSecret = consumerSecret
        self.consumerKey = consumerKey


Twitter = Configuration(apiKey="", apiSecret="",
                         consumerKey="", consumerSecret="")


Guardian = Configuration(apiKey="")
NPR = Configuration(apiKey="")
Tumblr = Configuration(apiKey="", apiSecret="")
NYT = Configuration(apiKey="")


