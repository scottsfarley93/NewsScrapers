from utils import *

print "Importing..."
tumblr = importFile("/Users/scottsfarley/documents/Syria_2015-9-1_2015-11-1/tumblr.dat")
print "Imported.  Parsing..."
agg = AggregateAnalysis(tumblr)
print "Parsed.  Analyzing..."
c = agg.countryMentions()
print c
b = agg.cityMentions()
print b
sent = agg.aggregateSentiment()
print sent
