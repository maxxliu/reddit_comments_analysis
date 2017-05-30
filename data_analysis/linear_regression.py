import re
import pandas as pd


def training_data(txt_file, csv_file):
    '''
    this should be a dictionary with company as key and values of quarterly
    training data as well as bucket data
    data = {'Apple': {'earnings': [1, 2, 3, 4],
                        'products': [iPhone, iPod]}
    '''
    pass

def read_txt_file(txt_file):
    '''
    reads the txt file returned by the mapreduce and return easily searchable
    dictionary of all of the data
    '''
    num_pattern = '[0-9]+\.[0-9]+|[0-9]+'
    name_pattern = '([a-zA-Z]+)\d'
    date_pattern = '[0-9]+'
    raw_data = open(txt_file)
    data_items = {}
    for item in raw_data:
        item = item.split('\t')
        nums = [float(x) for x in re.findall(num_pattern, item[1])]
        # nums = [average_sentiment, total_mentions, total_sentiment]
        name = re.findall(name_pattern, item[0])[0]
        data_type = item[0][-2] # whether we are looking at month or week
        date = int(re.findall(date_pattern, item[0])[0]) # week/month number
        if name in data_items:
            data_items[name][data_type][date] = nums
        else:
            data_items[name] = {'m': {}, 'w': {}}
            data_items[name][data_type][date] = nums

    return data_items


def make_data_struct(txt_file):
    '''
    makes a
    txt_file (text file): text file with the results from sentiment analysis
    '''
    pass
