from surt import surt 
import csv

input_file = "swh/sf_projects.csv"
output_file = "swh/sf_projects_surt.csv"

surt_csv = open(output_file, "w")
surt_writer = csv.writer(surt_csv, delimiter=" ")
surt_writer.writerow(['ProjectName', 'PublicationURI', 'SURT'])

swh_csv = open(input_file, newline='')
swh_reader = csv.reader(swh_csv, delimiter=' ')
next(swh_reader)
for row in swh_reader:
    url = row[1]
    s = surt(url.strip())
    surt_writer.writerow([row[0], url, s])
swh_csv.close()
surt_csv.close()
