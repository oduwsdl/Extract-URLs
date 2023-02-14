import csv
import json

input_file = './github_api/dedupe_gh_api_output.csv'
output_file = './github_api/gh_extracted_stats.csv'

gh_results_file = open(output_file, 'a')
gh_results_csv = csv.writer(gh_results_file, delimiter=',')
gh_results_csv.writerow(['URL', 'Error', 'Forks', 'Subscribers', 'Stargazers'])

with open(input_file, newline='') as gh_api_results_file:
    gh_api_results = csv.reader(gh_api_results_file, delimiter=',')
    for row in gh_api_results:
        url = row[0]
        response_file = row[2]
        try:
            f = open(response_file)
            data = json.load(f)
            try: 
                gh_results_csv.writerow([url, 'No', data['forks_count'], data['subscribers_count'], data['stargazers_count']])
            except: 
                gh_results_csv.writerow([url, 'Yes', 0, 0, 0])
        except:
            pass

gh_results_file.close()