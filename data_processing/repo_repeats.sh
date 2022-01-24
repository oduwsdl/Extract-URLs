#!/bin/bash
cut -f1 -d, repo_results/github.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/github_count.csv
cut -f1 -d, repo_results/gitlab.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/gitlab_count.csv
cut -f1 -d, repo_results/bitbucket.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/bitbucket_count.csv
cut -f1 -d, repo_results/sourceforge.csv | sort | uniq -c | sed 's/  *//' | sort -k1 -n -o repo_results/sourceforge_count.csv