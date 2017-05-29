import nltk.tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

RELATED_WORD_TAGS = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']


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


def related_words(key_word, comment):
    '''
    '''
    related = {}
    word_list = nltk.word_tokenize(comment)
    tagged_words = nltk.pos_tag(word_list)

    for info in tagged_words:
        if info[1] in RELATED_WORD_TAGS and info[0] != key_word:
            related[info[0]] = related.get(info[0], 0) + 1

    return related 


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