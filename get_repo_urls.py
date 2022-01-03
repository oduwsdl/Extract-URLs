import json
import os
import re

sourceforge = open("repo_results/sourceforge.csv", "w")
github = open("repo_results/github.csv", "w")
gitlab = open("repo_results/gitlab.csv", "w")
bitbucket = open("repo_results/bitbucket.csv", "w")
repos = open("repo_results/repo_urls.json", "w")

# authors = open("~/authors-parsed.json")
# authors_json = json.load(authors)

def url_union(repo_dict):
    repo_all = list(set(repo_dict["annot_urls"]).union(set(repo_dict["text_urls"])))
    return repo_all

def update_dict(dir_dict, repo_all, repo_dict):
    repo_dict["all_urls"] = repo_all
    repo_dict["url_count"] = len(repo_all)
    dir_dict["annot_urls"].extend(repo_dict["annot_urls"])
    dir_dict["text_urls"].extend(repo_dict["text_urls"])
    dir_dict["all_urls"].extend(repo_all)
    dir_dict["url_count"] = dir_dict["url_count"] + len(repo_all)

data = {}
all_files = 0

file_list = os.listdir("parsed/")
for file_name in file_list:
    dir = re.findall(r"(\d{4}).json", file_name)[0]
    data[dir] = {"files":{}}
    f = open("parsed/" + file_name, "r")
    json_data = json.load(f)
    dir_sourceforge_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    dir_github_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    dir_gitlab_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
    dir_bitbucket_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}

    for pdf_name in json_data[dir]["files"]:
        all_files = all_files + 1
        annot_urls = json_data[dir]["files"][pdf_name]["annot_urls"]
        text_urls = json_data[dir]["files"][pdf_name]["text_urls"]
        sourceforge_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
        github_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
        gitlab_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
        bitbucket_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
        for url in annot_urls:
            sf = re.search(r"(sourceforge.net)", url)
            if sf is not None:
                sourceforge_dict["annot_urls"].append(url)
                sourceforge.write(url + ", " + dir + ", " + pdf_name + "\n")

            gh = re.search(r"(github.com|github.io)", url)
            if gh is not None:
                github_dict["annot_urls"].append(url)
                github.write(url + ", " + dir + ", " + pdf_name + "\n")
            
            gl = re.search(r"(gitlab.com|gitlab.io)", url)
            if gl is not None:
                gitlab_dict["annot_urls"].append(url)
                gitlab.write(url + ", " + dir + ", " + pdf_name + "\n")
            
            bb = re.search(r"(bitbucket.org)", url)
            if bb is not None:
                bitbucket_dict["annot_urls"].append(url)
                bitbucket.write(url + ", " + dir + ", " + pdf_name + "\n")
        
        for url in text_urls:
            sf = re.search(r"(sourceforge.net)", url)
            if sf is not None:
                sourceforge_dict["text_urls"].append(url)
                sourceforge.write(url + ", " + dir + ", " + pdf_name + "\n")

            gh = re.search(r"(github.com|github.io)", url)
            if gh is not None:
                github_dict["text_urls"].append(url)
                github.write(url + ", " + dir + ", " + pdf_name + "\n")
            
            gl = re.search(r"(gitlab.com|gitlab.io)", url)
            if gl is not None:
                gitlab_dict["text_urls"].append(url)
                gitlab.write(url + ", " + dir + ", " + pdf_name + "\n")
            
            bb = re.search(r"(bitbucket.org)", url)
            if bb is not None:
                bitbucket_dict["text_urls"].append(url)
                bitbucket.write(url + ", " + dir + ", " + pdf_name + "\n")
        
        sourceforge_all = url_union(sourceforge_dict)
        github_all = url_union(github_dict)
        gitlab_all = url_union(gitlab_dict)
        bitbucket_all = url_union(bitbucket_dict)

        if len(sourceforge_all) + len(github_all) + len(gitlab_all) + len(bitbucket_all) != 0:
            data[dir]["files"][pdf_name] = {}
        if len(sourceforge_all) != 0:
            update_dict(dir_sourceforge_dict, sourceforge_all, sourceforge_dict)
            data[dir]["files"][pdf_name]["sourceforge"] = sourceforge_dict
        if len(github_all) != 0:
            update_dict(dir_github_dict, github_all, github_dict)
            data[dir]["files"][pdf_name]["github"] = github_dict
        if len(gitlab_all) != 0:
            update_dict(dir_gitlab_dict, gitlab_all, gitlab_dict)
            data[dir]["files"][pdf_name]["gitlab"] = gitlab_dict
        if len(bitbucket_all) != 0:
            update_dict(dir_bitbucket_dict, bitbucket_all, bitbucket_dict)
            data[dir]["files"][pdf_name]["bitbucket"] = bitbucket_dict
    data[dir]["sourceforge"] = dir_sourceforge_dict
    data[dir]["github"] = dir_github_dict
    data[dir]["gitlab"] = dir_gitlab_dict
    data[dir]["bitbucket"] = dir_bitbucket_dict

json.dump(data, repos)
repos.close()
sourceforge.close()
github.close()
gitlab.close()
bitbucket.close()

print("Total number of files: " + str(all_files))