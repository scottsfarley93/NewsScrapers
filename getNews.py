__author__ = 'scottsfarley'
###Get raw-text content using a keyword and a date range
###Save to a json file
###Sources:
    ##1.  New York Times
    ##2.  Tumblr
    ##3. NPR story transcriptions
    ##4.  The Guardian (UK)
##Write to a new folder




import datetime
runStart = datetime.datetime.now()
print "New Scraper Process Started at: ", str(runStart)
print "Starting up..."
from utils import *
import NPR
import Guardian
import Tumblr
import NYT
import os
docsFolder = os.environ['HOME'] + "/documents"

####RUN SETTINGS
key = "Syria"
startDate = (2015, 9, 1) ##Sept 1, 2015
endDate = (2015, 11, 1) ##through Nov 1, 2015

startString = dateToURLString(startDate)
endString = dateToURLString(endDate)

##make a new folder that is easy to identify in the docs directory
folderName = key + "_" + startString + "_" + endString

defaultDir = docsFolder + "/" + folderName
saveDest = defaultDir + "/"

if not os.path.exists(defaultDir):
    os.mkdir(defaultDir)


print "Running!"
print "\tGathering content from NPR..."
#npr = NPR.getRange(key, startDate, endDate)
#writeOutputToFile(npr, saveDest + "NPR.dat")
print "\tFinished NPR"
print "\tGathering content from New York Times..."
#nyt = NYT.getRange(key, startDate, endDate)
#writeOutputToFile(nyt, saveDest + "NYT.dat")
print "\tFinished NYT"
print "\tGathering content from Guardian UK..."
#guardian = Guardian.getRange(key, startDate, endDate)
#writeOutputToFile(guardian, saveDest + "guardian.dat")
print "\tFinished Guardian UK"
print "\tGathering content from Tumblr"
tumblr = Tumblr.getRange(key, startDate, endDate)
writeOutputToFile(tumblr, saveDest + "tumblr.dat")
print "\tFinished Tumblr."
print "Analysis Finished!"
exit()
