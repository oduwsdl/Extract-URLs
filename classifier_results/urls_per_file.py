# Input: class_repo_urls.json
# Output: class_urls_per_file.csv (directory, average # of URLs per file, category)
# Notes: Similar to dir_urls.py but generates the average # of URLs per file instead of total

import json
import csv

corpora = ["class"]
for corpus in corpora:
    if corpus == 'arxiv':
        prefix = ""
    else:
        prefix = corpus + "_"
    repo_file = open("./repo_results/" + prefix + "repo_urls.json")
    repo_json = json.load(repo_file)
    repo_file.close()

    csv_file = open("./classifier_results/" + prefix + "urls_per_file.csv", "w")
    csvwriter = csv.writer(csv_file)
    csvwriter.writerow(['Directory', 'URICount', 'Category', 'TotalURIs'])

    total_file_count = 0
    total_url_count = 0
    total_sourceforge_count = 0
    total_github_count = 0
    total_gitlab_count = 0
    total_bitbucket_count = 0
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
        elif corpus == "etd":
            date = dir[0:4] + "-" + dir[4:]
            dir_file = open("raw_data_outputs/" + prefix + "parsed/" + dir + ".json")
        elif corpus == "class_pmc":
            date = dir[0:4] + "-" + dir[4:]
            dir_file = open("raw_data_outputs/classifier_pmc_parsed/" + dir + ".json")

        dir_json = json.load(dir_file)
        dir_file.close()

        sourceforge_count = repo_json[dir]["sourceforge"]["url_count"]
        sourceforge_oads_count = len(repo_json[dir]["sourceforge"]["oads_urls"])
        sourceforge_non_count = sourceforge_count - sourceforge_oads_count

        github_count = repo_json[dir]["github"]["url_count"]
        github_oads_count = len(repo_json[dir]["github"]["oads_urls"])
        github_non_count = github_count - github_oads_count

        gitlab_count = repo_json[dir]["gitlab"]["url_count"]
        gitlab_oads_count = len(repo_json[dir]["gitlab"]["oads_urls"])
        gitlab_non_count = gitlab_count - gitlab_oads_count

        bitbucket_count = repo_json[dir]["bitbucket"]["url_count"]
        bitbucket_oads_count = len(repo_json[dir]["bitbucket"]["oads_urls"])
        bitbucket_non_count = bitbucket_count - bitbucket_oads_count

        total_sourceforge_count = total_sourceforge_count + sourceforge_count
        total_github_count = total_github_count + github_count
        total_gitlab_count = total_gitlab_count + gitlab_count
        total_bitbucket_count = total_bitbucket_count + bitbucket_count

        dir_count = 0
        file_count = 0
        oads_count = 0
        non_count = 0
        for file in dir_json[dir]["files"]:
            file_count = file_count + 1
            url_count = dir_json[dir]["files"][file]["url_count"]
            dir_count = dir_count + url_count
            file_oads_count = dir_json[dir]["files"][file]["oads_count"]
            non_count = non_count + url_count - file_oads_count
            oads_count = oads_count + file_oads_count
        total_file_count = total_file_count + file_count
        total_url_count = total_url_count + dir_count

        oads_count = oads_count - sourceforge_oads_count - bitbucket_oads_count - github_oads_count - gitlab_oads_count
        non_count = non_count - sourceforge_non_count - bitbucket_non_count - github_non_count - gitlab_non_count

        csvwriter.writerow([date, dir_count, "Total", dir_count])
        csvwriter.writerow([date, oads_count, "OADS", dir_count])
        csvwriter.writerow([date, non_count, "NonOADS", dir_count])
        csvwriter.writerow([date, (sourceforge_oads_count + sourceforge_non_count), "SourceForge", dir_count])
        csvwriter.writerow([date, (github_oads_count + github_non_count), "GitHub", dir_count])
        csvwriter.writerow([date, (gitlab_oads_count + gitlab_non_count), "GitLab", dir_count])
        csvwriter.writerow([date, (bitbucket_oads_count + bitbucket_non_count), "Bitbucket", dir_count])
    print("Total file count: " + str(total_file_count))
    print("Total URL count: " + str(total_url_count))
    print("SourceForge count: " + str(total_sourceforge_count))
    print("GitHub count: " + str(total_github_count))
    print("GitLab count: " + str(total_gitlab_count))
    print("Bitbucket count: " + str(total_bitbucket_count))
    csv_file.close()