import csv
import json
from datetime import datetime

input_file = "timemap_results.csv"
output_file = "data_processing/url_timemap_dates.csv"

dates_file = open(output_file, 'w')
dates_csv = csv.writer(dates_file, delimiter=',')
dates_csv.writerow(['URL', 'EarliestVisit', 'LatestVisit', 'Average', 'NumVisits', 'MinDays', 'MaxDays'])

with open(input_file, newline='') as timemap_results_file:
    timemap_results = csv.reader(timemap_results_file, delimiter=' ')
    next(timemap_results)
    for row in timemap_results:
        url = row[0].lower()
        timemap = row[3]
        if timemap == "Yes":
            timemap_file = row[2]
            earliest = ""
            latest = ""
            average = ""
            sum_days = 0
            min_days = ""
            max_days = ""
            num_visits = 0
            prev_visit = ""
            curr_visit = ""
            f = open(timemap_file)
            data = json.load(f)
            for l in data['mementos']['list']:
                num_visits += 1
                curr_visit = datetime.strptime(l['datetime'][0:10], '%Y-%m-%d')
                if num_visits > 1:
                    delta = curr_visit - prev_visit
                    days = delta.days
                    sum_days += days
                    if min_days == "":
                        min_days = days
                    elif days < min_days:
                        min_days = days
                    if max_days == "":
                        max_days = days
                    elif days > max_days:
                        max_days = days
                prev_visit = curr_visit
            earliest = data['mementos']['first']['datetime'][0:10]
            latest = data['mementos']['last']['datetime'][0:10]
            if num_visits > 1:
                average = sum_days / (num_visits - 1)
            dates_csv.writerow([url, earliest, latest, average, num_visits, min_days, max_days])
            f.close()
dates_file.close()