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
