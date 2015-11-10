##Do the analyses and save resulting csv files to disk for later analysis
from utils import *
def doTSAnalysisAndSave(directory="/Users/scottsfarley/documents/Syria_2015-9-1_2015-11-1", guardian=True, npr=True, nyt=True, tumblr=True):
    """Do the requested time series analyses and save them to the disk"""
    timeSeriesDirectory = "/Users/scottsfarley/documents/analysis/timeseries/"
    if guardian:
        print "Doing Guardian..."
        g = importFile(directory + "/guardian.dat")
        gTS = TimeSeriesAnalysis(g)
        gTS.dailyCitiesReferences()
        gTS.dailyCountryReferences()
        gTS.dailySentiment()
        ##save and reload so everything works and we have a backup for later
        gTS.writeToDisk(timeSeriesDirectory + "/guardian.dat")
        ts = importAnalysisFile(timeSeriesDirectory + "/guardian.dat")
        g_dailySentiments = getDailySentimentMatrix(ts)
        g_dailySentiments.to_csv(timeSeriesDirectory + "/Guardian_Sentiment_TS.csv")
        g_dailyCountries = getDailyCountryOccurrenceMatrix(ts)
        g_dailyCountries.to_csv(timeSeriesDirectory + "/Guardian_Countries_TS.csv")
        g_dailyCities = getDailyCityOccurrenceMatrix(ts)
        g_dailyCities.to_csv(timeSeriesDirectory + "/Guardian_Cities_TS.csv")
        print "Guardian Finished."
    if npr:
        print "Doing NPR..."
        n = importFile(directory +"/npr.dat")
        nTS = TimeSeriesAnalysis(n)
        nTS.dailyCitiesReferences()
        nTS.dailySentiment()
        nTS.dailyCountryReferences()
        nTS.writeToDisk(timeSeriesDirectory + "/npr.dat")
        ts = importAnalysisFile(timeSeriesDirectory + "/npr.dat")
        n_dailySentiments = getDailySentimentMatrix(ts)
        n_dailySentiments.to_csv(timeSeriesDirectory + "/NPR_Sentiment_TS.csv")
        n_dailyCities = getDailyCityOccurrenceMatrix(ts)
        n_dailyCities.to_csv(timeSeriesDirectory + "/NPR_Cities_TS.csv")
        n_dailyCountries = getDailyCountryOccurrenceMatrix(ts)
        n_dailyCountries.to_csv(timeSeriesDirectory + "/NPR_Countries_TS.csv")
        print "NPR Finished..."
    if nyt:
        print "Doing New York Times..."
        n = importFile(directory +"/nyt.dat")
        nTS = TimeSeriesAnalysis(n)
        nTS.dailyCitiesReferences()
        nTS.dailySentiment()
        nTS.dailyCountryReferences()
        nTS.writeToDisk(timeSeriesDirectory + "/nyt.dat")
        ts = importAnalysisFile(timeSeriesDirectory + "/nyt.dat")
        n_dailySentiments = getDailySentimentMatrix(ts)
        n_dailySentiments.to_csv(timeSeriesDirectory + "/NYT_Sentiment_TS.csv")
        n_dailyCities = getDailyCityOccurrenceMatrix(ts)
        n_dailyCities.to_csv(timeSeriesDirectory + "/NYT_Cities_TS.csv")
        n_dailyCountries = getDailyCountryOccurrenceMatrix(ts)
        n_dailyCountries.to_csv(timeSeriesDirectory + "/NYT_Countries_TS.csv")
        print "New York Times Done..."
    if tumblr:
        print "Doing Tumblr..."
        n = importFile(directory +"/tumblr.dat")
        nTS = TimeSeriesAnalysis(n)
        nTS.dailyCitiesReferences()
        nTS.dailySentiment()
        nTS.dailyCountryReferences()
        nTS.writeToDisk(timeSeriesDirectory + "/tumblr.dat")
        ts = importAnalysisFile(timeSeriesDirectory + "/tumblr.dat")
        n_dailySentiments = getDailySentimentMatrix(ts)
        n_dailySentiments.to_csv(timeSeriesDirectory + "/tumblr_Sentiment_TS.csv")
        n_dailyCities = getDailyCityOccurrenceMatrix(ts)
        n_dailyCities.to_csv(timeSeriesDirectory + "/tumblr_Cities_TS.csv")
        n_dailyCountries = getDailyCountryOccurrenceMatrix(ts)
        n_dailyCountries.to_csv(timeSeriesDirectory + "/tumblr_Countries_TS.csv")
        print "Tumblr Done."

doTSAnalysisAndSave(nyt=False)



