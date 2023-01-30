import os 
import csv
import re

input_file = "curl_results.csv"
output_file = "rerun_curl.csv"
map_file = "rerun_curl_map.csv" 
i = 0

rerun_file = open('./data_processing/' + output_file, "w")
rerun_csv = csv.writer(rerun_file, delimeter=',')

with open('data_processing/' + input_file) as curl_results_file:
    curl_results = csv.reader(curl_results_file, delimiter=',')
    next(curl_results)
    for row in curl_results:
        url = row[0].lower()
        ghp = row[1]
        repo_url = row[2]
        file = row[3].strip('/')[1]
        http = row[5]
        if http != '200':
            rerun_csv.writerow([url, ghp, file])

rerun_file.close()

rerun_map = open('./data_processing/' + map_file, "w")
rerun_map_csv = csv.writer(rerun_map, delimiter=',')

rerun_urls_file = open('data_processing/' + output_file)
rerun_urls_reader = csv.reader(rerun_urls_file, delimiter=',')
for row in rerun_urls_reader:
    url = row[0]
    ghp = row[1]
    repo_url = row[2]
    file = 'rerun_curl_' + i + '/' + row[3]
    os.system('./curl_url.sh ' + url + ' ' + file)
    rerun_map_csv.writerow([url, ghp, repo_url, file])
rerun_urls_file.close()
