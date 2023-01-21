# Input: dedupe_surt.jsonl
# Output: timemap_results.csv (File, SURT, URL, TimeMap, Error), timemap_map.txt, timemap/
# Notes: Creates a TimeMap for each deduped URL

import csv
import jsonlines
import subprocess
import os
import re

host = os.uname()[1]
# host = 'test'
if host == 'terra':
    input_file = 'part_dedupe_surt_0.jsonl'
    timemap_file = 'timemap_map_0.csv'
    output_file = 'timemap_results_0.csv'
elif host == 'wsdl-docker':
    input_file = 'part_dedupe_surt_1.jsonl'
    timemap_file = 'timemap_map_1.csv'
    output_file = 'timemap_results_1.csv'
elif host == 'wsdl-docker-private':
    input_file = 'part_dedupe_surt_2.jsonl'
    timemap_file = 'timemap_map_2.csv'
    output_file = 'timemap_results_2.csv'
elif host == "test":
    input_file = 'test_surt.jsonl'
    timemap_file = 'test_timemap_map.csv'
    output_file = 'test_timemap_results.csv'

timemap_map_file = open("./data_processing/" + timemap_file, "w")
timemap_map_csv = csv.writer(timemap_map_file, delimiter=' ')

with jsonlines.open('data_processing/' + input_file, 'r') as jsonl_f:
     for line in jsonl_f:
        url = str(line['info'][0]['url']).lower()
        ghp = str(line['GHP'])

        if ghp == "GitHub":
            result = re.match(r'(http|https|git):\/\/(www.|)github.com\/([^\/]+)\/([^\/(\.)][a-zA-Z0-9-_]+)', url)
            if result != None and result != "":
                repo_url = result[0]
            else:
                repo_url = ' '
            whole_url = re.match(r'(http|https|git):\/\/(www.|)github.com\/(.*)', url)
            file = 'timemap/github' + '-'.join(whole_url[3].split('/')) + '.txt'
            os.system('./timemap_surt.sh ' + url + ' ' + file + ' skip')
            timemap_map_csv.writerow([url, ghp, repo_url, file])
        elif ghp == "GitLab":
            result = re.match(r'(http|https):\/\/(www.|)gitlab.com\/([^\/]+)\/([^\/(\.)][a-zA-Z0-9-_]+)', url)
            if result != None and result != "":
                repo_url = result[0] + '.git'
            else: 
                repo_url = ' '
            whole_url = re.match(r'(http|https):\/\/(www.|)gitlab.com\/(.*)', url)
            file = 'timemap/gitlab' + '-'.join(whole_url[3].split('/')) + '.txt'
            os.system('./timemap_surt.sh ' + url + ' ' + file + ' skip')
            timemap_map_csv.writerow([url, ghp, repo_url, file])
        elif ghp == "Bitbucket":
            result = re.match(r'(http|https):\/\/(www.|\w+@|)bitbucket.org\/([^\/]+)\/([^\/(\.)][a-zA-Z0-9-_]+)', url)
            if result != None and result != "": 
                repo_url = result[0]
            else: 
                repo_url = ' '
            whole_url = re.match(r'(http|https):\/\/(www.|\w+@|)bitbucket.org\/(.*)', url)
            file = 'timemap/bitbucket' + '-'.join(whole_url[3].split('/')) + '.txt'
            os.system('./timemap_surt.sh ' + url + ' ' + file + ' skip')
            timemap_map_csv.writerow([url, ghp, repo_url, file])
        elif ghp == "SourceForge":
            result = re.match(r'(http|https):\/\/(www.|)sourceforge.net\/(projects|p)\/([^\/(\.)][a-zA-Z0-9-_]+)', url)
            if result != None and result != "": 
                repo = result[4]
                repo_url = r"https://svn.code.sf.net/p/" + repo + r"/code"
            else:
                repo_url = ' '
            whole_url = re.match(r'(http|https):\/\/(www.|)sourceforge.net\/(.*)', url)
            file = 'timemap/sourceforge' + '-'.join(whole_url[3].split('/')) + '.txt'
            os.system('./timemap_surt.sh ' + url + ' ' + file + ' skip')
            timemap_map_csv.writerow([url, ghp, repo_url, file])

timemap_results = open("./data_processing/" + output_file, "a")
timemap_results_csv = csv.writer(timemap_results, delimiter=',')
# timemap_results_csv.writerow(['URL', 'GHP', 'RepoURL', 'File', 'TimeMap(Yes/No)', 'Error(Yes/No)'])

before_has_timemap = 0
after_has_timemap = 0
before_no_timemap = 0
after_no_timemap = 0
before_html = 0
after_html = 0
before_bad_gateway = 0
after_bad_gateway = 0
before_other = 0
after_other = 0

def check_timemap(file_name, rerun):
    infile = open(file_name, 'r')
    first_line = infile.readline().strip()
    if first_line == "{":
        if rerun:
            global after_has_timemap
            after_has_timemap = after_has_timemap + 1
        else:
            global before_has_timemap
            before_has_timemap = before_has_timemap + 1
        status = "TimeMap"
    elif first_line == "404 page not found":
        if rerun:
            global after_no_timemap
            after_no_timemap = after_no_timemap + 1
        else:
            global before_no_timemap
            before_no_timemap = before_no_timemap + 1
        status = "No TimeMap"
    elif first_line == "<html>":
        if rerun:
            global after_html
            after_html = after_html + 1
            status = "Error"
        else:
            global before_html
            before_html = before_html + 1
            status = "rerun"
    elif first_line == "Bad Gateway":
        if rerun:
            global after_bad_gateway
            after_bad_gateway = after_bad_gateway + 1
            status = "Error"
        else:
            global before_bad_gateway
            before_bad_gateway = before_bad_gateway + 1
            status = "rerun"
    else:
        if rerun:
            global after_other
            after_other = after_other + 1
            status = "Error"
        else:
            global before_other
            before_other = before_other + 1
            status = "rerun"
    return status

with open('./data_processing/' + timemap_file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        status = check_timemap(row[3], False)
        if status == "rerun":
            subprocess.check_call(["./timemap_surt.sh", row[0], row[3]])
            status = check_timemap(row[3], True)

        if status == "TimeMap":
            timemap_results_csv.writerow([row[0], row[1], row[2], row[3], 'Yes', 'No'])
        elif status == "No TimeMap":
            timemap_results_csv.writerow([row[0], row[1], row[2], row[3], 'No', 'No'])
        elif status == "Error":
            timemap_results_csv.writerow([row[0], row[1], row[2], row[3], 'No', 'Yes'])

print("Initial has timemap: " + str(before_has_timemap))
print("Initial no timemap: " + str(before_no_timemap))
print("Initial <html>: " + str(before_html))
print("Initial Bad Gateway: " + str(before_bad_gateway))
print("Initial other error: " + str(before_other))
print("Rerun has timemap: " + str(after_has_timemap))
print("rerun no timemap: " + str(after_no_timemap))
print("Rerun <html>: " + str(after_html))
print("Rerun Bad Gateway: " + str(after_bad_gateway))
print("Rerun other error: " + str(after_other))
timemap_results.close()            