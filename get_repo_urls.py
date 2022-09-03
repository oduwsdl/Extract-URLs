# Input: parsed/ and pmc_parsed/
# Output: CSV for each platform (with the URL, dir, and file name) and corpus; [pmc_]all_file_urls.json (with all files regardless of platform URLs)
# Notes: Also created [pmc_]repo_urls.json with only files that contain a platform URL

import json
import os
import re
import csv
from surt import surt

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
    return repo_dict

sf_surt_file = open("./repo_results/sourceforge_surt.csv", "w")
sf_surt_csv = csv.writer(sf_surt_file, delimiter=' ', escapechar='\\', quoting=csv.QUOTE_NONE)

not_sf_file = open('./acorns/not_really_sourceforge.csv', 'w')
not_sf_csv = csv.writer(not_sf_file, delimiter=' ')
not_sf_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

gh_surt_file = open("./repo_results/github_surt.csv", "w")
gh_surt_csv = csv.writer(gh_surt_file, delimiter=' ', escapechar='\\', quoting=csv.QUOTE_NONE)

memento_file = open('./acorns/mementos.csv', 'w')
memento_csv = csv.writer(memento_file, delimiter=' ')
memento_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

save_file = open('./acorns/archive_save.csv', 'w')
save_csv = csv.writer(save_file, delimiter=' ')
save_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

gist_file = open('./acorns/gist_urls.csv', 'w')
gist_csv = csv.writer(gist_file, delimiter=' ')
gist_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

gh_io_file = open('./acorns/github_io.csv', 'w')
gh_io_csv = csv.writer(gh_io_file, delimiter=' ')
gh_io_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

not_gh_file = open('./acorns/not_really_github.csv', 'w')
not_gh_csv = csv.writer(not_gh_file, delimiter=' ')
not_gh_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

gl_surt_file = open("./repo_results/gitlab_surt.csv", "w")
gl_surt_csv = csv.writer(gl_surt_file, delimiter=' ', escapechar='\\', quoting=csv.QUOTE_NONE)

gl_io_file = open('./acorns/gitlab_io.csv', 'w')
gl_io_csv = csv.writer(gl_io_file, delimiter=' ')
gl_io_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

not_gl_file = open('./acorns/not_really_gitlab.csv', 'w')
not_gl_csv = csv.writer(not_gl_file, delimiter=' ')
not_gl_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

bb_surt_file = open("./repo_results/bitbucket_surt.csv", "w")
bb_surt_csv = csv.writer(bb_surt_file, delimiter=' ', escapechar='\\', quoting=csv.QUOTE_NONE)

bb_io_file = open('./acorns/bitbucket_io.csv', 'w')
bb_io_csv = csv.writer(bb_io_file, delimiter=' ')
bb_io_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

not_bb_file = open('./acorns/not_really_bitbucket.csv', 'w')
not_bb_csv = csv.writer(not_bb_file, delimiter=' ')
not_bb_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

gh_sitemap = ['github.com/join\?', 'github.com/login', 'github.com/pricing$', 'github.com/pricing/.*' 'github.com/git-guides$', 'github.com/git-guides/.*', 'github.com/team$', 'github.com/team/.*', 'github.com/marketplace$', 'github.com/marketplace/.*', 'github.com/enterprise$', 'github.com/enterprise/.*', 'github.com/features$', 'github.com/features/.*', 'github.com/readme$', 'github.com/readme/.*', 'github.com/about$', 'github.com/about/.*', 'github.com/learn$', 'github.com/learn/.*']
gl_sitemap = ['gitlab.com/users/sign_in$', 'gitlab.com/users/sign_in/.*', 'gitlab.com/users/sign_up$', 'gitlab.com/users/sign_up/.*', 'gitlab.com/explore$', 'gitlab.com/explore/.*', 'gitlab.com/help$', 'gitlab.com/help/.*']
sf_sitemap = ['sourceforge.net/create$', 'sourceforge.net/create/.*', 'sourceforge.net/about$', 'sourceforge.net/about/.*', 'sourceforge.net/top$', 'sourceforge.net/top/.*', 'sourceforge.net/user/newsletters$', 'sourceforge.net/user/newsletters/.*', 'sourceforge.net/user/registration$', 'sourceforge.net/user/registation/.*', 'sourceforge.net/user/registration_business$', 'sourceforge.net/user/registration_business/.*', 'sourceforge.net/software/vendors$', 'sourceforge.net/software/vendors/.*', 'sourceforge.net/software/reviews$', 'sourceforge.net/software/reviews/.*', 'sourceforge.net/p/forge$', 'sourceforge.net/p/forge/.*', 'sourceforge.net/p/add_project$', 'sourceforge.net/p/add_project/.*', 'sourceforge.net/auth$', 'sourceforge.net/auth/.*', 'sourceforge.net/directory$', 'sourceforge.net/directory/.*', 'sourceforge.net/software/?', 'sourceforge.net/blog$', 'sourceforge.net/blog/.*', 'sourceforge.net/about$', 'sourceforge.net/about/.*']
bb_sitemap = ['bitbucket.org/product$', 'bitbucket.org/product/.*', 'bitbucket.org/blog$', 'bitbucket.org/blog/.*']

