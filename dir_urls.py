import json
import csv

repo_file = open("repo_results/repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

csv_file = open("urls.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['Directory', 'TotalURLS', 'SourceForgeURLS', 'GitHubURLs', 'GitLabURLs', 'BitbucketURLs'])

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
    csvwriter.writerow([dir, dir_count, sourceforge_count, github_count, gitlab_count, bitbucket_count])
csv_file.close()