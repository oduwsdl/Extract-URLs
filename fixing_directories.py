import jsonlines
import json
import csv
import re
import os

csv_file = open('../oa_non_comm_use_pdf.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
all_files = list(csv_reader)

# file_list = os.listdir("conflict_parsed/")
file_list = ['1009.json']
for file_name in file_list:
    print(file_name)
    dir = re.findall(r"(\d{4}).json", file_name)[0]
    with open("conflict_parsed/" + file_name, 'r', encoding='utf-8') as f:
        dir1900 = '19' + str(dir)
        j1900 = open("pmc_parsed/" + dir1900 + ".json")
        data1900 = json.load(j1900)
        files1900 = data1900[dir1900]['files']

        dir2000 = '20' + str(dir)
        j2000 = open("pmc_parsed/" + dir2000 + ".json")
        data2000 = json.load(j2000)
        files2000 = data2000[dir2000]['files']
        for line in f:
            try:
                d = json.loads(line.rstrip('\n|\r'))
            except:
                print(d)
                print("Except")
                continue
            
            full_path = list(d.keys())[0]

            #loop through the csv list
            for row in all_files:
                if full_path == row[0]:
                    citation = row[1]
                    try:
                        parsed_date = re.findall(r"(\d{4}) (\w{3}) (\d{1,2})", citation)[0]
                    except:
                        try:
                            parsed_date = re.findall(r"(\d{4}) (\w{3})", citation)[0]
                        except:
                            continue
                    if parsed_date[0][:2] == '19':
                        files1900.update(d)
                    elif parsed_date[0][:2] == '20':
                        files2000.update(d)
            csv_file.close()
    data1900[dir1900]['files'] = files1900
    data1900[dir1900]['num_files'] = len(data1900[dir1900]['files'].keys())

    data2000[dir2000]['files'] = files2000
    data2000[dir2000]['num_files'] = len(data2000[dir2000]['files'].keys())

    print(data1900)
    json.dump(data1900, j1900)
    # j.close()

    print(data2000)
    json.dump(data2000, j2000)
    # j.close()
        