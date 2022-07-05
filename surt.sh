#!/bin/bash
python3 github_surt.py
sort -k2 repo_results/github_surt.csv > sort.csv
cat sort.csv > repo_results/github_surt.csv
python3 gitlab_surt.py
sort -k2 repo_results/gitlab_surt.csv > sort.csv
cat sort.csv > repo_results/gitlab_surt.csv
python3 sourceforge_surt.py
sort -k2 repo_results/sourceforge_surt.csv > sort.csv
cat sort.csv > repo_results/sourceforge_surt.csv
python3 bitbucket_surt.py
sort -k2 repo_results/bitbucket_surt.csv > sort.csv
cat sort.csv > repo_results/bitbucket_surt.csv
rm sort.csv