from mrjob.job import MRJob
import re
import json
import helper


class t_companies_baskets(MRJob):
    '''
    finds the top 100 companies and their top mentioned words
    '''
    def mapper_init(self):
        self.comp_list = set()
        self. stopwords = set()

        csv = open('companylist.csv')
        for i in csv:
            i = i.strip('\n')
            self.comp_list.add(i)

        stop = open('stopwords.csv')
        for s in stop:
            s = s.strip('\n')
            self.stopwords.add(s)


    def mapper(self, _, line):
        j = helper.clean_line(line)

        comment = j['body']
        words = re.findall(helper.PATTERN, comment)
        words = set(words)
        to_use = [x for x in words if x not in self.stopwords]

        for word in to_use:
            if word in self.comp_list:
                related_dict = helper.related_words(word, comment)
                yield word, (1, related_dict)


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
