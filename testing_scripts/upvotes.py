from mrjob.job import MRJob
import re
import json

class guest_staff(MRJob):
    '''
    yields a list of people who were both
    visitors and staffers of the white house.
    '''


        up = a['ups']


    def mapper(self, _, line):
        json = json.loads(line)
        up = json['ups']
        author = json['author']
        body = json['body']
        body = body.replace("\r\n", " ")
        body = body.replace("\n", " ")
        body = body.replace("\r", " ")
        sentiment = body #do some sentiment analysis right here
        yield author, (up, sentiment)   

    def combiner(self, author, type_tuple):
        up = 0
        sentiment = 0
        for tup in type_tuple:
            up += tup[0]
            sentiment += tup[1]
        yield author, (up, sentiment)

    def reducer_init(self):
        self.up_values = [0] * 10
        self.up_people = [None] * 10
        self.sent_values = [0] * 10
        self.sent_people = [None] * 10

    def reducer(self, author, type_person):
        up = 0
        sentiment = 0
        for tup in type_tuple:
            up += tup[0]
            sentiment += tup[1]
        u = 9
        s = 9
        while up > self.up_values[u] and u > -1:
            u = u - 1
        if u != 9:
            self.up_values.insert((u + 1), up)
            self.up_people.insert((u + 1), author)

        while sentiment > self.sent_values[s] and s > -1:
            s = s - 1
        if s != 9:
            self.sent_values.insert((s + 1), sentiment)
            self.sent_people.insert((s + 1), author)

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

        yield self.sent_people[0], self.sent_values[0]
        yield self.sent_people[1], self.sent_values[1]
        yield self.sent_people[2], self.sent_values[2]
        yield self.sent_people[3], self.sent_values[3]
        yield self.sent_people[4], self.sent_values[4]
        yield self.sent_people[5], self.sent_values[5]
        yield self.sent_people[6], self.sent_values[6]
        yield self.sent_people[7], self.sent_values[7]
        yield self.sent_people[8], self.sent_values[8]
        yield self.sent_people[9], self.sent_values[9]



if __name__ == '__main__':
    guest_staff.run()