corpora = ["pmc", "arxiv"]
for corpus in corpora:
    if corpus == "pmc":
        sourceforge = open("repo_results/pmc_sourceforge.csv", "w")
        github = open("repo_results/pmc_github.csv", "w")
        gitlab = open("repo_results/pmc_gitlab.csv", "w")
        bitbucket = open("repo_results/pmc_bitbucket.csv", "w")
        has_repo_json = open("repo_results/pmc_repo_urls.json", "w")
        all_files_json = open("repo_results/pmc_all_file_urls.json", "w")
        csv_file2 = open("./data_processing/pmc_file_count.csv", "w")
        csvwriter2 = csv.writer(csv_file2)
        csvwriter2.writerow(['Directory', 'FileCount', 'FileWithURL'])

        has_repo_data = {}
        all_files_data = {}
        total_all_files = 0
        total_url_files = 0

        file_list = os.listdir("pmc_parsed/")
    elif corpus == "arxiv":
        sourceforge = open("repo_results/sourceforge.csv", "w")
        github = open("repo_results/github.csv", "w")
        gitlab = open("repo_results/gitlab.csv", "w")
        bitbucket = open("repo_results/bitbucket.csv", "w")
        has_repo_json = open("repo_results/repo_urls.json", "w")
        all_files_json = open("repo_results/all_file_urls.json", "w")
        csv_file2 = open("./data_processing/file_count.csv", "w")
        csvwriter2 = csv.writer(csv_file2)
        csvwriter2.writerow(['Directory', 'FileCount', 'FileWithURL'])

        has_repo_data = {}
        all_files_data = {}
        total_all_files = 0
        total_url_files = 0

        file_list = os.listdir("parsed/")
    for file_name in file_list:
        if corpus == "pmc":
            dir = re.findall(r"(\d{6}).json", file_name)[0]
        elif corpus == "arxiv":
            dir = re.findall(r"(\d{4}).json", file_name)[0]
        has_repo_data[dir] = {"files":{}}
        all_files_data[dir] = {"files":{}}
        if corpus == "pmc":
            f = open("pmc_parsed/" + file_name, "r")
        elif corpus == "arxiv":
            f = open("parsed/" + file_name, "r")
        json_data = json.load(f)

        all_dir_sourceforge_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
        repo_dir_sourceforge_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
        all_dir_github_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
        repo_dir_github_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
        all_dir_gitlab_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
        repo_dir_gitlab_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
        all_dir_bitbucket_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}
        repo_dir_bitbucket_dict = {"url_count":0, "annot_urls":[], "text_urls":[], "all_urls":[]}

        all_files = 0
        url_files = 0
        for pdf_name in json_data[dir]["files"]:
            all_files = all_files + 1
            if json_data[dir]["files"][pdf_name]["url_count"] != 0:
                url_files = url_files + 1
            annot_urls = json_data[dir]["files"][pdf_name]["annot_urls"]
            text_urls = json_data[dir]["files"][pdf_name]["text_urls"]

            sourceforge_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
            github_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
            gitlab_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}
            bitbucket_dict = {"annot_urls":[], "text_urls":[], "all_urls":[]}

            for url in annot_urls:
                s = surt(url.strip())
                if len(dir) == 4:
                    d = "20" + dir
                elif len(dir) == 6:
                    d = dir
                sf = re.search(r"(sourceforge.net)", url)
                if sf is not None:
                    if re.search(r"(?=("+'|'.join(sf_sitemap)+r"))", url) is not None:
                        not_sf_csv.writerow([url, s, d, pdf_name, corpus, 'SourceForge'])
                    else:
                        sourceforge_dict["annot_urls"].append(url)
                        sourceforge.write(url + " " + s + " " + d + " " + pdf_name + "\n")
                        sf_surt_csv.writerow([url, s, d, pdf_name, corpus, 'SourceForge'])

                gh = re.search(r"(github.com|github.io)", url)
                if gh is not None:
                    if re.match(r'com,github,gist', url):
                        gist_csv.writerow([url, s, d, pdf_name, corpus, 'GitHub'])
                    elif re.match(r'org,archive,web\)\/save\/', url):
                        save_csv.writerow([url, s, d, pdf_name, corpus, 'GitHub'])
                    elif re.match(r'org,archive,web\)\/web\/', url):
                        memento_csv.writerow([url, s, d, pdf_name, corpus, 'GitHub'])
                    elif re.match(r'io,github', url):
                        gh_io_csv.writerow([url, s, d, pdf_name, corpus, 'GitHub'])
                    elif not re.match(r"^(https:\/\/w{0,3}.?github.com\/.+)", url) or re.search(r"(?=("+'|'.join(gh_sitemap)+r"))", url) is not None:
                        not_gh_csv.writerow([url, s, d, pdf_name, corpus, 'GitHub'])
                    else:
                        github_dict["annot_urls"].append(url)
                        github.write(url + " " + s + " " + d + " " + pdf_name + "\n")
                        gh_surt_csv.writerow([url, s, d, pdf_name, corpus, 'GitHub'])
                
                gl = re.search(r"(gitlab.com|gitlab.io)", url)
                if gl is not None:
                    if re.match(r'io,gitlab', s):
                        gl_io_csv.writerow([url, s, d, pdf_name, corpus, 'GitLab'])
                    elif not re.match(r"^(https:\/\/w{0,3}.?gitlab.com\/.+)", url) or re.search(r"(?=("+'|'.join(gl_sitemap)+r"))", url) is not None:
                        not_gl_csv.writerow([url, s, d, pdf_name, corpus, 'GitLab'])
                    else:
                        gitlab_dict["annot_urls"].append(url)
                        gitlab.write(url + " " + s + " " + d + " " + pdf_name + "\n")
                        gl_surt_csv.writerow([url, s, d, pdf_name, corpus, 'GitLab'])
                
                bb = re.search(r"(bitbucket.org|bitbucket.io)", url)
                if bb is not None:
                    # is it a link to a repo?
                    if not re.match(r"^https:\/\/(w{0,3}.?bitbucket.org\/.+|.*@bitbucket.org\/.+)", url) or re.search(r"(?=("+'|'.join(bb_sitemap)+r"))", url) is not None:
                        # is it a link to Bitbucket pages?
                        if re.match(r"^https:\/\/((?!www).*.?bitbucket.org|.*bitbucket.io)", url):
                            bb_io_csv.writerow([url, s, d, pdf_name, corpus, 'Bitbucket'])
                        else:
                            not_bb_csv.writerow([url, s, d, pdf_name, corpus, 'Bitbucket'])
                    else:
                        bitbucket_dict["annot_urls"].append(url)
                        bitbucket.write(url + " " + s + " " + d + " " + pdf_name + "\n")
                        bb_surt_csv.writerow([url, s, d, pdf_name, corpus, 'Bitbucket'])
            
            for url in text_urls:
                s = surt(url.strip())
                sf = re.search(r"(sourceforge.net)", url)
                if sf is not None:
                    sourceforge_dict["text_urls"].append(url)
                    sourceforge.write(url + " " + dir + " " + pdf_name + "\n")
                    sf_surt_csv.writerow([url, s, d, pdf_name, corpus, 'SourceForge'])

                gh = re.search(r"^(https:\/\/w{0,3}.?github.com\/.+)", url)
                if gh is not None:
                    github_dict["text_urls"].append(url)
                    github.write(url + " " + dir + " " + pdf_name + "\n")
                    gh_surt_csv.writerow([url, s, d, pdf_name, corpus, 'GitHub'])
                
                gl = re.search(r"^(https:\/\/w{0,3}.?gitlab.com\/.+)", url)
                if gl is not None:
                    gitlab_dict["text_urls"].append(url)
                    gitlab.write(url + " " + dir + " " + pdf_name + "\n")
                    gl_surt_csv.writerow([url, s, d, pdf_name, corpus, 'GitLab'])
                
                bb = re.search(r"^https:\/\/(w{0,3}.?bitbucket.org\/.+|.*@bitbucket.org\/.+)", url)
                if bb is not None:
                    bitbucket_dict["text_urls"].append(url)
                    bitbucket.write(url + " " + dir + " " + pdf_name + "\n")
                    bb_surt_csv.writerow([url, s, d, pdf_name, corpus, 'Bitbucket'])
            
            sourceforge_all = url_union(sourceforge_dict)
            github_all = url_union(github_dict)
            gitlab_all = url_union(gitlab_dict)
            bitbucket_all = url_union(bitbucket_dict)

            all_files_data[dir]["files"][pdf_name] = {}
            all_sourceforge_dict = update_dict(all_dir_sourceforge_dict, sourceforge_all, sourceforge_dict)
            all_files_data[dir]["files"][pdf_name]["sourceforge"] = all_sourceforge_dict
            all_github_dict = update_dict(all_dir_github_dict, github_all, github_dict)
            all_files_data[dir]["files"][pdf_name]["github"] = all_github_dict
            all_gitlab_dict = update_dict(all_dir_gitlab_dict, gitlab_all, gitlab_dict)
            all_files_data[dir]["files"][pdf_name]["gitlab"] = all_gitlab_dict
            all_bitbucket_dict = update_dict(all_dir_bitbucket_dict, bitbucket_all, bitbucket_dict)
            all_files_data[dir]["files"][pdf_name]["bitbucket"] = all_bitbucket_dict

            if len(sourceforge_all) + len(github_all) + len(gitlab_all) + len(bitbucket_all) != 0:
                has_repo_data[dir]["files"][pdf_name] = {}
                if len(sourceforge_all) != 0:
                    repo_sourceforge_dict = update_dict(repo_dir_sourceforge_dict, sourceforge_all, sourceforge_dict)
                    has_repo_data[dir]["files"][pdf_name]["sourceforge"] = repo_sourceforge_dict
                if len(github_all) != 0:
                    repo_github_dict = update_dict(repo_dir_github_dict, github_all, github_dict)
                    has_repo_data[dir]["files"][pdf_name]["github"] = repo_github_dict
                if len(gitlab_all) != 0:
                    repo_gitlab_dict = update_dict(repo_dir_gitlab_dict, gitlab_all, gitlab_dict)
                    has_repo_data[dir]["files"][pdf_name]["gitlab"] = repo_gitlab_dict
                if len(bitbucket_all) != 0:
                    repo_bitbucket_dict = update_dict(repo_dir_bitbucket_dict, bitbucket_all, bitbucket_dict)
                    has_repo_data[dir]["files"][pdf_name]["bitbucket"] = repo_bitbucket_dict
            
        all_files_data[dir]["sourceforge"] = all_dir_sourceforge_dict
        has_repo_data[dir]["sourceforge"] = repo_dir_sourceforge_dict
        all_files_data[dir]["github"] = all_dir_github_dict
        has_repo_data[dir]["github"] = repo_dir_github_dict
        all_files_data[dir]["gitlab"] = all_dir_gitlab_dict
        has_repo_data[dir]["gitlab"] = repo_dir_gitlab_dict
        all_files_data[dir]["bitbucket"] = all_dir_bitbucket_dict
        has_repo_data[dir]["bitbucket"] = repo_dir_bitbucket_dict
        csvwriter2.writerow([dir[0:4] + "-" + dir[4:], all_files, url_files])
        total_all_files = total_all_files + all_files
        total_url_files = total_url_files + url_files

    json.dump(all_files_data, all_files_json)
    json.dump(has_repo_data, has_repo_json)

    has_repo_json.close()
    all_files_json.close()
    sourceforge.close()
    github.close()
    gitlab.close()
    bitbucket.close()
    csv_file2.close()

    print("Total number of files: " + str(total_all_files) + " " + corpus)
    print("Files with URLs: " + str(total_url_files) + " " + corpus)

memento_file.close()
save_file.close()
not_sf_file.close()
sf_surt_file.close()
gist_file.close()
gh_io_file.close()
not_gh_file.close()
gh_surt_file.close()
gl_io_file.close()
not_gl_file.close()
gl_surt_file.close()
bb_io_file.close()
not_bb_file.close()
bb_surt_file.close()