import jsonlines
import csv

# input_file = "test_surt.jsonl"
input_file = "dedupe_surt.jsonl"
output_file = "url_pub_dates.csv"

dates_file = open("./data_processing/" + output_file, "w")
dates_csv = csv.writer(dates_file, delimiter=' ')
dates_csv.writerow(['URL', 'EarliestPub'])

with jsonlines.open('data_processing/' + input_file, 'r') as jsonl_f:
   for line in jsonl_f:
      url = str(line['info'][0]['url']).lower()
      earliest = 300000
      for ref in line['info']:
         if int(ref['dir']) < earliest:
            earliest = int(ref['dir'])
      earliest_date = str(earliest)[0:4] + '-' + str(earliest)[4:6] + '-01'
      dates_csv.writerow([url, earliest_date])

dates_file.close()