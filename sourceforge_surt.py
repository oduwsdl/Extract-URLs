from surt import surt 
import csv
import re

surt_file = open("./repo_results/sourceforge_surt.csv", "w")
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

# io_file = open('./acorns/sourceforge_io.csv', 'w')
# io_csv = csv.writer(io_file, delimiter=' ')
# io_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

# not_sf_file = open('./acorns/not_really_sourceforge.csv', 'w')
# not_sf_csv = csv.writer(not_sf_file, delimiter=' ')
# not_sf_csv.writerow(['URL', 'SURT', 'Directory', 'File', 'Repo', 'Corpus'])

with open('repo_results/sourceforge.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        if re.match(r'https:\/\/\w*.sourceforge.net', row[0]):
            url = row[0].replace('https', 'http')
        else: 
            url = row[0]
        s = surt(url.strip())

        # if re.match(r'com,sourceforge,gist', s):
        #     gist_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'SourceForge'])
        # elif re.match(r'org,archive,web\)\/save\/', s):
        #     save_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'SourceForge'])
        # elif re.match(r'org,archive,web\)\/web\/', s):
        #     memento_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'SourceForge'])
        # elif re.match(r'io,sourceforge', s):
        #     io_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'SourceForge'])
        # elif not re.match(r'^com,sourceforge\)', s):
        #     not_sf_csv.writerow([s, row[0].strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'SourceForge'])
        if s != "net,sourceforge)/":
            surt_csv.writerow([s, url.strip(), '20' + row[1].strip(), row[2].strip(), 'arXiv', 'SourceForge'])

with open('repo_results/pmc_sourceforge.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        if re.match(r'https:\/\/\w*.sourceforge.net', row[0]):
            url = row[0].replace('https', 'http')
        else: 
            url = row[0]
        s = surt(url.strip())

        # if re.match(r'com,sourceforge,gist', s):
        #     gist_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'SourceForge'])
        # elif re.match(r'org,archive,web\)\/save\/', s):
        #     save_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'SourceForge'])
        # elif re.match(r'org,archive,web\)\/web\/', s):
        #     memento_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'SourceForge'])
        # elif re.match(r'io,sourceforge', s):
        #     io_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'SourceForge'])
        # elif not re.match(r'^com,sourceforge\)', s):
        #     not_sf_csv.writerow([s, row[0].strip(), row[1].strip(), row[2].strip(), 'PMC', 'SourceForge'])
        if s != "net,sourceforge)/":
            surt_csv.writerow([s, url.strip(), row[1].strip(), row[2].strip(), 'PMC', 'SourceForge'])

# memento_file.close()
# save_file.close()
# gist_file.close()
# io_file.close()
# not_sf_file.close()
surt_file.close()