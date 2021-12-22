import json
import csv

repo_file = open("./repo_results/repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

csv_file = open("file_url_counts.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['Filename', 'URLCount', 'Category'])

for dir in repo_json:
    for file in repo_json[dir]["files"]:
        try:
            sourceforge_count = repo_json[dir]["files"][file]["sourceforge"]["url_count"]
            csvwriter.writerow([file, sourceforge_count, "SourceForge"])
        except:
            pass
        try:
            github_count = repo_json[dir]["files"][file]["github"]["url_count"]
            csvwriter.writerow([file, github_count, "GitHub"])
        except:
            pass
        try:
            gitlab_count = repo_json[dir]["files"][file]["gitlab"]["url_count"]
            csvwriter.writerow([file, gitlab_count, "GitLab"])
        except:
            pass
        try:
            bitbucket_count = repo_json[dir]["files"][file]["bitbucket"]["url_count"]
            csvwriter.writerow([file, bitbucket_count, "Bitbucket"])
        except:
            pass
csv_file.close()