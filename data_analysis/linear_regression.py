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
    data_dict = {}
    for item in raw_data:
        item = item.split('\t')
        nums = [float(x) for x in re.findall(num_pattern, item[1])]
        # nums = [total_mentions, total_sentiment]
        name = re.findall(name_pattern, item[0])[0]
        data_type = item[0][-2] # whether we are looking at month or week
        date = int(re.findall(date_pattern, item[0])[0]) # week/month number
        if name in data_items:
            data_items[name][data_type][date] = nums
        else:
            data_items[name] = {'m': {}, 'w': {}}
            data_items[name][data_type][date] = nums

    return data_dict


def make_data_struct(data_dict, training_set, typ, date, quarter):
    '''
    makes a data struct with points of interest

    data_dict (dict) - dictionary of data points
    training_set (dict) - dictionary of companies with their top products and their
                    quarterly earning performance
    typ (str) - using month or week?
    date (int) - which month or week?
    quarter (int) - which quarter are we analyzing?
    '''
    x = []
    y = []
    for key, value in training_set.items():
        y.append(value['earnings'][quarter - 1])

        count = 0
        total = 0
        for item in value['products']:
            count += data_dict[item][typ][date][0]
            total += data_dict[item][typ][date][1]

        x.append(total / count)

    data_table = pd.DataFrame({key: x, 'Earnings': y})

    return data_table
