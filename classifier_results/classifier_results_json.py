import csv
import json
import re
import sys
import datetime
import jsonlines

corpus = sys.argv[1]

if corpus == "arxiv":
    input_file = "parsed_Arxiv-Output.csv"
    json_directory = "./raw_data_outputs/classifier_results/"
elif corpus == "pmc":
    input_file = "parsed_PMC-Output.csv"
    json_directory = "./raw_data_outputs/classifier_pmc_jsonl/"
    pmc_dir = {}
    with open('oa_non_comm_use_pdf.csv', newline='') as csvfile:
        csv_file = csv.reader(csvfile, delimiter=',')

        next(csv_file)
        for row in csv_file:
            full_path = row[0]
            citation = row[1]
            try:
                parsed_date = re.findall(r"(\d{4}) (\w{3}) (\d{1,2})", citation)[0]
                month_num = datetime.datetime.strptime(parsed_date[1], '%b').month
            except:
                try:
                    parsed_date = re.findall(r"(\d{4}) (\w{3})", citation)[0]
                    month_num = datetime.datetime.strptime(parsed_date[1], '%b').month
                except:
                    try:
                        parsed_date = re.findall(r"(\d{4})", citation)[0]
                        month_num = 1
                    except:
                        continue
            dir = parsed_date[0] + f"{month_num:02}"
            pmc_dir[full_path] = dir

def get_dir(filename):
    if corpus == "arxiv":
        return re.findall(r"(\d{4}).\d*v\d*.pdf", filename)[0]
    elif corpus == "pmc":
        return pmc_dir[filename]

with open("./classifier_results/" + input_file, newline='') as classifier_results_file:
    classifier_results = csv.reader(classifier_results_file, delimiter=' ')

    prev_filename = ""
    prev_dir = ""
    data = {}
    url_dict = {}

    for row in classifier_results:
        try:
            url = row[0]
            classification = row[2]
            filename = row[3]
        except:
            # print(row)
            continue
        try:
            dir = get_dir(filename)
        except:
            print(row)
            continue

        if prev_dir == "":
            if corpus == "arxiv":
                d = open(json_directory + dir + '.json', 'w')
            elif corpus == "pmc":
                d = open(json_directory + dir + '.json', 'a')
                jsonl_writer = jsonlines.Writer(d)
            data[dir] = {"files":{}}
            prev_dir = dir

        if url != "":
            if prev_filename != filename:
                if prev_filename != "":
                    url_dict = {"url_count":len(all_urls), "oads_count":len(oads_urls), "oads_urls":list(oads_urls), "non_oads_urls":list(non_oads_urls), "all_urls":sorted(oads_urls.union(non_oads_urls))}
                    data[prev_dir]["files"][prev_filename] = url_dict
                all_urls, oads_urls, non_oads_urls = set(), set(), set()
            if classification == "OADS":
                oads_urls.add(url)
            else:
                non_oads_urls.add(url)
            all_urls.add(url)
            prev_filename = filename

        if prev_dir != dir:
            if corpus == "arxiv":
                json.dump(data, d)
                d.close()
                d = open(json_directory + dir + '.json', 'w')
            elif corpus == "pmc":
                jsonl_writer.write(data)
                jsonl_writer.close()
                d = open(json_directory + dir + '.json', 'a')
                jsonl_writer = jsonlines.Writer(d)
            data = {}
            data[dir] = {"files":{}}
            prev_dir = dir

    data[dir]["files"][prev_filename] = url_dict

json.dump(data, d)
d.close()