import nltk.tokenize
from textblob import TextBlob


def comment_analysis(key_word, comment):
    '''
    '''
    comment_analysis = {'mentions': 0, 'score': 0}
    scores = []
    sent_list = nltk.sent_tokenize(comment)
    
    for sent in sent_list:
        if word_in(key_word, sent):
            comment_analysis['mentions'] += 1
            analysis = TextBlob(sent)
            scores.append(analysis.sentiment.polarity)

    comment_analysis['score'] = sum(scores) / len(scores)

    return comment_analysis


def dumb_analysis(comment):
    '''
    '''
    sent_list = nltk.sent_tokenize(comment)
    scores = []

    for sent in sent_list:
        analysis = TextBlob(sent)
        scores.append(analysis.sentiment.polarity)

    return sum(scores) / len(scores)


def word_in(key_word, sent):
    if key_word in sent:
        return True