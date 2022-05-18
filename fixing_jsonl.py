import jsonlines
import json
import csv
import re
import os

file_list = os.listdir("new_dir/")
for file_name in file_list:
    files = {}
    num = 0
    dir = re.findall(r"(\d{4}).json", file_name)[0]
    new_dir = '19' + str(dir)
    print(new_dir)
    with open("new_dir/" + file_name, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line.rstrip('\n|\r'))
            full_path = list(d.keys())[0]
            files.update(d)
            num = num + 1
    data = {new_dir:{}}
    data[new_dir]['files'] = files
    data[new_dir]['num_files'] = num
    j = open("pmc_parsed/" + new_dir + ".json", "w")
    json.dump(data, j)
    j.close()
