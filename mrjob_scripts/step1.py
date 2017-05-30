from mrjob.job import MRJob
import re
import json
import helper


COMP_LIST = []

def load_lst():
    csv = open('companylist.csv')
    for i in csv:
        i = i.strip('\n')
        COMP_LIST.append(i)
    COMP_LIST.pop(0)

class t_companies_baskets(MRJob):
    '''
    yields 3 lists of commenters:
    1. Commenters with highest upvote counts
    2. Commenters that are the meanest
    3. Commenters that are the nicest
    '''

    def mapper(self, _, line):
        j = helper.clean_line(line)

        comment = j['body']
        words = set([x.strip(",.'!?/:;-_#$[]()%*") for x in comment.split(' ')])
        to_use = [x for x in words if x not in helper.STOPWORDS]

        for word in to_use:
            if word in COMP_LIST:
                related_dict = helper.related_words(company, to_use)
                yield company, (1, related_dict)


    def combiner(self, company, count_dict_tuple):
        count = 0
        related_dict = {}
        for tup in count_dict_tuple:
            count += tup[0]
            for word, values in tup[1].items():
                if word not in related_dict:
                    related_dict[word] = 0
                related_dict[word] += values
        yield company, (count, related_dict)



    def reducer_init(self):
        self.companies = [None] * 100
        self.comp_count = [0] * 100
        self.related_words = [None] * 100


    def reducer(self, company, count_dict_tuple):
        count = 0
        related_dict = {}
        for tup in count_dict_tuple:
            count += tup[0]
            for word, values in tup[1].items():
                if word not in related_dict:
                    related_dict[word] = 0
                related_dict[word] += values
        u = 99
        while count > self.comp_count[u] and u > -1:
            u = u - 1
        if u != 99:
            self.companies.insert((u + 1), company)
            self.comp_count.insert((u + 1), count)
            sorted_words = sorted(related_dict, key=related_dict.get, reverse=True)
            self.related_words.insert((u + 1), sorted_words[0:5])


    def reducer_final(self):
        for i in range(100):
            yield self.companies[i] ,self.related_words[i]



if __name__ == '__main__':
    load_lst()
    t_companies_baskets.run()
