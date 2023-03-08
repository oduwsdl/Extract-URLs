import csv

input_file = "dedupe_swh_results.csv"
output_file = "missing_urls.csv"

missing_urls_file = open("./swh/" + output_file, "w")
missing_urls_csv = csv.writer(missing_urls_file, delimiter=',')

with open('swh/' + input_file, newline='') as swh_results_file:
    swh_results = csv.reader(swh_results_file, delimiter=',')
    next(swh_results)
    for row in swh_results:
        if row[5] == "Yes" and row[6] == "No":
            missing_urls_csv.writerow([row[1].lower()])

missing_urls_file.close()
