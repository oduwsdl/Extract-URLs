import json
import csv

repo_file = open("repo_results/repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

csv_file = open("urls.csv", "w")
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
    for file in dir_json[dir]["files"]:
        dir_count = dir_count + dir_json[dir]["files"][file]["url_count"]

    csvwriter.writerow([dir, dir_count, "Total"])
    csvwriter.writerow([dir, sourceforge_count, "SourceForge"])
    csvwriter.writerow([dir, github_count, "GitHub"])
    csvwriter.writerow([dir, gitlab_count, "GitLab"])
    csvwriter.writerow([dir, bitbucket_count, "Bitbucket"])
csv_file.close()