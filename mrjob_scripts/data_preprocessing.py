import json
import csv

def json_txt(txt_file):
    '''
    turns json txt file to txt file
    '''
    my_txt = open(txt_file + '.txt', 'wt')

    for line in open(txt_file):
        json_v = json.loads(line)
        comments = json_v['body']
        comments = comments.replace('\n', '')
        comments = comments.replace('\r', '')
        comments = comments.replace('\t', '')
        comments = comments.replace(',', '')
        epoch = json_v['created_utc']
        my_txt.write(comments + ' , ' + str(epoch) + '\n')


def json_csv(txt_file):
    '''
    turns json txt file to csv file
    '''
    my_csv = open(txt_file + '.csv', 'wt')
    csv_writer = csv.writer(my_csv)

    for line in open(txt_file):
        json_v = json.loads(line)
        comments = json_v['body']
        comments = comments.replace('\n', '')
        comments = comments.replace('\r', '')
        comments = comments.replace('\t', '')
        comments = comments.replace(',', '')
        epoch = json_v['created_utc']
        line = (comments, epoch)
        csv_writer.writerow(line)
