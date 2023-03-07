# Input: oa_non_comm_use_pdf.csv
# Output: Updated completed_dirs.txt and created raw_data_outputs/pmc_parsed/[dir_name].json (with the extracted URLs for each file in the directory)
# Notes: Must be run on ssh connection to access /arxiv_data/pdf/

import csv
import datetime
import concurrent.futures
import hashlib
import io
import json
import os
import re
import time
import jsonlines

import flask
import requests

from extractor import Extractor
from util import APIUtil

def extraction(pdf_path):
    extractor = Extractor()
    urls = extractor.extract_all_urls(pdf_path)
    return urls
    
done = set(line.strip() for line in open('completed_files.txt'))
completed = open("completed_files.txt", "a")

with open('oa_non_comm_use_pdf.csv', newline='') as csvfile:
    csv_file = csv.reader(csvfile, delimiter=',')
    for row in csv_file:
        full_path = row[0]
        citation = row[1]
        if full_path not in done:
            completed.write(full_path + "\n")
            try:
                parsed_date = re.findall(r"(\d{4}) (\w{3}) (\d{1,2})", citation)[0]
                month_num = datetime.datetime.strptime(parsed_date[1], '%b').month
            except:
                try:
                    parsed_date = re.findall(r"(\d{4}) (\w{3})", citation)[0]
                    month_num = datetime.datetime.strptime(parsed_date[1], '%b').month
                except:
                    print(row)
                    continue
            dir = parsed_date[0][2:] + f"{month_num:02}"

            data = {}

            try:
                url_dict = extraction("/arxiv_data1/" + row[0])
            except: 
                print(row)
                # split_path = full_path.split('/')
                # directory = split_path[0] + '/' + split_path[1] + '/' + split_path[2]
                # os.system("mkdir -p /arxiv_data1/" + directory + "; cd /arxiv_data1/" + directory +  "; wget -e robots=off https://ftp.ncbi.nlm.nih.gov/pub/pmc/" + row[0] + "; cd ~/Extract-URLs")
                # url_dict = extraction("/arxiv_data1/" + row[0])
            data[full_path] = url_dict

            d = open("raw_data_outputs/pmc_parsed/" + dir + ".json", "a")
            jsonl_writer = jsonlines.Writer(d)
            jsonl_writer.write(data)
            jsonl_writer.close()
            d.close()
completed.close()
        

# # Segment of code for looping through all directories in the 'pdf' directory
# pdf_dir_path = "/arxiv_data/pdf/"
# completed = open("completed_dirs.txt", "w")
# # dir_list = os.listdir(pdf_dir_path)
# dir_list = ["2111"]

# for dir in dir_list:
#     completed.write(dir + "\n")
#     if not os.path.exists("parsed/" + dir + ".json"):
#         start_time = time.time()
#         d = open("parsed/" + dir + ".json", "w")

#         dir_path = pdf_dir_path + dir + "/"
#         file_list = os.listdir(dir_path)
#         data = {dir: {"files":{}}}

#         freq = {}
#         file_count = 0
#         prev_file_base = ""
#         max_version = ""

#         for file_name in sorted(file_list):
#             file_count = file_count + 1
#             try:
#                 parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0]
#             except:
#                 print(file_name + "\n")
#                 continue
#             file_base = parsed_file[0]
#             if prev_file_base != file_base:
#                 if prev_file_base == "":
#                     prev_file_base = file_base
#                 else:
#                     if max_version in freq:
#                         freq[max_version] = freq[max_version] + 1
#                     else:
#                         freq[max_version] = 1

#                     url_dict = extraction(dir_path + prev_file_base + "v" + max_version + ".pdf")
#                     data[dir]["files"][prev_file_base + "v" + max_version + ".pdf"] = url_dict
#                     prev_file_base = file_base
#                 max_version = parsed_file[1]
#             else:
#                 if int(max_version) < int(parsed_file[1]):
#                     max_version = parsed_file[1]

#         url_dict = extraction(dir_path + prev_file_base + "v" + max_version + ".pdf")
#         end_time = time.time()
#         run_time = round((end_time - start_time) / 60, 2)  # Run time is the time in minutes rounded to 2 decimals
#         data[dir]["files"][prev_file_base + "v" + max_version + ".pdf"] = url_dict
#         data[dir]["num_files"] = file_count
#         data[dir]["freq_version"] = freq
#         data[dir]["run_time"] = run_time
#         json.dump(data, d)
#         d.close()
# completed.close()