import json
import csv

def clean_json(txt_file):
    '''
    turns json txt file to csv file
    '''
    my_csv = open(txt_file + '_csv.csv', 'wt')
    csv_writer = csv.writer(my_csv)

    for line in open(txt_file):
        json_v = json.loads(line)
        comments = json_v['body']
        comments = comments.replace('\n', '')
        comments = comments.replace('\r', '')
        comments = comments.replace('\t', '')
        epoch = json_v['created_utc']
        line = [comments, epoch]
        csv_writer.writerow(tuple(line))
