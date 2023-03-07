# Input: swh/dedupe_swh_results.csv
# Output: github_api/gh_api_output.csv, raw_data_outputs/gh_headers/, raw_data_outputs/gh_response/

import csv
import subprocess
import re
import sys

auth_token = sys.argv[1]

rate_limit_remaining = '1'
rate_limit_reset = '0'

input_file = "./swh/dedupe_swh_results.csv"
output_file = "./github_api/gh_api_output.csv"

gh_results_file = open(output_file, "a")
gh_results_csv = csv.writer(gh_results_file, delimiter=',')

with open(input_file, newline='') as swh_results_file:
    swh_results = csv.reader(swh_results_file, delimiter=',')
    next(swh_results)
    for row in swh_results:
        ghp = row[2]
        correct_url = row[5]
        if ghp == "GitHub" and correct_url == "Yes":
            url = row[1].lower()
            re_output = re.match(r'(http|https|git):\/\/(www.|)github.com\/([^\/]+)\/([^\/(\.)][a-zA-Z0-9-_]+)', url)
            username = re_output[3]
            repo = re_output[4]
            file = 'github-' + username + '-' + repo + '.txt'
            api_url = 'https://api.github.com/repos/' + username + '/' + repo
            output = subprocess.check_output('./gh_api_scrape.sh ' + api_url + ' ' + rate_limit_reset + ' ' + rate_limit_remaining + ' raw_data_outputs/gh_headers/' + file + ' raw_data_outputs/gh_response/' + file + ' ' + auth_token, shell=True, text=True).strip().split()
            try: 
                if output[0] != "Repeat":
                    rate_limit_reset = output[0]
                    rate_limit_remaining = output[1]
            except: 
                rate_limit_reset = '0'
                rate_limit_remaining = '1'
            gh_results_csv.writerow([url, 'raw_data_outputs/gh_headers/' + file, 'raw_data_outputs/gh_response/' + file])

gh_results_file.close()