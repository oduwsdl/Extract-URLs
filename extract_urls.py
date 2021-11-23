import concurrent.futures
import hashlib
import io
import json
import os
import re

import flask
import requests

from extractor import Extractor
from util import APIUtil

def extraction(pdf_path):
    extractor = Extractor()
    urls = extractor.extract_all_urls(pdf_path)
    return urls

f = open("1811_valid.txt", "w")

# Segment of code for looping through all directories in the 'pdf' directory
# pdf_dir_path = "/home/mklein/pdf/"
# dir_list = os.listdir(pdf_dir_path)
# for dir_path in dir_list:
#     print(pdf_dir_path + dir_path)

dir_path = "/home/mklein/pdf/1811/"
prev_file_base = ""
prev_version = ""
file_list = os.listdir(dir_path)
for file_name in sorted(file_list):
    parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0]
    file_base = parsed_file[0]
    if prev_file_base != file_base:
        if prev_file_base == "":
            prev_file_base = file_base
        else:
            f.write("Run for " + prev_file_base + "v" + prev_version + ".pdf\n")
            url_list = extraction(dir_path + prev_file_base + "v" + prev_version + ".pdf")
            f.write(str(url_list) + "\n")
            prev_file_base = file_base
    prev_version = parsed_file[1]
f.write("Run for " + prev_file_base + "v" + prev_version + ".pdf\n")
url_list = extraction(dir_path + prev_file_base + "v" + prev_version + ".pdf")
f.write(str(url_list) + "\n")
f.close()
