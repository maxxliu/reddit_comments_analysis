# test for running through and grabbing sentiment towards keywords
# that we are interested in (eg. apple, technology, computers)
from mrjob.job import MRJob
import json
import time
import nltk_testing

dates = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
            'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10',
            'Nov': '11', 'Dec': '12'}

class DailySentiment(MRJob):
    def mapper(self, _, line):
        json_v = json.loads(line)
        epoch = json_v['created_utc']
        json_v['time'] = time.strftime("%a %d %b %Y %H:%M:%S", time.localtime(epoch))
        day = json_v['time'][4:6]
        

        # do something
    def combiner(self, key, values):
        # do something
    def reducer(self, key, values):
        # do something

if __name__=='__main__':
    DailySentiment.run()
