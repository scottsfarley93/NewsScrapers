__author__ = 'scottsfarley'


"""Purpose: Download text with a keyword to a json file
Input: Keyword
        StartDate
        EndDate

Output: JSON File
        {
            summary:
                number of content  (articles, tweets, etc)
                number of words
                start date
                end date
                number of days of coverage
            content:
                day
                    date
                    number of words
                    number of content
                    entity
                        date
                        number of words
                        raw text
                        title (if applicable)
                        author (if applicable)
                        other ?
"""




import NYT
import Twitter
import NPR
import Guardian
import Tumblr


NYT.test()
Twitter.test()
NPR.test()
Guardian.test()
Tumblr.test()
