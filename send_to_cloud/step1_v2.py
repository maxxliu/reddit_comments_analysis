from mrjob.job import MRJob
import re
import json
from textblob import TextBlob
import os
from mrjob.step import MRStep

'''
this mapreduce DOES NOT require the helper.py file
this mapreduce takes in the UNPROCESSED files
'''


class t_companies_baskets(MRJob):
    '''
    finds the top 100 companies and their top mentioned words
    '''
    def mapper_init_1(self):

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


    def mapper_1(self, _, line):
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
        to_use = [x for x in to_use if x.lower() not in self.stopwords]
        new_str = ' '.join(to_use)

        for word in to_use:
            if word in self.comp_list:
                related = {}
                blob = TextBlob(new_str)

                for info in blob.tags:
                    if info[1] in self.related_word_tags and info[0] != word:
                        related[info[0]] = related.get(info[0], 0) + 1

                yield word, (1, related)


    def combiner_1(self, company, count_dict_tuple):
        count = 0
        related_dict = {}
        for tup in count_dict_tuple:
            count += tup[0]
            for word, values in tup[1].items():
                if word not in related_dict:
                    related_dict[word] = 0
                related_dict[word] += values
        yield company, (count, related_dict)


    def reducer_init_1(self):
        self.companies = [None] * 100
        self.comp_count = [0] * 100
        self.related_words = [None] * 100


    def reducer_1(self, company, count_dict_tuple):
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


    def reducer_final_1(self):
        yield None, (self.comp_count, self.companies, self.related_words)


    def reducer_concat(self, _, values):
        final_comp = [(0, 0, 0)] * 100

        for value in values:
            for i in range(100):
                cur = 99
                temp = (value[0][i], value[1][i], value[2][i])
                while cur >= 0:
                    if temp[0] > final_comp[cur][0]:
                        rm = final_comp.pop(cur)
                        final_comp.insert(cur, temp)
                        temp = rm
                    cur -= 1


        for item in final_comp:
            yield item[1], item[2]


    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init_1,
                    mapper=self.mapper_1,
                    combiner=self.combiner_1,
                    reducer_init=self.reducer_init_1,
                    reducer=self.reducer_1,
                    reducer_final=self.reducer_final_1),
            MRStep(reducer=self.reducer_concat)
        ]


if __name__ == '__main__':
    t_companies_baskets.run()
