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
                key = word + json_v['suffix']
                yield key, values # (sentiment, word_count)


    def combiner(self, key, values):
        sent_count = 0 # number of values
        sent_total = 0 # aggregate of sentiment scores
        word_count = 0 # number of words
        for value in values:
            sent_count += 1
            sent_total += values[0]
            word_count += values[1]

        yield key, (sent_count, sent_total, word_count)


    def reducer(self, key, values):
        sent_count = 0
        sent_total = 0
        word_count = 0
        for value in values:
            sent_count += values[0]
            sent_total += values[1]
            word_count += values[2]
        sent_avg = sent_total / sent_count

        yield key, (sent_avg, sent_total, word_count)

if __name__=='__main__':
    DailySentiment.run()
