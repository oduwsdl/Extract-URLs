# Input: new_dir/ (deleted directory)
# Output: pmc_full/ 

import json
import re
import os

file_list = os.listdir("raw_data_outputs/tamu_jsonl/")
for file_name in file_list:
    files = {}
    num = 0
    dir = re.findall(r"(\d{6}).json", file_name)[0]
    with open("raw_data_outputs/tamu_jsonl/" + file_name, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line.rstrip('\n|\r'))
            full_path = list(d.keys())[0]
            files.update(d)
            num = num + 1
    data = {dir:{}}
    data[dir]['files'] = files
    data[dir]['num_files'] = num
    j = open("raw_data_outputs/tamu_parsed/" + dir + ".json", "w")
    json.dump(data, j)
    j.close()
