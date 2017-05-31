from mrjob.job import MRJob
import json
import helper
import re


class ProductSentiment(MRJob):
    '''
    finds sentiment for each of the products we care about
    '''
    def mapper_init(self):
        self.products = set()
        self.stopwords = set()

        txt = open('testing_comps.txt')
        for item in txt:
            p = re.findall(helper.PATTERN, item)
            self.products.update(p)

        stop = open('stopwords.csv')
        for s in stop:
            s = s.strip('\n')
            self.stopwords.add(s)


    def mapper(self, _, line):
        json_v = helper.clean_line(line)

        words = json_v['body']
        words = re.findall(helper.PATTERN, words)
        words = set(words)
        to_use = [x for x in words if x not in self.stopwords]

        for word in to_use:
            if word in self.products:
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
    ProductSentiment.run()
