import csv
import json
import re

input_file = "parsed_Arxiv-Output.csv"

def get_dir(filename):
    return re.findall(r"(\d{4}).\d*v\d*.pdf", filename)[0]

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
            print(row)
            continue
        try:
            dir = get_dir(filename)
        except:
            print(row)
            continue

        if prev_dir == "":
            d = open('./raw_data_outputs/classifier_results/' + dir + '.json', 'w')
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
            json.dump(data, d)
            d.close()
            d = open('./raw_data_outputs/classifier_results/' + dir + '.json', 'w')
            data = {}
            data[dir] = {"files":{}}
            prev_dir = dir

    data[dir]["files"][prev_filename] = url_dict

json.dump(data, d)
d.close()