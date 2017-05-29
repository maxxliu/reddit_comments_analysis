from mrjob.job import MRJob
import json
import helper
import nltk.tokenize

PRODUCTS = ['Charlie', 'David', 'testing', 'business', 'school', 'plus', 'hello'
'why', 'weird', 'working', 'faster', 'microsoft', 'more', 'words']

def test():
    PRODUCTS.append('computer')
    PRODUCTS.append('iPod')
    PRODUCTS.append('Jonathan')
    PRODUCTS.append('Spencer')
    PRODUCTS.append('Max')
    PRODUCTS.append('test')
    PRODUCTS.append('school')
    PRODUCTS.append('study')
    PRODUCTS.append('Apple')
    useless = ['notgonnamatch'] * 100
    PRODUCTS.extend(useless)


class ProductSentiment(MRJob):
    def mapper(self, _, line):
        json_v = helper.clean_line(line)

        words = json_v['body']
        words = set([x.strip(",.'!?/:;-_#$[]()%*") for x in words.split(' ')])
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
        average_sentiment = final_sentiment / final_count

        yield key, (average_sentiment, final_count, final_sentiment)


if __name__=='__main__':
    test()
    ProductSentiment.run()
