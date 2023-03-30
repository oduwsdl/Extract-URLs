#!/bin/bash
cd ../raw_data_outputs/oads_output/
cat A* > part1_Arxiv-Output.csv
awk -F"," '{print $NF"|"$0}' part1_Arxiv-Output.csv | sort -t"|" -k1 | awk -F"|" '{print $NF }' > temp.csv
mv temp.csv part1_Arxiv-Output.csv
cd ../oads_output2/
cat A* > part2_Arxiv-Output.csv
awk -F"," '{print $NF"|"$0}' part2_Arxiv-Output.csv | sort -t"|" -k1 | awk -F"|" '{print $NF }' > temp.csv
mv temp.csv part2_Arxiv-Output.csv
cd ../..
python3 classifier_results/process_classifier_results.py > classifier_results/invalid_output.csv
cat classifier_results/parsed_part* > classifier_results/parsed_Arxiv-Output.csv
rm classifier_results/parsed_part*
cd classifier_results
awk -F"," '{print $NF"|"$0}' parsed_Arxiv-Output.csv | sort -t"|" -k1 | awk -F"|" '{print $NF }' > temp.csv
mv temp.csv parsed_Arxiv-Output.csv
cd ..
python3 classifier_results/classifier_results_json.py