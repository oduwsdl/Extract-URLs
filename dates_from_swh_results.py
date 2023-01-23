import os
import csv
import re
import ast
import jsonlines
from datetime import datetime

input_file = "dedupe_swh_results.csv"
output_file = "url_swh_dates.csv"

dates_file = open("./data_processing/" + output_file, "w")
dates_csv = csv.writer(dates_file, delimiter=',')
dates_csv.writerow(['URL', 'EarliestVisit', 'Average', 'NumVisits', 'MinDays', 'MaxDays'])

with open('data_processing/' + input_file, newline='') as swh_results_file:
    swh_results = csv.reader(swh_results_file, delimiter=',')
    next(swh_results)
    for row in swh_results:
        url = row[1].lower()
        in_swh = row[6]
        if in_swh == "Yes":
            response_file = row[4]
            earliest = ""
            average = ""
            sum_days = 0
            min_days = ""
            max_days = ""
            num_visits = 0
            prev_visit = ""
            curr_visit = ""
            with jsonlines.open(response_file, 'r') as jsonl_f:
                for line in jsonl_f:
                    try:
                        e = line['exception']
                        print(url)
                        break
                    except:
                        for l in line:
                            num_visits += 1
                            d = l['date']
                            curr_visit = datetime.strptime(d[0:10], '%Y-%m-%d')
                            if num_visits > 1:
                                delta = prev_visit - curr_visit
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
                            else:
                                prev_visit = curr_visit
                earliest = str(curr_visit)[0:10]
                if num_visits > 1:
                    average = sum_days / (num_visits - 1)
            dates_csv.writerow([url, earliest, average, num_visits, min_days, max_days])
                