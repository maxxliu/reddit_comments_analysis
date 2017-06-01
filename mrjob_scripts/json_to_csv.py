import json
import csv

def clean_json(txt_file):
    '''
    turns json txt file to csv file
    '''
    my_txt = open(txt_file + '.txt', 'wt')
    # csv_writer = csv.writer(my_txt)

    for line in open(txt_file):
        json_v = json.loads(line)
        comments = json_v['body']
        comments = comments.replace('\n', '')
        comments = comments.replace('\r', '')
        comments = comments.replace('\t', '')
        comments = comments.replace(',', '')
        epoch = json_v['created_utc']
        my_txt.write(comments + ' , ' + str(epoch) + '\n')
        # csv_writer.writerow((line))
