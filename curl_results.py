import os
import re
import csv

http_404 = 0
http_200 = 0
http_none = 0
http_other = 0
with open('data_processing/test_curl_map.csv', newline='') as map_file:
    curl_map = csv.reader(map_file, delimiter=',')
    for row in curl_map:
        url = row[0]
        file_name = row[3]
        with open(file_name, 'r') as f:
            status = ""
            for line in f:
                http_code = re.findall(r"HTTP\/.{1,3} (\d*)", line)
                if len(http_code) != 0:
                    status = http_code[0]
                l = re.findall(r"^[Ll]ocation: (.*)$", line)
            if l != []:
                location = l[0]
            else:
                location = ''
            if status == "404":
                http_404 = http_404 + 1
            elif status == "200":
                http_200 = http_200 + 1
            elif status == "":
                http_none = http_none + 1
            else: 
                http_other = http_other + 1
            print(url + " " + location + " " + status)
