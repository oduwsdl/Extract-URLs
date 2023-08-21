# Input: swh/sf_repo_uris.csv
# Output: swh/sf_project_uris.csv (is this specific repo URI in SWH?) and swh/sf_swh_results.csv (is at least 1 repo URI in SWH?)
# Notes: calls swh_sf_api_scrape.sh, checks SWH for each repo URI and variation to determine if the repo is ever captured by SWH

import csv
import subprocess
import sys

def get_variations(uri):
    uri_path = uri.split('/')
    i = len(uri_path) - 1 # index of the last element of the array
    while i >= 0:
        if uri_path[i] == "code" or uri_path[i] == "svn":
            break
        i = i - 1
    # if i == -1, 'code' and 'svn' weren't found so the whole uri is returned
    if i == -1:
        output = '/'.join(uri_path)
    # otherwise, the uri up to i+1 (including 'code' or 'svn') is returned
    else:
        output = '/'.join(uri_path[:i+1])
    return output

def add_uris(row, uris_to_process):
    code = row[2]
    if code == "Yes":
        http_uri = row[4].rstrip('/')
        other_uri = row[5].rstrip('/')
        if http_uri != "None":
            uris_to_process.add(http_uri)
            uris_to_process.add(get_variations(http_uri))
        if other_uri != []:
            uris_to_process.add(other_uri)
            uris_to_process.add(get_variations(other_uri))

def run_uris(project_name, uris_to_process, scrape_data):
    code = "No"
    in_swh = "No"
    if len(uris_to_process) != 0:
        code = "Yes"
        for uri in uris_to_process:
            file = 'sourceforge-' + project_name + '.txt'
            output = subprocess.check_output('./swh_sf_api_scrape.sh https://archive.softwareheritage.org/api/1/origin/' + uri + '/visits/ ' + scrape_data['rate_limit_reset'] + ' ' + scrape_data['rate_limit_remaining'] + ' ../raw_data_outputs/swh_sf_headers/' + file + ' ../raw_data_outputs/swh_sf_response/' + file + ' ' + scrape_data['auth_token'], shell=True, text=True).strip().split()
            http_code = output[0]
            try: 
                scrape_data['rate_limit_reset'] = output[1]
                scrape_data['rate_limit_remaining'] = output[2]
            except: 
                scrape_data['rate_limit_reset'] = '0'
                scrape_data['rate_limit_remaining'] = '1'
            if http_code == "200":
                in_swh = "Yes"
                uri_data_csv.writerow([project_name, uri, 'Yes'])
            else:
                uri_data_csv.writerow([project_name, uri, 'No'])
        output = [project_name, "SourceForge", 'raw_data_outputs/swh_sf_headers/' + file, 'raw_data_outputs/swh_sf_response/' + file, code, in_swh]
    else:
        output = [project_name, "SourceForge", " ", " ", code, in_swh]
    return output

sf_stats = {'incorrect_url': 0, 'correct_url': 0, 'missing_swh': 0, 'found_swh': 0}
scrape_data = {'rate_limit_remaining': '1', 'rate_limit_reset': '0', 'auth_token': sys.argv[1]}

input_file = 'sf_repo_uris.csv'
output_file = 'sf_swh_results.csv'
uri_data_file = 'sf_project_uris.csv'

swh_results_file = open(output_file, "w")
swh_results_csv = csv.writer(swh_results_file, delimiter=',')
swh_results_csv.writerow(['ProjectName', 'GHP', 'HeaderFile', 'ResponseFile', 'CorrectURL?', 'InSWH?'])

uri_data = open(uri_data_file, "w")
uri_data_csv = csv.writer(uri_data, delimiter=",")
uri_data_csv.writerow(['ProjectName', 'URI', 'InSWH?'])

sf_csv = open(input_file, newline='')
sf_reader = csv.reader(sf_csv, delimiter=' ')
prev_project_name = ""
uris_to_process = set(())
next(sf_reader)
for row in sf_reader:
    project_name = row[0]
    ghp = "SoureForge"

    if prev_project_name == "":
        # add uris to the set
        add_uris(row, uris_to_process)
        prev_project_name = project_name
    else:
        if project_name == prev_project_name:
            # add uris to the set
            add_uris(row, uris_to_process)
        else:
            # run uris in the set
            output = run_uris(prev_project_name, uris_to_process, scrape_data)
            code = output[4]
            in_swh = output[5]
            if code == "Yes":
                sf_stats['correct_url'] += 1
                if in_swh == "Yes":
                    sf_stats['found_swh'] += 1
                else:
                    sf_stats['missing_swh'] += 1
            else:
                sf_stats['incorrect_url'] += 1
            swh_results_csv.writerow(output)
            # start a new set of uris with the current project
            uris_to_process.clear()
            add_uris(row, uris_to_process)
            prev_project_name = project_name

output = run_uris(prev_project_name, uris_to_process, scrape_data)
code = output[4]
in_swh = output[5]
if code == "Yes":
    sf_stats['correct_url'] += 1
    if in_swh == "Yes":
        sf_stats['found_swh'] += 1
    else:
        sf_stats['missing_swh'] += 1
else:
    sf_stats['incorrect_url'] += 1
swh_results_csv.writerow(output)

swh_results_file.close()

print(sf_stats)
