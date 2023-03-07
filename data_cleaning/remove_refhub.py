# Input: pmc_full/
# Output: pmc_parsed/
# Notes: pmc_full/ contains all URLs, pmc_parse/ contains all URLs except Elsevier, Creative Commons, and Crossmark

import json
import re
import os

file_list = os.listdir("raw_data_outputs/pmc_full/")
for file_name in file_list:
    print(file_name)
    dir = re.findall(r"(\d{6}).json", file_name)[0]

    j = open("raw_data_outputs/pmc_full/" + file_name, "r")
    data = json.load(j)
    j.close
    files = data[dir]['files']

    for file in data[dir]['files']:
        annot_urls = []
        text_urls = []
        for url in data[dir]['files'][file]['annot_urls']:
            refhub = re.search(r"(https:\/\/refhub.elsevier.com)", url)
            creative_commons = re.search(r"(https:\/\/(www.)?creative)", url)
            crossmark = re.search(r"(https:\/\/crossmark.crossref.org)", url)
            if refhub is None and creative_commons is None and crossmark is None:
                annot_urls.append(url)
        for url in data[dir]['files'][file]['text_urls']:
            refhub = re.search(r"(https:\/\/refhub.elsevier.com)", url)
            creative_commons = re.search(r"(https:\/\/(www.)?creative)", url)
            crossmark = re.search(r"(https:\/\/crossmark.crossref.org)", url)
            if refhub is None and creative_commons is None and crossmark is None:
                text_urls.append(url)

        all_urls = list(set(annot_urls) | set(text_urls))

        data[dir]['files'][file]['annot_urls'] = annot_urls
        data[dir]['files'][file]['text_urls'] = text_urls
        data[dir]['files'][file]['all_urls'] = all_urls
        data[dir]['files'][file]['url_count'] = len(all_urls)

    j = open("raw_data_outputs/pmc_parsed/" + file_name, "w")
    json.dump(data, j)
    j.close()

        