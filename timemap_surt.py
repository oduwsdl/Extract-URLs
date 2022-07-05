import csv
import jsonlines
import subprocess

with jsonlines.open('data_processing/dedupe_surt.jsonl', 'r') as jsonl_f:
     for line in jsonl_f:
        url = str(line['info'][0]['url'])
        surt = str(line['surt'])
        subprocess.check_call(["./timemap_surt.sh", url, surt, 'skip'])

timemap_results = open("timemap_results.csv", "w")
timemap_results_csv = csv.writer(timemap_results, delimiter=' ')
timemap_results_csv.writerow(['File', 'SURT', 'URL', 'TimeMap(Yes/No)', 'Error(Yes/No)'])

before_has_timemap = 0
after_has_timemap = 0
before_no_timemap = 0
after_no_timemap = 0
before_html = 0
after_html = 0
before_bad_gateway = 0
after_bad_gateway = 0
before_other = 0
after_other = 0

def check_timemap(file_name, rerun):
    infile = open(file_name, 'r')
    first_line = infile.readline().strip()
    if first_line == "{":
        if rerun:
            global after_has_timemap
            after_has_timemap = after_has_timemap + 1
        else:
            global before_has_timemap
            before_has_timemap = before_has_timemap + 1
        status = "TimeMap"
    elif first_line == "404 page not found":
        if rerun:
            global after_no_timemap
            after_no_timemap = after_no_timemap + 1
        else:
            global before_no_timemap
            before_no_timemap = before_no_timemap + 1
        status = "No TimeMap"
    elif first_line == "<html>":
        if rerun:
            global after_html
            after_html = after_html + 1
            status = "Error"
        else:
            global before_html
            before_html = before_html + 1
            # status = "rerun"
            status = "Error"
    elif first_line == "Bad Gateway":
        if rerun:
            global after_bad_gateway
            after_bad_gateway = after_bad_gateway + 1
            status = "Error"
        else:
            global before_bad_gateway
            before_bad_gateway = before_bad_gateway + 1
            # status = "rerun"
            status = "Error"
    else:
        if rerun:
            global after_other
            after_other = after_other + 1
            status = "Error"
        else:
            global before_other
            before_other = before_other + 1
            # status = "rerun"
            status = "Error"
    return status

with open('timemap_map.txt', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        status = check_timemap(row[2], False)
        if status == "rerun":
            subprocess.check_call(["./timemap_surt.sh", row[0], row[1]])
            status = check_timemap(row[2], True)

        if status == "TimeMap":
            timemap_results_csv.writerow([row[0], row[1], row[2], 'Yes', 'No'])
        elif status == "No TimeMap":
            timemap_results_csv.writerow([row[0], row[1], row[2], 'No', 'No'])
        elif status == "Error":
            timemap_results_csv.writerow([row[0], row[1], row[2], 'No', 'Yes'])

print("Initial has timemap: " + str(before_has_timemap))
print("Initial no timemap: " + str(before_no_timemap))
print("Initial <html>: " + str(before_html))
print("Initial Bad Gateway: " + str(before_bad_gateway))
print("Initial other error: " + str(before_other))
print("Rerun has timemap: " + str(after_has_timemap))
print("rerun no timemap: " + str(after_no_timemap))
print("Rerun <html>: " + str(after_html))
print("Rerun Bad Gateway: " + str(after_bad_gateway))
print("Rerun other error: " + str(after_other))
timemap_results.close()            