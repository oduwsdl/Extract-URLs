# Input: repo_urls.json (from get_repo_urls.py)
# Output: dir_urls.csv (directory, URL count, and category) and file_count.csv (directory and file count)
# Notes: Outputs to terminal: total file count, total URL count, counts for each platform

import json
import csv

repo_file = open("./repo_results/repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

csv_file = open("./data_processing/dir_urls.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['Directory', 'URLCount', 'Category'])

csv_file2 = open("./data_processing/file_count.csv", "w")
csvwriter2 = csv.writer(csv_file2)
csvwriter2.writerow(['Directory', 'FileCount'])

total_file_count = 0
total_url_count = 0
total_sourceforge_count = 0
total_github_count = 0
total_gitlab_count = 0
total_bitbucket_count = 0
for dir in repo_json:
    sourceforge_count = repo_json[dir]["sourceforge"]["url_count"]
    github_count = repo_json[dir]["github"]["url_count"]
    gitlab_count = repo_json[dir]["gitlab"]["url_count"]
    bitbucket_count = repo_json[dir]["bitbucket"]["url_count"]
    total_sourceforge_count = total_sourceforge_count + sourceforge_count
    total_github_count = total_github_count + github_count
    total_gitlab_count = total_gitlab_count + gitlab_count
    total_bitbucket_count = total_bitbucket_count + bitbucket_count
    dir_file = open("parsed/" + dir + ".json")
    dir_json = json.load(dir_file)
    dir_file.close()
    url_count = 0
    file_count = 0
    for file in dir_json[dir]["files"]:
        file_count = file_count + 1
        url_count = url_count + dir_json[dir]["files"][file]["url_count"]
    total_file_count = total_file_count + file_count
    total_url_count = total_url_count + url_count
    csvwriter2.writerow(["20" + dir[0:2] + "-" + dir[2:], file_count])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], url_count, "Total"])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], sourceforge_count, "SourceForge"])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], github_count, "GitHub"])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], gitlab_count, "GitLab"])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], bitbucket_count, "Bitbucket"])
print("Total file count: " + str(total_file_count))
print("Total URL count: " + str(total_url_count))
print("SourceForge count: " + str(total_sourceforge_count))
print("GitHub count: " + str(total_github_count))
print("GitLab count: " + str(total_gitlab_count))
print("Bitbucket count: " + str(total_bitbucket_count))
csv_file.close()
csv_file2.close()