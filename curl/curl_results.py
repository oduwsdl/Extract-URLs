# Input: ../data_processing/dedupe_curl_map.csv and all of the swh_curl/ files mentioned in it
# Output: curl_results.csv
# Notes: run with `python3 curl_results.py > curl_results.csv`, REFACTOR

import re
import csv

http_404 = 0
http_200 = 0
http_none = 0
http_other = 0
# with open('dedupe_curl_map.csv', newline='') as map_file:
with open('rerun_curl_map_1.csv', newline='') as map_file:
    curl_map = csv.reader(map_file, delimiter=',')
    for row in curl_map:
        url = row[0]
        ghp = row[1]
        repo_url = row[2]
        file_name = row[3]
        try: 
            with open('../raw_data_outputs/' + file_name, 'r') as f:
                status = ""
                location = ""
                for line in f:
                    http_code = re.findall(r"HTTP\/.{1,3} (\d*)", line)
                    if len(http_code) != 0:
                        status = http_code[0]
                    l = re.findall(r"^[Ll]ocation: (.*)$", line)
                    if len(l) != 0:
                        location = l[0]
                if status == "404":
                    http_404 = http_404 + 1
                elif status == "200":
                    http_200 = http_200 + 1
                elif status == "":
                    http_none = http_none + 1
                else: 
                    http_other = http_other + 1
        except:
            location = "DNE"
            status = "DNE"
        print(url + "," + ghp + "," + repo_url + "," + file_name + "," + location + "," + status)
