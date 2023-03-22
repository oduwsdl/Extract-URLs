import csv
import json

# For file in file_list:
# input_file = file
# output_file = file[:-4] + ".json"

input_file = "parsed_Arxiv-Output.csv"
output_file = "parsed_Arxiv-Output.json"

# Change location of JSON files
d = open("./classifier_results/" + output_file, "w")

with open("./classifier_results/" + input_file, newline='') as classifier_results_file:
    classifier_results = csv.reader(classifier_results_file, delimiter=',')

    # Derive the directory and replace dir
    dir = "0704"
    prev_filename = ""
    data = {dir: {"files":{}}}
    url_dict = {}

    next(classifier_results)
    for row in classifier_results:
        url = row[1]
        classification = row[2]
        filename = row[3]

        if url != "":
            if prev_filename != filename:
                if prev_filename != "":
                    url_dict = {"url_count":len(all_urls), "oads_count":len(oads_urls), "oads_urls":list(oads_urls), "non_oads_urls":list(non_oads_urls), "all_urls":sorted(oads_urls.union(non_oads_urls))}
                    data[dir]["files"][prev_filename] = url_dict
                all_urls, oads_urls, non_oads_urls = set(), set(), set()
            if classification == "OADS":
                oads_urls.add(url)
            else:
                non_oads_urls.add(url)
            all_urls.add(url)
            prev_filename = filename


    data[dir]["files"][prev_filename] = url_dict

json.dump(data, d)
d.close()