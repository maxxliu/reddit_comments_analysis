from textblob import TextBlob
import json
import time
import datetime


PATTERN = '[a-zA-Z]+'


DATES = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
            'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10',
            'Nov': '11', 'Dec': '12'}


RELATED_WORD_TAGS = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']


def clean_line(raw_line):
    '''
    cleans raw line from data set

    raw_line (string) - json string
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
    tells us the sentiment towards a product word we are intersted in

    product (string) - word that we are looking at sentiment for
    comment (string) - the reddit comment
    '''
    mentions = 0
    total_sentiment = 0
    blob = TextBlob(comment)

    for sent in blob.sentences:
        if product in sent:
            mentions += 1
            analysis = sent.sentiment.polarity
            total_sentiment += analysis

    return mentions, total_sentiment


def related_words(key_word, comment):
    '''
    finds all of the related words in a string

    key_word (string) - word that we are looking for related words for
    comment (string) - comment string
    '''
    related = {}
    blob = TextBlob(comment)

    for info in blob.tags:
        if info[1] in RELATED_WORD_TAGS and info[0] != key_word:
            related[info[0]] = related.get(info[0], 0) + 1

    return related
