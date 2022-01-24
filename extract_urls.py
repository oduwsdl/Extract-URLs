# Input: /arxiv_data/pdf/
# Output: Updated completed_dirs.txt and created parsed/[dir_name].json (with the extracted URLs for each file in the directory)
# Notes: Must be run on ssh connection to access /arxiv_data/pdf/

import concurrent.futures
import hashlib
import io
import json
import os
import re
import time

import flask
import requests

from extractor import Extractor
from util import APIUtil

def extraction(pdf_path):
    extractor = Extractor()
    urls = extractor.extract_all_urls(pdf_path)
    return urls



# Segment of code for looping through all directories in the 'pdf' directory
pdf_dir_path = "/arxiv_data/pdf/"
completed = open("completed_dirs.txt", "a")
# dir_list = os.listdir(pdf_dir_path)
dir_list = ["2112"]

for dir in dir_list:
    completed.write(dir + "\n")
    if not os.path.exists("parsed/" + dir + ".json"):
        start_time = time.time()
        d = open("parsed/" + dir + ".json", "w")
        dir_path = pdf_dir_path + dir + "/"
        file_list = os.listdir(dir_path)
        data = {dir: {"files":{}}}

        freq = {}
        file_count = 0
        prev_file_base = ""
        max_version = ""

        for file_name in sorted(file_list):
            file_count = file_count + 1
            try:
                parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0]
            except:
                print(file_name + "\n")
                continue
            file_base = parsed_file[0]
            if prev_file_base != file_base:
                if prev_file_base == "":
                    prev_file_base = file_base
                else:
                    if max_version in freq:
                        freq[max_version] = freq[max_version] + 1
                    else:
                        freq[max_version] = 1

                    url_dict = extraction(dir_path + prev_file_base + "v" + max_version + ".pdf")
                    data[dir]["files"][prev_file_base + "v" + max_version + ".pdf"] = url_dict
                    prev_file_base = file_base
                max_version = parsed_file[1]
            else:
                if int(max_version) < int(parsed_file[1]):
                    max_version = parsed_file[1]

        url_dict = extraction(dir_path + prev_file_base + "v" + max_version + ".pdf")
        end_time = time.time()
        run_time = round((end_time - start_time) / 60, 2)  # Run time is the time in minutes rounded to 2 decimals
        data[dir]["files"][prev_file_base + "v" + max_version + ".pdf"] = url_dict
        data[dir]["num_files"] = file_count
        data[dir]["freq_version"] = freq
        data[dir]["run_time"] = run_time
        json.dump(data, d)
        d.close()
completed.close()