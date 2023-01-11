import csv
import json
from math import perm
import re
import os
from datetime import datetime
import time

has_timemap = 0
no_timemap = 0
total_internet_archive = 0
total_archive_it = 0
total_arquivo = 0
total_archive_today = 0
total_bibalex = 0
total_australia = 0
total_stanford = 0
total_loc = 0
total_iceland = 0
total_perma = 0
total_uk_archive = 0
total_banq = 0
total_not_categorized = 0

csv_file = open("./mementos/valid_mementos.csv", "w")
csvwriter = csv.writer(csv_file, delimiter=' ')
csvwriter.writerow(['URL', 'SURT', 'TimeMapAddr', 'TimeMap', 'Datetime', 'Archive', 'StatusCode'])

with open('timemap_results.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        if row[3] == "Yes":
            has_timemap = has_timemap + 1

            internet_archive = 0
            archive_it = 0
            arquivo = 0
            archive_today = 0
            bibalex = 0
            australia = 0
            stanford = 0
            loc = 0
            iceland = 0
            perma = 0
            uk_archive = 0
            banq = 0
            not_categorized = 0

            timemap = open(row[2])
            data = json.load(timemap)
            for item in data["mementos"]["list"]:
                uri = item["uri"]

                # if from Internet Archive
                if re.match(r"https:\/\/web.archive.org\/", uri) is not None and internet_archive == 0:
                    time.sleep(1)
                    output = os.popen("curl -s http://web.archive.org/cdx/search/cdx?url=" + data["original_uri"])
                    o = output.read()
                    output_items = o.strip().split('\n')
                    internet_archive = internet_archive + len(output_items)
                    for cdx in output_items:
                        c = cdx.split(' ')
                        try:
                            csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], c[1], uri, "Internet-Archive", c[4]])
                        except: 
                            print(uri)
                            print(c)
                # if from Archive-It
                elif re.match(r"https:\/\/wayback.archive-it.org", uri) is not None and archive_it == 0:
                    time.sleep(1)
                    output = os.popen("curl -s http://wayback.archive-it.org/all/timemap/cdx?url=" + data["original_uri"])
                    o = output.read()
                    output_items = o.strip().split('\n')
                    archive_it = archive_it + len(output_items)
                    for cdx in output_items:
                        c = cdx.split(' ')
                        csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], c[1], uri, "Archive-It", c[4]])
                # if from Portuguese Web Archive
                elif re.match(r"https:\/\/arquivo.pt", uri) is not None and arquivo == 0:
                    time.sleep(1)
                    output = os.popen("curl -s https://arquivo.pt/wayback/cdx\?url\=" + data["original_uri"] + "\&output\=text")
                    o = output.read()
                    output_items = o.strip().split('\n')
                    arquivo = arquivo + len(output_items)
                    for cdx in output_items:
                        c = cdx.split(' ')
                        csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], c[1], uri, "Portuguese-Web-Archive", c[4]])
                # if from Archive.today
                elif re.match(r"https?:\/\/archive.md", uri) is not None:
                    time.sleep(1)
                    archive_today = archive_today + 1
                    output = os.popen("curl -IL -w '%{http_code}' -s -o /dev/null " + uri)
                    o = output.read()
                    dt = re.findall(r"https?:\/\/archive.md\/(\d*)", uri)[0]
                    csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], dt, uri, 'Archive.today', o])
                # if from Bibliotheca Alexandrina Web Archive (http://web.archive.bibalex.org:80/web/20021128063619/http://mixmaster.sourceforge.net/)
                elif re.match(r"http:\/\/web.archive.bibalex.org", uri) is not None:
                    time.sleep(1)
                    bibalex = bibalex + 1
                    output = os.popen("curl -IL -w '%{http_code}' -s -o /dev/null " + uri)
                    o = output.read()
                    dt = re.findall(r"https?:\/\/web.archive.bibalex.org:80\/web\/(\d*)", uri)[0]
                    csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], dt, uri, 'Bibliotheca-Alexandria', o])
                # if from Australian Web Archive (https://web.archive.org.au/awa/20210827160844mp_/http://pandora.nla.gov.au/pan/188309/20210827-1823/github.com/about.html)
                elif re.match(r"https:\/\/web.archive.org.au", uri) is not None:
                    australia = australia + 1
                # if from Stanford Web Archive (https://swap.stanford.edu/20201010163111/https://github.com/cwein3/dropout-analytical)
                elif re.match(r"https:\/\/swap.stanford.edu", uri) is not None:
                    time.sleep(1)
                    stanford = stanford + 1
                    output = os.popen("curl -IL -w '%{http_code}' -s -o /dev/null " + uri)
                    o = output.read()
                    dt = re.findall(r"https?:\/\/swap.stanford.edu\/(\d*)", uri)[0]
                    csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], dt, uri, 'Stanford', o])
                # if from Library of Congress (https://webarchive.loc.gov/all/20200319040516/https://github.com/BayesForDays/coronada)
                elif re.match(r"https:\/\/webarchive.loc.gov", uri) is not None:
                    time.sleep(1)
                    loc = loc + 1
                    output = os.popen("curl -IL -w '%{http_code}' -s -o /dev/null " + uri)
                    o = output.read()
                    dt = re.findall(r"https?:\/\/webarchive.loc.gov\/all\/(\d*)", uri)[0]
                    csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], dt, uri, 'Library-of-Congress', o])
                # if from Icelandic Web Archive (http://wayback.vefsafn.is/wayback/20200321032152/https://github.com/datadista/datasets/tree/master/COVID%2019)
                elif re.match(r"http:\/\/wayback.vefsafn.is", uri) is not None:
                    time.sleep(1)
                    iceland = iceland + 1
                    output = os.popen("curl -IL -w '%{http_code}' -s -o /dev/null " + uri)
                    o = output.read()
                    dt = re.findall(r"https?:\/\/wayback.vefsafn.is\/wayback\/(\d*)", uri)[0]
                    csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], dt, uri, 'Icelandic-Web-Archive', o])
                # if from Perma Archive (https://perma.cc/S4YH-P9LJ)
                elif re.match(r"https:\/\/perma.cc", uri) is not None:
                    time.sleep(1)
                    perma = perma + 1
                    output = os.popen("curl -ILs " + uri)
                    o = output.read()
                    response_code = re.findall(r"HTTP\/.*(\d{3})", o)[-1]
                    date = re.findall(r"[Mm]emento-[Dd]atetime: (.*)", o)[0]
                    datetime_object = datetime.strptime(date,r"%a, %d %b %Y %H:%M:%S %Z")
                    memento_datetime = datetime_object.strftime(r"%Y%m%d%H%M%S")
                    csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], memento_datetime, uri, 'Perma', response_code])
                # if from UK Web Archive (https://www.webarchive.org.uk/wayback/archive/20160220122632mp_/http://github.com/janl/mustache.js)
                elif re.match(r"https:\/\/www.webarchive.org.uk", uri) is not None:
                    time.sleep(1)
                    uk_archive = uk_archive + 1
                    output = os.popen("curl -IL -w '%{http_code}' -s -o /dev/null " + uri)
                    o = output.read()
                    dt = re.findall(r"https?:\/\/www.webarchive.org.uk\/wayback\/archive\/(\d*)", uri)[0]
                    csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], dt, uri, 'UK-Web-Archive', o])
                # if from BAnQ (https://waext.banq.qc.ca/wayback/20181006134836/https://github.com/mrdoob/three.js)
                elif re.match(r"https:\/\/waext.banq.qc.ca", uri) is not None:
                    time.sleep(1)
                    banq = banq + 1
                    output = os.popen("curl -IL -w '%{http_code}' -s -o /dev/null " + uri)
                    o = output.read()
                    dt = re.findall(r"https?:\/\/waext.banq.qc.ca\/wayback\/(\d*)", uri)[0]
                    csvwriter.writerow([data["original_uri"], row[1], row[2], row[3], dt, uri, 'BAnQ', o])

            total_internet_archive = total_internet_archive + internet_archive
            total_archive_it = total_archive_it + archive_it
            total_arquivo = total_arquivo + arquivo
            total_archive_today = total_archive_today + archive_today
            total_bibalex = total_bibalex + bibalex
            total_australia = total_australia + australia
            total_stanford = total_stanford + stanford
            total_loc = total_loc + loc
            total_iceland = total_iceland + iceland
            total_perma = total_perma + perma
            total_uk_archive = total_uk_archive + uk_archive
            total_banq = total_banq + banq
            total_not_categorized = total_not_categorized + not_categorized

        else: 
            no_timemap = no_timemap + 1
            csvwriter.writerow([row[0], row[1], row[2], row[3], 'None', 'None', 'None'])

csv_file.close()

print("has_timemap: " + str(has_timemap))
print("no_timemap: " + str(no_timemap))
print("Internet Archive: " + str(total_internet_archive))
print("Archive.it: " + str(total_archive_it))
print("Portuguese Web Archive: " + str(total_arquivo))
print("Archive.today: " + str(total_archive_today))
print("Bibliotheca Alexandrina Web Archive: " + str(total_bibalex))
print("Australian Web Archive: " + str(total_australia))
print("Stanford Web Archive: " + str(total_stanford))
print("Library of Congress: " + str(total_loc))
print("Icelandic Web Archive: " + str(total_iceland))
print("Perma CC: " + str(total_perma))
print("UK Web Archive: " + str(total_uk_archive))
print("BAnQ: " + str(total_banq))
print("Not categorized: " + str(total_not_categorized))
 