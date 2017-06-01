from mrjob.job import MRJob
import json
import re
import time
import datetime
from textblob import TextBlob

'''
this mapreduce DOES NOT require the helper.py file
this mapreduce takes in UNPROCESSED file
'''

class ProductSentiment(MRJob):
    '''
    finds sentiment for each of the products we care about
    '''
    def mapper_init(self):
        self.products = set()
        self.stopwords = set()
        self.pattern = '[a-zA-Z]+'
        self.dates = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
                    'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10',
                    'Nov': '11', 'Dec': '12'}

        txt = open('testing_comps.txt')
        for item in txt:
            p = re.findall(self.pattern, item)
            self.products.update(p)

        stop = open('stopwords.csv')
        for s in stop:
            s = s.strip('\n')
            self.stopwords.add(s)


    def mapper(self, _, line):
        json_v = json.loads(line)
        epoch = json_v['created_utc']
        json_v['time'] = time.strftime("%a %d %b %Y %H:%M:%S", time.localtime(epoch))
        # day of the week, day, month, year, time
        day = json_v['time'][4:6]
        month = json_v['time'][7:10]
        year = json_v['time'][11:15]
        n_mnth = self.dates[month]
        week_num = datetime.date(int(year), int(n_mnth), int(day)).isocalendar()[1]
        json_v['week'] = str(week_num)
        json_v['month'] = n_mnth
        json_v['year'] = year
        comment = json_v['body']
        comment = comment.replace('\n', '')
        comment = comment.replace('\r', '')
        comment = comment.replace('%', '')
        comment = comment.replace('*', '')
        comment = comment.replace('gt', '')

        words = re.findall(self.pattern, comment)
        words = set(words)
        to_use = [x for x in words if x not in self.stopwords]

        for word in to_use:
            if word in self.products:
                mentions = 0
                total_sentiment = 0
                blob = TextBlob(comment)

                for sentence in blob.sentences:
                    if word in sentence:
                        mentions += 1
                        analysis = sentence.sentiment.polarity
                        total_sentiment += analysis

                score = (mentions, total_sentiment)

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
