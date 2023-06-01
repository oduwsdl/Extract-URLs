import csv
import re
import sys
import os
from surt import surt

base_dir = os.path.abspath(os.path.join(__file__, '../..'))
sys.path.append(f'{base_dir}')

from util import URLUtil

util = URLUtil()

# input_file = "test_arxiv_output.csv"

corpus = sys.argv[1]

if corpus == "arxiv":
    input_files = ["oads_output/part1_Arxiv-Output.csv", "oads_output2/part2_Arxiv-Output.csv", "oads_dataset3/part3_Arxiv-Output.csv"]
    file_pattern = r"(\d{4}.\d*)v(\d*).pdf"
elif corpus == "pmc":
    input_files = ["class_pmc_results/PMC-Output.csv"]
    # input_files = ["class_pmc_results/a_test_PMC-Output.csv"]
    file_pattern = r"\/arxiv_data1\/(oa_pdf.*\.pdf)"

for input in input_files:
    output_file = "parsed_" + os.path.basename(input)

    revised_output_file = open("./classifier_results/" + output_file, "w")
    revised_output_csv = csv.writer(revised_output_file, delimiter=' ')
    # revised_output_csv.writerow(['Sentence', 'ValidURL', 'Class', 'File'])

    with open('raw_data_outputs/' + input, newline='') as classifier_results_file:
        classifier_results = csv.reader(classifier_results_file, delimiter=',')

        prev_file_base = ""
        prev_file_name = ""
        prev_data = []
        max_version = ""

        for row in classifier_results:
            try:
                sent = row[0]
                classification = row[-2]
                file_name = row[-1]
                parsed_file = re.findall(file_pattern, file_name)[0]
            except: 
                print(row)
                continue

            if corpus == "arxiv":
                file_base = parsed_file[0]
            elif corpus == "pmc":
                file_name = parsed_file
                file_base = parsed_file

            # From Lamia
            # regex = r'((http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?)'
            # m = re.findall(regex, sent)

            # Found online 
            regex2 = r'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/=]*)'
            m2 = re.findall(regex2, sent)
            if m2 != []:
                u = m2[0].rstrip('.')
                try:
                    url = util.validate_url(u).lower()
                    s = surt(url)
                except:
                    continue

            if prev_file_name == "":
                # add current info to rows
                # prev_data.append([sent, url, classification, file_name])
                prev_data.append([url, s, classification, file_name])
                # set prev_file to file
                prev_file_name = file_name
                # set prev_base to filebase
                prev_file_base = file_base
            elif prev_file_name != file_name:
                if prev_file_base != file_base:
                    # write rows to file
                    revised_output_csv.writerows(prev_data)
                    # reset rows
                    prev_data.clear()
                    # add current info to rows
                    # prev_data.append([sent, url, classification, file_name])
                    prev_data.append([url, s, classification, file_name])
                    # set prev_file to file
                    prev_file_name = file_name
                    # set prev_base to filebase
                    prev_file_base = file_base
                else:
                    # reset rows
                    prev_data.clear()
                    # add current info to rows
                    # prev_data.append([sent, url, classification, file_name])
                    prev_data.append([url, s, classification, file_name])
                    # set prev_file to file
                    prev_file_name = file_name
            else:
                # add current info to rows
                # prev_data.append([sent, url, classification, file_name])
                prev_data.append([url, s, classification, file_name])
            
            # if prev_file_base != file_base:
            #     if prev_file_base != "":
            #         revised_output_csv.writerow(prev_data)
            #     prev_file_base = file_base
            #     max_version = parsed_file[1]
            # else:
            #     if int(max_version) < int(parsed_file[1]):
            #         max_version = parsed_file[1]
            # prev_data = [sent, url, classification, file_name]

        revised_output_csv.writerows(prev_data)
            

    revised_output_file.close()