# Input: swh/sorted_sf_projects.csv (sorted version of sf_projects.csv from run_sf_in_swh.sh)
# Output: swh/sf_api_output.jsonl
# Notes: uses the project name for each URI to ping the SF API and write the results to the output file

import csv
import urllib.request
import jsonlines
import json
import time

project_csv = open('swh/sorted_sf_projects.csv', newline='')
project_reader = csv.reader(project_csv, delimiter=' ')
d = open('swh/sf_api_output.jsonl', 'w')
jsonl_writer = jsonlines.Writer(d)
prev_project = ""
for row in project_reader:
    project = row[0]
    if prev_project != project:
        api_url = "https://sourceforge.net/rest/p/" + project + "/"
        time.sleep(1)
        req = urllib.request.Request(api_url)
        try:
            response = urllib.request.urlopen(req)
            output = json.loads(response.read().decode('utf-8'))
            jsonl_writer.write(output)
        except Exception as error:
            print(project + " " + str(error))
            output = {"project": project, "url": api_url, "status": "rotten"}
            jsonl_writer.write(output)
        prev_project = project
jsonl_writer.close()