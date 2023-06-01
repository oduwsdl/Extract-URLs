#!/bin/bash
# cd ../raw_data_outputs/class_pmc_results/
# cat P* > PMC-Output.csv
# awk -F"," '{print $NF"|"$0}' PMC-Output.csv | sort -t"|" -k1 | awk -F"|" '{print $NF }' > temp.csv
# mv temp.csv PMC-Output.csv
# cd ../..
# python3 classifier_results/process_classifier_results.py pmc > classifier_results/invalid_output.csv
# cd classifier_results
# awk -F" " '{print $NF"|"$0}' parsed_PMC-Output.csv | sort -t"|" -k1 | awk -F"|" '{print $NF }' > temp.csv
# mv temp.csv parsed_PMC-Output.csv
# split -l 750000 -a 1 -d parsed_PMC-Output.csv parsed_PMC-Output_
# cd ..
# python3 classifier_results/classifier_results_json.py pmc > classifier_results/no_date.txt
# python3 classifier_results/fixing_jsonl.py
# python3 get_repo_urls.py
cd repo_results/
cat class_pmc_github.csv > class_pmc_ghp_urls.csv
cat class_pmc_gitlab.csv >> class_pmc_ghp_urls.csv
cat class_pmc_bitbucket.csv >> class_pmc_ghp_urls.csv
cat class_pmc_sourceforge.csv >> class_pmc_ghp_urls.csv
cd ..
python3 classifier_results/urls_per_file.py
# python3 get_hostname.py
# sort oads_non_ghp_hostnames.csv > sorted_oads_non_ghp_hostnames.csv
# uniq -c sorted_oads_non_ghp_hostnames.csv uniq_oads_non_ghp_hostnames.csv
# sort -k1n -t ' ' uniq_oads_non_ghp_hostnames.csv > count_oads_non_ghp_hostnames.csv