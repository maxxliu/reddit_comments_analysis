# for testing on smaller data set
# note that the json format and data avilable for 2016 is
# slightly different but should still be ok
import json
import time
import datetime
import nltk.tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk


DATES = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
            'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10',
            'Nov': '11', 'Dec': '12'}


def clean_line(raw_line):
    '''
    cleans raw line from data set
    '''
    json_v = json.loads(raw_line)
    epoch = json_v['created_utc']
    json_v['time'] = time.strftime("%a %d %b %Y %H:%M:%S", time.localtime(epoch))
    # day of the week, day, month, year, time
    day = json_v['time'][4:6]
    month = json_v['time'][7:10]
    year = json_v['time'][11:15]
    n_mnth = DATES[month]
    week_num = datetime.date(int(year), int(n_mnth), int(day)).isocalendar()[1]
    json_v['week'] = week_num
    json_v['month'] = n_mnth
    comment = json_v['body']
    comment = comment.replace('\n', '')
    comment = comment.replace('\r', '')
    json_v['body'] = comment.lower()

    return json_v



def init_data():
    '''
    reads each line of the file
    '''
    raw_data = open('2005/RC_2005-12')
    data_lst = []
    for line in raw_data:
        json_v = clean_line(line)
        data_lst.append(json_v)

    return data_lst

def body_list(data):
    '''
    just creates a list of the actual comments so we can play with nltk
    '''
    comments = []
    for d in data:
        comment = d['body']
        comments.append(comment)

    return comments


def sent_analysis(comment):
    '''
    runs a sentiment analysis on a comment by sentence and returns sent_score
    of average sentiment score of sentences
    '''
    sent_score = 0
    sent_list = nltk.sent_tokenize(comment)
    sentiment = SIA()
    scores_list = []
    if len(sent_list) > 0:
        for sent in sent_list:
            score_dict = sentiment.polarity_scores(sent)
            score = score_dict['compound']
            scores_list.append(score)
        sent_score = sum(scores_list)/len(scores_list)
    return sent_score


if __name__=='__main__':
    data = init_data()
    comments = body_list(data)
