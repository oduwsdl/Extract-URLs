# Input: repo_urls.json
# Output: repo_url_counts.csv (directory, URL count, and category)
# Notes: same output at dir_urls.py without the 'Total' (all valid URLs) category

import json
import csv

repo_file = open("repo_results/pmc_repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

csv_file = open("data_processing/pmc_repo_url_counts.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['Directory', 'URLCount', 'Category'])

for dir in repo_json:
    sourceforge_count = repo_json[dir]["sourceforge"]["url_count"]
    github_count = repo_json[dir]["github"]["url_count"]
    gitlab_count = repo_json[dir]["gitlab"]["url_count"]
    bitbucket_count = repo_json[dir]["bitbucket"]["url_count"]
    dir_file = open("pmc_parsed/" + dir + ".json")
    dir_json = json.load(dir_file)
    dir_file.close()
    dir_count = 0
    file_count = 0
    for file in dir_json[dir]["files"]:
        file_count = file_count + 1

    csvwriter.writerow([dir[0:4] + "-" + dir[4:], sourceforge_count, "SourceForge"])
    csvwriter.writerow([dir[0:4] + "-" + dir[4:], github_count, "GitHub"])
    csvwriter.writerow([dir[0:4] + "-" + dir[4:], gitlab_count, "GitLab"])
    csvwriter.writerow([dir[0:4] + "-" + dir[4:], bitbucket_count, "Bitbucket"])
csv_file.close()