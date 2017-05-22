# test for running through and grabbing sentiment towards keywords
# that we are interested in (eg. apple, technology, computers)
from mrjob.job import MRJob
import json
import time
import nltk_testing

KEYWORDS = []

class DailySentiment(MRJob):
    def mapper(self, _, line):
        json_v = nltk_testing.clean_line(line)

        for word in KEYWORDS:
            if word in json_v['body']:
                # do the sentiment analysis
                # should return sentiment and word count
                


        # do something
    def combiner(self, key, values):
        # do something
    def reducer(self, key, values):
        # do something

if __name__=='__main__':
    DailySentiment.run()
