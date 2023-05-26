#!/bin/bash
PREFIX="class"
python3 get_repo_urls.py
sort -o repo_results/temp_${PREFIX}_github_surt.csv repo_results/${PREFIX}_github_surt.csv
mv repo_results/temp_${PREFIX}_github_surt.csv repo_results/${PREFIX}_github_surt.csv 
sort -o repo_results/temp_${PREFIX}_gitlab_surt.csv repo_results/${PREFIX}_gitlab_surt.csv
mv repo_results/temp_${PREFIX}_gitlab_surt.csv repo_results/${PREFIX}_gitlab_surt.csv 
sort -o repo_results/temp_${PREFIX}_sourceforge_surt.csv repo_results/${PREFIX}_sourceforge_surt.csv
mv repo_results/temp_${PREFIX}_sourceforge_surt.csv repo_results/${PREFIX}_sourceforge_surt.csv 
sort -o repo_results/temp_${PREFIX}_bitbucket_surt.csv repo_results/${PREFIX}_bitbucket_surt.csv
mv repo_results/temp_${PREFIX}_bitbucket_surt.csv repo_results/${PREFIX}_bitbucket_surt.csv
python3 ./data_processing/dir_urls.py
python3 ./data_processing/file_url_counts.py
./data_processing/url_freq.sh
./data_processing/multiple_repos.sh
python3 ./data_processing/multiple_repos_table.py
python3 ./data_processing/repo_url_counts.py
python3 ./data_processing/urls_per_file.py
python3 ./data_processing/pdf_stats.py
./data_processing/repo_repeats.sh
# python3 ./data_cleaning/dedupe_surts.py
# python3 timemap_surt.py