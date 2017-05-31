from mrjob.job import MRJob
import json
import helper
import nltk.tokenize
import re


PRODUCTS = set()


def add_products(txt_file):
    '''
    txt_file - this is the file with the results of the first mapreduce,
                it has a list of 100 companies and their top 5 most mentions
    '''
    txt = open(txt_file)
    for item in txt:
        p = re.findall(helper.PATTERN, item)
        PRODUCTS.update(p)


class ProductSentiment(MRJob):
    def mapper(self, _, line):
        json_v = helper.clean_line(line)

        words = json_v['body']
        words = re.findall(helper.PATTERN, words)
        # words = set([x.strip(",.'!?/:;-_#$[]()%*") for x in words.split(' ')])
        words = set(words)
        to_use = [x for x in words if x not in helper.STOPWORDS]

        for word in to_use:
            if word in PRODUCTS:
                score = helper.product_sentiment(word, json_v['body'])
                # score = (mentions, total_sentiment)

                key1 = word + json_v['week'] + 'w'
                key2 = word + json_v['month'] + 'm'

                yield key1, score
                yield key2, score


    def combiner(self, key, values):
        count_total = 0
        sentiment_total = 0
        for value in values:
            count_total += value[0]
            sentiment_total += value[1]

        yield key, (count_total, sentiment_total)


    def reducer(self, key, values):
        final_count = 0
        final_sentiment = 0
        for value in values:
            final_count += value[0]
            final_sentiment += value[1]

        yield key, (final_count, final_sentiment)


if __name__=='__main__':
    add_products('../data_analysis/testing_comps.txt')
    ProductSentiment.run()
