# for testing on smaller data set
# note that the json format and data avilable for 2016 is
# slightly different but should still be ok
import json
import time
import nltk.tokenize
from nltk.sentiment.vader import SentimentIntensityanalyzer as SIA


import nltk

def init_data():
    '''
    reads each line of the file
    '''
    raw_data = open('2005/RC_2005-12')
    data_lst = []
    for line in raw_data:
        json_v = json.loads(line)
        epoch = json_v['created_utc']
        json_v['time'] = time.strftime("%a %d %b %Y %H:%M:%S", time.localtime(epoch))
        # day of the week, day, month, year, time
        data_lst.append(json_v)

    return data_lst

def body_list(data):
    '''
    just creates a list of the actual comments so we can play with nltk
    '''
    comments = []
    for d in data:
        comments.append(d['body'])

    return comments


def sent_analysis(comment):
    '''
    runs a sentiment analysis on a comment by sentence and returns sent_score
    of average sentiment score of sentences
    '''
    sent_list = nltk.sent_tokenize(comment)
    sentiment = SIA()
    scores_list = []

    for sent in sent_list:
        score = sentiment.polarity_scores(sent)
        scores_list.append(score)

    sent_score = sum(scores_list)/len(scores_list)

    return sent_score


if __name__=='__main__':
    data = init_data()
    comments = body_list(data)
