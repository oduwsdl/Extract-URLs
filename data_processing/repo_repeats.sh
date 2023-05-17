#!/bin/bash
cut -f1 -d ' ' repo_results/pmc_github.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/pmc_github_count.csv
cut -f1 -d ' ' repo_results/pmc_gitlab.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/pmc_gitlab_count.csv
cut -f1 -d ' ' repo_results/pmc_bitbucket.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/pmc_bitbucket_count.csv
cut -f1 -d ' ' repo_results/pmc_sourceforge.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/pmc_sourceforge_count.csv
cut -f1 -d ' ' repo_results/github.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/github_count.csv
cut -f1 -d ' ' repo_results/gitlab.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/gitlab_count.csv
cut -f1 -d ' ' repo_results/bitbucket.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/bitbucket_count.csv
cut -f1 -d ' ' repo_results/sourceforge.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/sourceforge_count.csv
cut -f1 -d ' ' repo_results/class_github.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/class_github_count.csv
cut -f1 -d ' ' repo_results/class_gitlab.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/class_gitlab_count.csv
cut -f1 -d ' ' repo_results/class_bitbucket.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/class_bitbucket_count.csv
cut -f1 -d ' ' repo_results/class_sourceforge.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/class_sourceforge_count.csv
cut -f1 -d ' ' repo_results/etd_github.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/etd_github_count.csv
cut -f1 -d ' ' repo_results/etd_gitlab.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/etd_gitlab_count.csv
cut -f1 -d ' ' repo_results/etd_bitbucket.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/etd_bitbucket_count.csv
cut -f1 -d ' ' repo_results/etd_sourceforge.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/etd_sourceforge_count.csv