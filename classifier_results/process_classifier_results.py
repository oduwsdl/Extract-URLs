import csv
import re
import sys
import os

base_dir = os.path.abspath(os.path.join(__file__, '../..'))
sys.path.append(f'{base_dir}')

from util import URLUtil

util = URLUtil()

# input_file = "test_arxiv_output.csv"
input_file = "Arxiv-Output.csv"
output_file = "parsed_" + input_file

revised_output_file = open("./classifier_results/" + output_file, "w")
revised_output_csv = csv.writer(revised_output_file, delimiter=',')
revised_output_csv.writerow(['Sentence', 'ValidURL', 'Class', 'File'])

with open('raw_data_outputs/classifier_results/' + input_file, newline='') as classifier_results_file:
    classifier_results = csv.reader(classifier_results_file, delimiter=',')

    prev_file_base = ""
    prev_data = []
    max_version = ""

    next(classifier_results)
    for row in classifier_results:
        sent = row[0]
        classification = row[1]
        file_name = row[2]

        try:
            parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0]
        except: 
            continue

        file_base = parsed_file[0]

        # From Lamia
        # regex = r'((http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?)'
        # m = re.findall(regex, sent)

        # Found online 
        regex2 = r'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
        m2 = re.findall(regex2, sent)
        if m2 != []:
            u = m2[0].rstrip('.')
            try:
                url = util.validate_url(u)
            except:
                url = ''

        if prev_file_base != file_base:
            if prev_file_base != "":
                revised_output_csv.writerow(prev_data)
            prev_file_base = file_base
            max_version = parsed_file[1]
        else:
            if int(max_version) < int(parsed_file[1]):
                max_version = parsed_file[1]
        prev_data = [sent, url, classification, file_name]

    revised_output_csv.writerow(prev_data)
        

revised_output_file.close()