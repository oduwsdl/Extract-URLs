import csv
import os
import re
import json

output_file_name = "tamu/tamu_urls.csv"
output_file = open(output_file_name, 'w')
output_csv = csv.writer(output_file, delimiter=' ')

file_list = os.listdir("raw_data_outputs/tamu_parsed/")
for file_name in file_list:
    dir = re.findall(r"(\d{6}).json", file_name)[0]
    f = open("raw_data_outputs/tamu_parsed/" + file_name, "r")
    json_data = json.load(f)
    for pdf_name in json_data[dir]["files"]:
        annot_urls = json_data[dir]["files"][pdf_name]["annot_urls"]
        text_urls = json_data[dir]["files"][pdf_name]["text_urls"]
        url_lists = {'annot_urls': annot_urls, 'text_urls': text_urls}
        for url_list in url_lists:
            for u in url_lists[url_list]:
                url = u.lower()
                output_csv.writerow([url])