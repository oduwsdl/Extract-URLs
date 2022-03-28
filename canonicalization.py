import csv
from surt import surt 
import json
import jsonlines
import re

prev_surt = ''
curr_surt = ''
json_dict = {}

canon_json = open('data_processing/urls_and_authors.jsonl', 'w')
jsonl_writer = jsonlines.Writer(canon_json)
author_json = open('/arxiv_data/authors-parsed.json')
author_dict = json.load(author_json)

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
        json_dict[repo_surt] = {}
        json_dict[repo_surt][file_name] = []
        try:
            parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0][0]
            for author in author_dict[parsed_file]: 
                json_dict[repo_surt][file_name].append(author)
        except:
            print("No " + file_name + "\n")

    elif prev_surt != repo_surt:
        jsonl_writer.write(json_dict)
        prev_surt = repo_surt
        json_dict = {}
        json_dict[repo_surt] = {}
        json_dict[repo_surt][file_name] = []
        try:
            parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0][0]
            for author in author_dict[parsed_file]: 
                json_dict[repo_surt][file_name].append(author)
        except:
            print("No " + file_name + "\n")
    else:
        json_dict[repo_surt][file_name] = []
        try:
            parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0][0]
            for author in author_dict[parsed_file]: 
                json_dict[repo_surt][file_name].append(author)
        except:
            print("No " + file_name + "\n")

jsonl_writer.write(json_dict)
jsonl_writer.close()
canon_json.close()