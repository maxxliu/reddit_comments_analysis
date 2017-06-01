from mrjob.job import MRJob
import re
import json
# from textblob import TextBlob
import os

'''
this mapreduce DOES NOT require the helper.py file
this mapreduce takes in the UNPROCESSED files
'''


class t_companies_baskets(MRJob):
    '''
    finds the top 100 companies and their top mentioned words
    '''
    def mapper_init(self):

        self.comp_list = set()
        self.stopwords = set()
        self.related_word_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']
        self.pattern = '[a-zA-Z]+'

        csv = open('companylist.csv')
        for i in csv:
            i = i.strip('\n')
            self.comp_list.add(i)

        stop = open('stopwords.csv')
        for s in stop:
            s = s.strip('\n')
            self.stopwords.add(s)


    def mapper(self, _, line):
        json_v = json.loads(line)
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
            if word in self.comp_list:
                related = {}
                # blob = TextBlob(comment)

                for info in to_use:
                    if info != word:
                        related[info] = related.get(info, 0) + 1

                # for info in blob.tags:
                #     if info[1] in self.related_word_tags and info[0] != word:
                #         related[info[0]] = related.get(info[0], 0) + 1

                yield word, (1, related)


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
    t_companies_baskets.run()
