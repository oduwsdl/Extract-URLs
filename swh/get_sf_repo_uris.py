# Input: swh/sf_api_output.jsonl
# Output: swh/sf_repo_uris.csv
# Notes: extracts the repo URIs from the SF API response to create an iterable CSV file

import csv
import jsonlines

output_file = open("swh/sf_repo_uris.csv", "w")
output_csv = csv.writer(output_file, delimiter=" ")
output_csv.writerow(['ProjectName', 'Status', 'Code', 'SCM', 'HTTPURL', 'RepoURL'])
status_404 = 0
status_active = 0
no_code = 0
yes_code = 0
git_scm = 0
svn_scm = 0
hg_scm = 0
with jsonlines.open('swh/sf_api_output.jsonl', 'r') as jsonl_f:
    for line in jsonl_f:
        status = line['status']
        code = "No"
        if status != "rotten":
            project_name = line['shortname']
            status_active = status_active + 1
            for tool in line['tools']:
                if tool['name'] == "svn":
                    scm = "SVN"
                    if 'clone_url_https_anon' in tool:
                        repo_url_http = tool['clone_url_https_anon']
                    else: 
                        repo_url_http = "None"
                    if 'clone_url_ro' in tool:
                        repo_url_other = tool['clone_url_ro']
                    else:
                        repo_url_other = "None"
                    if code == "No":
                        code = "Yes"
                        yes_code = yes_code + 1
                    svn_scm = svn_scm + 1
                    output = [project_name, status, code, scm, repo_url_http, repo_url_other]
                    output_csv.writerow(output)
                elif tool['name'] == "git":
                    scm = "Git"
                    if 'clone_url_https_anon' in tool:
                        repo_url_http = tool['clone_url_https_anon']
                    else: 
                        repo_url_http = "None"
                    if 'clone_url_ro' in tool:
                        repo_url_other = tool['clone_url_ro']
                    else:
                        repo_url_other = "None"
                    if code == "No":
                        code = "Yes"
                        yes_code = yes_code + 1
                    git_scm = git_scm + 1
                    output = [project_name, status, code, scm, repo_url_http, repo_url_other]
                    output_csv.writerow(output)
                elif tool['name'] == "hg":
                    scm = "Mercurial"
                    if 'clone_url_https_anon' in tool:
                        repo_url_http = tool['clone_url_https_anon']
                    else: 
                        repo_url_http = "None"
                    if 'clone_url_ro' in tool:
                        repo_url_other = tool['clone_url_ro']
                    else:
                        repo_url_other = "None"
                    if code == "No":
                        code = "Yes"
                        yes_code = yes_code + 1
                    hg_scm = hg_scm + 1
                    output = [project_name, status, code, scm, repo_url_http, repo_url_other]
                    output_csv.writerow(output)
            if code == "No":
                no_code = no_code + 1
                output_csv.writerow([project_name, status, code])
        else:
            project_name = line['project']
            status_404 = status_404 + 1
            output_csv.writerow([project_name, status, code])

output_file.close()

print("Status active: " + str(status_active))
print("Status 404: " + str(status_404))
print("Yes code: " + str(yes_code))
print("No code: " + str(no_code))
print("Git: " + str(git_scm))
print("SVN: " + str(svn_scm))
print("HG: " + str(hg_scm))
