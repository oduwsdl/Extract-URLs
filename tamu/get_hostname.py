import csv
from urllib.parse import urlparse
import tldextract

input_file_name = "tamu_urls.csv"
output_file_name = "tamu_hostnames.csv"

output_file = open(output_file_name, 'w')
output_csv = csv.writer(output_file, delimiter=' ')

with open(input_file_name) as url_input_file:
    url_input = csv.reader(url_input_file)
    for row in url_input:
        try:
            print(row[0])
        except: 
            continue
        output_csv.writerow([urlparse(row[0]).hostname, tldextract.extract(row[0]).suffix])


output_file.close()