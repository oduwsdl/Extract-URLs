# Input: list of all SourceForge URIs (repo_results/sourceforge.csv)
# Output: swh/sf_projects.csv, file of all SF URIs and their associated project names
# Note: extracts the project name from the SourceForge URIs

import re
import csv

sf_csv = open('repo_results/sourceforge.csv', newline='')
sf_reader = csv.reader(sf_csv, delimiter=' ')
project_file = open("swh/sf_projects.csv", "w")
project_csv = csv.writer(project_file, delimiter=" ")
project_csv.writerow(['ProjectName', 'PublicationURI'])
for row in sf_reader:
    url = row[0]
    project = ""
    result = re.match(r'(http|https):\/\/(www.|)sourceforge.net\/(projects|p|project)\/([^\/(\.)][a-zA-Z0-9-‑_]+)', url)
    if result != None and result != "": 
        project = result[4]
    else: 
        result = re.match(r'(http|https):\/\/(www.|)([^\/(\.)][a-zA-Z0-9-‑_]+).(git.sourceforge|svn.sourceforge|sourceforge).net', url)
        if result != None and result != "":
            project = result[3]
    if project != 'www' and project != "":
        project_csv.writerow([project, url])
    else:
        print(url + " " + project)
sf_csv.close()
project_file.close()