from mrjob.job import MRJob
import re
import json
import tb_sentiment

class sent_count(MRJob):
    '''
    yields 3 lists of commenters: 
    1. Commenters with highest upvote counts
    2. Commenters that are the meanest
    3. Commenters that are the nicest
    '''


    def mapper(self, _, line):
        j = json.loads(line)
        up = j['ups']
        author = j['author']
        body = j['body']
        body = body.replace("\r\n", " ")
        body = body.replace("\n", " ")
        body = body.replace("\r", " ")
        sentiment = tb_sentiment.dumb_analysis(body) #do some sentiment analysis right here
        yield author, (up, sentiment, 1)   

    def combiner(self, author, type_tuple):
        up = 0
        sentiment = 0
        author_count = 0
        for tup in type_tuple:
            up += tup[0]
            sentiment += tup[1]
            author_count += tup[2]
        yield author, (up, sentiment, author_count)

    def reducer_init(self):
        self.up_values = [0] * 10
        self.up_people = [None] * 10
        self.gsent_values = [0] * 10
        self.gsent_people = [None] * 10
        self.bsent_values = [0] * 10
        self.bsent_people = [None] * 10

    def reducer(self, author, type_tuple):
        up = 0
        sentiment = 0
        author_count = 0
        for tup in type_tuple:
            up += tup[0]
            sentiment += tup[1]
            author_count += tup[2]
        u = 9
        s = 9
        while up > self.up_values[u] and u > -1:
            u = u - 1
        if u != 9:
            self.up_values.insert((u + 1), up)
            self.up_people.insert((u + 1), author)

        while sentiment < self.bsent_values[s] and s > -1:
            s = s - 1
        if s != 9:
            self.bsent_values.insert((s + 1), sentiment)
            self.bsent_people.insert((s + 1), author)

        while sentiment > self.gsent_values[s] and s > -1:
            s = s - 1
        if s != 9:
            self.gsent_values.insert((s + 1), sentiment)
            self.gsent_people.insert((s + 1), author)

    def reducer_final(self):
        yield self.up_people[0], self.up_values[0]
        yield self.up_people[1], self.up_values[1]
        yield self.up_people[2], self.up_values[2]
        yield self.up_people[3], self.up_values[3]
        yield self.up_people[4], self.up_values[4]
        yield self.up_people[5], self.up_values[5]
        yield self.up_people[6], self.up_values[6]
        yield self.up_people[7], self.up_values[7]
        yield self.up_people[8], self.up_values[8]
        yield self.up_people[9], self.up_values[9]

        yield self.gsent_people[0], self.gsent_values[0]
        yield self.gsent_people[1], self.gsent_values[1]
        yield self.gsent_people[2], self.gsent_values[2]
        yield self.gsent_people[3], self.gsent_values[3]
        yield self.gsent_people[4], self.gsent_values[4]
        yield self.gsent_people[5], self.gsent_values[5]
        yield self.gsent_people[6], self.gsent_values[6]
        yield self.gsent_people[7], self.gsent_values[7]
        yield self.gsent_people[8], self.gsent_values[8]
        yield self.gsent_people[9], self.gsent_values[9]

        yield self.bsent_people[0], self.bsent_values[0]
        yield self.bsent_people[1], self.bsent_values[1]
        yield self.bsent_people[2], self.bsent_values[2]
        yield self.bsent_people[3], self.bsent_values[3]
        yield self.bsent_people[4], self.bsent_values[4]
        yield self.bsent_people[5], self.bsent_values[5]
        yield self.bsent_people[6], self.bsent_values[6]
        yield self.bsent_people[7], self.bsent_values[7]
        yield self.bsent_people[8], self.bsent_values[8]
        yield self.bsent_people[9], self.bsent_values[9]



if __name__ == '__main__':
    sent_count.run()