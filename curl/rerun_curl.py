import os 
import csv
import re

i = 1

input_file = "curl_results.csv"
map_file = "rerun_curl_map_" + str(i) + ".csv" 

rerun_map_file = open('curl/' + map_file, "w")
rerun_csv = csv.writer(rerun_map_file, delimiter=',', quotechar='"')

with open('curl/' + input_file) as curl_results_file:
    curl_results = csv.reader(curl_results_file, delimiter=',', quotechar='"')
    next(curl_results)
    for row in curl_results:
        url = row[0].lower().rstrip('”,)')
        ghp = row[1]
        repo_url = row[2]
        file = 'rerun_curl_' + str(i) + '/' + row[3].split('/')[-1]
        http = row[5]
        if http != '200':
            os.system('curl/curl_url.sh ' + url + ' ' + file)
            rerun_csv.writerow([url, ghp, repo_url, file])

rerun_map_file.close()

# for row in rerun_urls_reader:
#     url = row[0]
#     ghp = row[1]
#     repo_url = row[2]
#     file = 'rerun_curl_' + i + '/' + row[3]
#     os.system('curl/curl_url.sh ' + url + ' raw_data_outputs/' + file)
#     rerun_map_csv.writerow([url, ghp, repo_url, file])
# rerun_urls_file.close()
