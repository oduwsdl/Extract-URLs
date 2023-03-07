# Input: ../repo_results/[github_surt.csv, gitlab_surt.csv, bitbucket_surt.csv, sourceforge_surt.csv] (these files combine the corpora)
# Output: ../data_processing/dedupe_surt.jsonl 

import jsonlines
import csv

json_file = open('data_processing/dedupe_surt.jsonl', 'w')
jsonl_writer = jsonlines.Writer(json_file)

file_list = ['github_surt.csv', 'gitlab_surt.csv', 'bitbucket_surt.csv', 'sourceforge_surt.csv']
for file_name in file_list:
    csv_file = open('repo_results/' + file_name)
    csv_reader = csv.reader(csv_file, delimiter=' ')
    prev_surt = ''
    ghp = ''
    surt = {}
    for row in csv_reader:
        curr_surt = row[1]
        curr_surt_dict = {'url': row[0], 'dir': row[2], 'file': row[3], 'corpus': row[4]}
        if prev_surt == '':
            surt_list = []
            surt_list.append(curr_surt_dict)
            prev_surt = curr_surt
            ghp = row[5]
        elif prev_surt == curr_surt:
            surt_list.append(curr_surt_dict)
        elif prev_surt != curr_surt:
            surt = {'surt': prev_surt, 'info': surt_list, 'GHP': ghp}
            jsonl_writer.write(surt)
            prev_surt = curr_surt
            surt_list = []
            surt_list.append(curr_surt_dict)
            ghp = row[5]

jsonl_writer.close()
