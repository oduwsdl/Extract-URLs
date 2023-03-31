# Input: TBD
# Output: 

import json
import os
import re

from extractor import Extractor
from util import APIUtil

def extraction(pdf_path):
    extractor = Extractor()
    urls = extractor.extract_all_urls(pdf_path)
    return urls

pdf_dir_path = "/data/etdrepo/"
file_list = sorted(os.listdir(pdf_dir_path))
prev_dir = ""
data = {}

output_dir_path = './raw_data_outputs/etd_parsed/'
if not os.path.exists(output_dir_path): 
    os.makedirs(output_dir_path)

for file_name in file_list:
    full_path = pdf_dir_path + file_name
    parsed_year = re.match(r"(\d{4})", file_name)[0]
    dir = parsed_year + "01"
    if prev_dir != dir:
        if prev_dir != "":
            f = open(output_dir_path + prev_dir + ".json", "w")
            json.dump(data, f)
            f.close()
        data = {dir: {"files": {}}}
    url_dict = extraction(full_path)
    data[dir]["files"][full_path] = url_dict
    prev_dir = dir
    
f = open(output_dir_path + prev_dir + ".json", "w")
json.dump(data, f)
f.close()    
