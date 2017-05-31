import re
import pandas as pd

PATTERN = '[a-zA-Z]+'

def top_companies(txt_file):
    '''
    creates dictionary of top companies and their buckets of products

    txt_file (txt) - txt file from the first mapreduce function with the
                        top companies
    '''
    txt = open(txt_file)
    d = {}
    companies = []

    for line in txt:
        words = re.findall(PATTERN, line)
        key = words.pop(0)
        d[key] = words
        companies.append(key)

    return d, companies

def training_data(txt_file, csv_file):
    '''
    this should be a dictionary with company as key and values of quarterly
    training data as well as bucket data
    data = {'Apple': {'earnings': [1, 2, 3, 4],
                        'products': [iPhone, iPod]}
    '''
    pass


def read_sent_file(txt_file):
    '''
    reads the sent file returned by the mapreduce and return easily searchable
    dictionary of all of the data

    txt_file (txt) - this is the text file from running the second mapreduce,
                        it should have all of the sentiment data
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
        if name in data_dict:
            data_dict[name][data_type][date] = nums
        else:
            data_dict[name] = {'m': {}, 'w': {}}
            data_dict[name][data_type][date] = nums

    return data_dict


def single_dp(data_dict, training_set, companies, typ, date, quarter):
    '''
    makes single data column with points of interest

    data_dict (dict) - dictionary of data points
    training_set (dict) - dictionary of companies with their top products and their
                    quarterly earning performance
    companies (list) - list of the top 100 companies
    typ (str) - using month or week?
    date (int) - which month or week?
    quarter (int) - which quarter are we analyzing?
    '''
    averages = []
    counts = []

    for company in companies:
        count = 0
        total = 0

        for item in training_set[company]['products']:
            count += data_dict[item][typ][date][0]
            total += data_dict[item][typ][date][1]

        averages.append(total / count)
        counts.append(total)

    avg_key = typ + int(date) + 'avg'
    count_key = typ + int(date) + 'cnt'
    temp_df = pd.DataFrame({avg_key: averages, count_key: counts})

    return temp_df


def mk_data_strct(data_dict, training_set, companies, m_r, w_r, quarter):
    '''
    makes a data struct with points of interest

    data_dict (dict) - dictionary of data points
    training_set (dict) - dictionary of companies with their top products and their
                    quarterly earning performance
    companies (list) - list of the top 100 companies
    m_r (tuple) - range of months to look at
    w_r (tuple) - range of weeks to look at
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

    data_table = pd.DataFrame({'Sentiment': x, 'Earnings': y})

    return data_table
