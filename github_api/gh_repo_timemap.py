# Input: gh_timemap.csv
# Output: gh_timemap_map.csv and gh_repo_timemaps.csv
# Note: WIP

import csv
import os
import re
import subprocess

input_file = "gh_timemap.csv"
timemap_file = "gh_timemap_map.csv"
output_file = "gh_repo_timemaps.csv"

timemap_map_file = open(timemap_file, "w")
timemap_map_csv = csv.writer(timemap_map_file, delimiter=',')
timemap_map_csv.writerow(['URL', 'GHP', 'RepoURL', 'File'])

with open(input_file) as repos_file:
    repos = csv.reader(repos_file, delimiter=',')
    next(repos)
    for row in repos:
        repo = row[0]
        whole_url = re.match(r'(http|https|git):\/\/(www.|)github.com\/(.*)', repo)
        file = 'gh_timemap/github' + '-'.join(whole_url[3].split('/')) + '.txt'
        os.system('../timemaps/timemap_surt.sh ' + repo + ' ' + file + ' skip')
        timemap_map_csv.writerow([repo, 'GitHub', repo, file])
timemap_map_file.close()

timemap_results = open(output_file, "a")
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

with open(timemap_file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        status = check_timemap('../' + row[3], False)
        if status == "rerun":
            subprocess.check_call(["../timemaps/timemap_surt.sh", row[0], row[3]])
            status = check_timemap('../' + row[3], True)

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