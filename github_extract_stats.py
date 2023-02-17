import csv
import json
import re

input_file = './github_api/dedupe_gh_api_output.csv'
output_file = './github_api/gh_extracted_stats.csv'

gh_results_file = open(output_file, 'w')
gh_results_csv = csv.writer(gh_results_file, delimiter=',')
gh_results_csv.writerow(['URL', 'Error', 'Forks', 'Subscribers', 'Stargazers'])

with open(input_file, newline='') as gh_api_results_file:
    gh_api_results = csv.reader(gh_api_results_file, delimiter=',')
    for row in gh_api_results:
        url = row[0]
        response_file = row[2]
        try: 
            f = open(response_file, 'r')
        except:
            continue

        file_string = f.read()
        
        try:
            data = json.load(f)
        except:
            found_json = False
            sections = re.findall(r'((?:[^\n\r](\n )?)+)', file_string)
            for s in sections:
                if '{' in s[0][0:4] and found_json != True:
                    data = json.loads(s[0])
                    found_json = True
        try: 
            gh_results_csv.writerow([url, 'No', data['forks_count'], data['subscribers_count'], data['stargazers_count']])
        except: 
            gh_results_csv.writerow([url, 'Yes', 0, 0, 0])

gh_results_file.close()
f.close()