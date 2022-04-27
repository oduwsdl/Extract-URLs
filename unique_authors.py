import json
import csv

def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3

csv_file = open("./data_processing/shared_authors.csv", "w")
csvwriter = csv.writer(csv_file, delimiter='|')
csvwriter.writerow(['Surt', 'FilesSharingAuthors', 'SharedAuthors', 'TotalFiles'])

with open("data_processing/urls_and_authors.jsonl", 'r', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line.rstrip('\n|\r'))
        count = 0
        shared_auth_count = 1
        shared_auths = []
        for file in d['files']:
            authors = d['files'][file]
            if count == 0:
                count = 1
                prev_auths = authors
            else:
                count = count + 1
                i = intersection(authors, prev_auths)
                if len(i) != 0:
                    shared_auth_count = shared_auth_count + 1
                    for auth in i:
                        if auth not in shared_auths:
                            shared_auths.append(auth)
                for a in authors:
                    if a not in prev_auths:
                        prev_auths.append(a)
        csvwriter.writerow([d['surt'], shared_auth_count, shared_auths, count])
csv_file.close()
        
        

            
