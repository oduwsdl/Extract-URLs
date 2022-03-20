import csv
from surt import surt 

prev_surt = ''
curr_surt = ''
files = []

canon_json = open('data_processing/urls_and_authors.jsonl', 'w')

surt_csv = open('repo_results/github_surt.csv', newline='')
surt_reader = csv.reader(surt_csv, delimiter=' ')
for row in surt_reader:
    split_surt = row[0].split('/')
    user = split_surt[1]
    try:
        repo = split_surt[2]
        repo_surt = split_surt[0] + '/' + split_surt[1] + '/' + split_surt[2]
    except:
        repo = ""
        repo_surt = split_surt[0] + '/' + split_surt[1]
    if prev_surt == '':
        prev_surt = repo_surt
    elif prev_surt != repo_surt:
        print(repo_surt)
        print(files)
        prev_surt = repo_surt
        files = [row[3]]
    else:
        files.append(row[3])


canon_json.close()