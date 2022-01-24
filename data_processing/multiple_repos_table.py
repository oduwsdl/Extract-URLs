# Input: multiple_repos.csv
# Output: multiple_repos_table.csv (filename, counts for each repo)
# Notes: Table is only for files that reference more than one platform

import csv

def reset():
    return "", "", "", ""

csv_file = open("multiple_repos_table.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['Filename', 'Bitbucket', 'GitHub', 'GitLab', 'SourceForge'])

with open('multiple_repos.csv') as read_csv:
    csv_reader = csv.reader(read_csv, delimiter=',')
    line_count = 0
    prev_file = ""
    gh, gl, bb, sf = reset()
    for row in csv_reader:
        if line_count == 0:
            prev_file = row[0]
            if row[2] == "GitHub":
                gh = row[1]
            elif row[2] == "GitLab":
                gl = row[1]
            elif row[2] == "Bitbucket":
                bb = row[1]
            elif row[2] == "SourceForge":
                sf = row[1]
            line_count += 1
        else:
            curr_file = row[0]
            if curr_file != prev_file:
                csvwriter.writerow([prev_file, bb, gh, gl, sf])
                prev_file = curr_file
                gh, gl, bb, sf = reset()
            if row[2] == "GitHub":
                gh = row[1]
            elif row[2] == "GitLab":
                gl = row[1]
            elif row[2] == "Bitbucket":
                bb = row[1]
            elif row[2] == "SourceForge":
                sf = row[1]
            line_count += 1

