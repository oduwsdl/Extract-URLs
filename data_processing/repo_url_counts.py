# Input: [pmc_]repo_urls.json
# Output: [pmc_]repo_url_counts.csv (directory, URL count, and category)
# Notes: same output at dir_urls.py without the 'Total' (all valid URLs) category

import json
import csv

# corpora = ["pmc", "arxiv", "class"]
corpora = ["tamu"]
for corpus in corpora:
    if corpus == "pmc":
        prefix = "pmc_"
    elif corpus == "arxiv":
        prefix = ""
    elif corpus == "class":
        prefix = "class_"
    elif corpus == "tamu":
        prefix = "tamu_"
    repo_file = open("repo_results/" + prefix + "repo_urls.json")
    repo_json = json.load(repo_file)
    repo_file.close()

    csv_file = open("data_processing/" + prefix + "repo_url_counts.csv", "w")
    csvwriter = csv.writer(csv_file)
    csvwriter.writerow(['Directory', 'URLCount', 'Category'])

    for dir in repo_json:
        if corpus == "pmc":
            date = dir[0:4] + "-" + dir[4:]
            dir_file = open("raw_data_outputs/" + prefix + "parsed/" + dir + ".json")
        elif corpus == "arxiv":
            date = "20" + dir[0:2] + "-" + dir[2:]
            dir_file = open("raw_data_outputs/" + prefix + "parsed/" + dir + ".json")
        elif corpus == "class":
            date = "20" + dir[0:2] + "-" + dir[2:]
            dir_file = open("raw_data_outputs/classifier_results/" + dir + ".json")
        elif corpus == "tamu":
            date = dir[0:4] + "-" + dir[4:]
            dir_file = open("raw_data_outputs/" + prefix + "parsed/" + dir + ".json")
        sourceforge_count = repo_json[dir]["sourceforge"]["url_count"]
        github_count = repo_json[dir]["github"]["url_count"]
        gitlab_count = repo_json[dir]["gitlab"]["url_count"]
        bitbucket_count = repo_json[dir]["bitbucket"]["url_count"]
        dir_json = json.load(dir_file)
        dir_file.close()
        dir_count = 0
        file_count = 0
        for file in dir_json[dir]["files"]:
            file_count = file_count + 1

        csvwriter.writerow([date, sourceforge_count, "SourceForge"])
        csvwriter.writerow([date, github_count, "GitHub"])
        csvwriter.writerow([date, gitlab_count, "GitLab"])
        csvwriter.writerow([date, bitbucket_count, "Bitbucket"])
    csv_file.close()