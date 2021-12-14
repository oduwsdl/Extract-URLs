import json
import csv

repo_file = open("repo_results/repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

csv_file = open("repo_url_counts.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['Directory', 'URLCount', 'Category'])

for dir in repo_json:
    sourceforge_count = repo_json[dir]["sourceforge"]["url_count"]
    github_count = repo_json[dir]["github"]["url_count"]
    gitlab_count = repo_json[dir]["gitlab"]["url_count"]
    bitbucket_count = repo_json[dir]["bitbucket"]["url_count"]
    dir_file = open("parsed/" + dir + ".json")
    dir_json = json.load(dir_file)
    dir_file.close()
    dir_count = 0
    file_count = 0
    for file in dir_json[dir]["files"]:
        file_count = file_count + 1

    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], sourceforge_count, "SourceForge"])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], github_count, "GitHub"])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], gitlab_count, "GitLab"])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], bitbucket_count, "Bitbucket"])
csv_file.close()