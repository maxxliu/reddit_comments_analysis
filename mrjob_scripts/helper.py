import nltk.tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import json
import time
import datetime


DATES = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
            'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10',
            'Nov': '11', 'Dec': '12'}

STOPWORDS = set(stopwords.words('english'))
RELATED_WORD_TAGS = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']


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
    json_v['week'] = str(week_num)
    json_v['month'] = n_mnth
    json_v['year'] = year
    comment = json_v['body']
    comment = comment.replace('\n', '')
    comment = comment.replace('\r', '')
    json_v['body'] = comment

    return json_v


def product_sentiment(product, comment):
    '''
    '''
    mentions = 0
    total_sentiment = 0
    sent_list = nltk.sent_tokenize(comment)

    for sent in sent_list:
        if product in sent:
            mentions += 1
            analysis = TextBlob(sent)
            total_sentiment += analysis.sentiment.polarity

    return mentions, total_sentiment


def related_words(key_word, to_use):
    '''
    '''
    related = {}
    tagged_words = nltk.pos_tag(to_use)

    for info in tagged_words:
        if info[1] in RELATED_WORD_TAGS and info[0] != key_word:
            related[info[0]] = related.get(info[0], 0) + 1

    return related
