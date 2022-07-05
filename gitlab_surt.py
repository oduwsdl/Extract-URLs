from surt import surt 
import csv
import re

surt_file = open("./repo_results/gitlab_surt.csv", "w")
surt_csv = csv.writer(surt_file, delimiter=' ', escapechar='\\', quoting=csv.QUOTE_NONE)

# memento_file = open('./acorns/mementos.csv', 'w')
# memento_csv = csv.writer(memento_file, delimiter=' ')
# memento_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

# save_file = open('./acorns/archive_save.csv', 'w')
# save_csv = csv.writer(save_file, delimiter=' ')
# save_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

# gist_file = open('./acorns/gist_urls.csv', 'w')
# gist_csv = csv.writer(gist_file, delimiter=' ')
# gist_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

io_file = open('./acorns/gitlab_io.csv', 'w')
io_csv = csv.writer(io_file, delimiter=' ')
io_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

not_gl_file = open('./acorns/not_really_gitlab.csv', 'w')
not_gl_csv = csv.writer(not_gl_file, delimiter=' ')
not_gl_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

with open('repo_results/gitlab.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        s = surt(row[0].strip())

        # if re.match(r'com,gitlab,gist', s):
        #     gist_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'GitLab'])
        # elif re.match(r'org,archive,web\)\/save\/', s):
        #     save_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'GitLab'])
        # elif re.match(r'org,archive,web\)\/web\/', s):
        #     memento_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'GitLab'])
        if re.match(r'io,gitlab', s):
            io_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'GitLab'])
        elif not re.match(r'^com,gitlab\)', s):
            not_gl_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'GitLab'])
        elif s != "com,gitlab)/":
            surt_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'GitLab'])

with open('repo_results/pmc_gitlab.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        s = surt(row[0].strip())

        # if re.match(r'com,gitlab,gist', s):
        #     gist_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'GitLab'])
        # elif re.match(r'org,archive,web\)\/save\/', s):
        #     save_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'GitLab'])
        # elif re.match(r'org,archive,web\)\/web\/', s):
        #     memento_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'GitLab'])
        if re.match(r'io,gitlab', s):
            io_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'GitLab'])
        elif not re.match(r'^com,gitlab\)', s):
            not_gl_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'GitLab'])
        elif s != "com,gitlab)/":
            surt_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'GitLab'])

# memento_file.close()
# save_file.close()
# gist_file.close()
io_file.close()
not_gl_file.close()
surt_file.close()