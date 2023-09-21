from surt import surt 
import csv

# s = surt(url.strip())

input_file = "curl/curl_results.csv"
output_file = "curl/curl_results_surt.csv"

surt_csv = open(output_file, "w")
surt_writer = csv.writer(surt_csv, delimiter=" ")
surt_writer.writerow(['URL', 'GHP', 'RepoURL', 'SURT', 'File', 'Location', 'HTTPStatus'])

curl_csv = open(input_file, newline='')
curl_reader = csv.reader(curl_csv, delimiter=',')
next(curl_reader)
for row in curl_reader:
    url = row[0]
    ghp = row[1]
    repo_url = row[2]
    if ghp == "GitHub" or ghp == "GitLab" or ghp == "Bitbucket":
        s = surt(repo_url.strip())
    elif ghp == "SourceForge":
        s = surt(url.strip())
    else:
        s = ""
    surt_writer.writerow([url, ghp, repo_url, s, row[3], row[4], row[5]])
curl_csv.close()
surt_csv.close()
    