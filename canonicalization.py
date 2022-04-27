import csv
from surt import surt 
import json
import jsonlines
import re
import urllib, urllib.request
import feedparser
import time

def get_authors(file_name):
    print(file_name)
    try:
        authors = author_data[file_name]
        for author in authors:
            json_dict[repo_surt][file_name].append(author)
    except:
        time.sleep(1)
        author_data[file_name] = []
        parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0][0]
        url = 'http://export.arxiv.org/api/query?id_list=' + parsed_file
        response = urllib.request.urlopen(url).read()
        feed = feedparser.parse(response)
        for author in feed.entries[0].authors:
            author_data[file_name].append(author.name)
            json_dict['files'][file_name].append(author.name)

prev_surt = ''
curr_surt = ''
json_dict = {}

authors_json = open('authors.json', 'w')
author_data = {}

canon_json = open('data_processing/urls_and_authors.jsonl', 'w')
jsonl_writer = jsonlines.Writer(canon_json)

surt_csv = open('repo_results/github_surt.csv', newline='')
surt_reader = csv.reader(surt_csv, delimiter=' ')
for row in surt_reader:
    split_surt = row[0].split('/')
    user = split_surt[1]
    file_name = row[3]
    try:
        repo = split_surt[2]
        repo_surt = split_surt[0] + '/' + user + '/' + repo
    except:
        repo = ""
        repo_surt = split_surt[0] + '/' + user


    if prev_surt == '':
        prev_surt = repo_surt
        json_dict['surt'] = repo_surt
        json_dict['files'] = {}
        json_dict['files'][file_name] = []
        get_authors(file_name)

    elif prev_surt != repo_surt:
        jsonl_writer.write(json_dict)
        prev_surt = repo_surt
        json_dict['surt'] = repo_surt
        json_dict['files'] = {}
        json_dict['files'][file_name] = []
        get_authors(file_name)
    else:
        json_dict['files'][file_name] = []
        get_authors(file_name)

jsonl_writer.write(json_dict)
jsonl_writer.close()
json.dump(author_data, authors_json)
authors_json.close()
canon_json.close()