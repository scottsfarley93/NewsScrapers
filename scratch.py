from utils import *
import matplotlib.pyplot as plt

#print "Importing..."
#tumblr = importFile("/Users/scottsfarley/documents/Syria_2015-9-1_2015-11-1/tumblr.dat")
#print "Imported.  Parsing..."
#ts = TimeSeriesAnalysis(tumblr)
#ts.dailyCitiesReferences()
#ts.dailyCountryReferences()
#ts.dailySentiment()
#ts.writeToDisk()

# print len(cities)
# ts = importAnalysisFile("/Users/scottsfarley/documents/TimeSeries.dat")
# matrix = getDailySentimentMatrix(ts)
# print matrix
# matrix.plot()
# plt.show()

# tumblr = importFile("/Users/scottsfarley/documents/Syria_2015-9-1_2015-11-1/tumblr.dat")
# agg = AggregateAnalysis(tumblr)
# agg.countryMentions()
# agg.aggregateSentiment()
# agg.cityMentions()
# agg.writeToDisk()
#
# agg = importAnalysisFile("/Users/scottsfarley/documents/AggregateSyria.dat")
# # matrix = getAggregateCountryMentions(agg)
# # matrix.plot(kind='bar')
# # plt.show()
#
# matrix = getAggregateCityMentions(agg)
# print matrix
# matrix.plot(kind='bar')
# plt.show()

npr = importFile("/Users/scottsfarley/documents/Syria_2015-9-1_2015-11-1/guardian.dat")
ts = TimeSeriesAnalysis(npr)
ts.dailySentiment()
ts.dailyCitiesReferences()
ts.dailyCountryReferences()
ts.writeToDisk()
ts = importAnalysisFile("/Users/scottsfarley/documents/TimeSeries.dat")
dailySents = getDailySentimentMatrix(ts)
dailySents.plot()
plt.show()