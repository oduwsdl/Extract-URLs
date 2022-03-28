from surt import surt 
import csv
import re

surt_file = open("./repo_results/github_surt.csv", "w")
surt_csv = csv.writer(surt_file, delimiter=' ', escapechar='\\', quoting=csv.QUOTE_NONE)

memento_file = open('./acorns/mementos.csv', 'w')
memento_csv = csv.writer(memento_file, delimiter=' ')
memento_csv.writerow(['URL', 'SURT', 'Directory', 'File'])

save_file = open('./acorns/archive_save.csv', 'w')
save_csv = csv.writer(save_file, delimiter=' ')
save_csv.writerow(['URL', 'SURT', 'Directory', 'File'])

gist_file = open('./acorns/gist_urls.csv', 'w')
gist_csv = csv.writer(gist_file, delimiter=' ')
gist_csv.writerow(['URL', 'SURT', 'Directory', 'File'])

io_file = open('./acorns/github_io.csv', 'w')
io_csv = csv.writer(io_file, delimiter=' ')
io_csv.writerow(['URL', 'SURT', 'Directory', 'File'])

not_gh_file = open('./acorns/not_really_github.csv', 'w')
not_gh_csv = csv.writer(not_gh_file, delimiter=' ')
not_gh_csv.writerow(['URL', 'SURT', 'Directory', 'File'])

with open('repo_results/github.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        s = surt(row[0].strip())

        if re.match(r'com,github,gist', s):
            gist_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip()])
        elif re.match(r'org,archive,web\)\/save\/', s):
            save_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip()])
        elif re.match(r'org,archive,web\)\/web\/', s):
            memento_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip()])
        elif re.match(r'io,github', s):
            io_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip()])
        elif not re.match(r'^com,github\)', s):
            not_gh_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip()])
        elif s != "com,github)/":
            surt_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip()])

memento_file.close()
save_file.close()
gist_file.close()
io_file.close()
not_gh_file.close()
surt_file.close()