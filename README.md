# Extract-URLs

This project is currently set up to extract URLs from PDf publications in the arXiv corpus and run numerous data analysis programs to understand the use of URLs in the arXiv corpus.

## Order of Programs

Some of the programs/scripts require the files from other programs/scripts. The correct order is shown below: 

* extract_urls.py (creates a JSON file of extracted URLs for each directory)
* get_repo_urls.py (creates repo_urls.json (only files with a repo URL) and all_file_urls.json (all files))
* data_processing/repo_repeats.sh (outputs the frequency of each URL for each repo)
* data_processing/dir_urls.py (aggregates the number of URLs per month per repo and creates dir_urls.csv and file_count.csv)
* data_processing/file_url_counts.py (creates file_url_counts.csv, ecdf_numbers.csv, and ccdf_numbers.csv)
* data_processing/url_freq.sh (creates URL_frequency.csv)
* data_processing/multiple_repos.sh (finds files that contain URLs to more than 1 repo and creates multiple_repos.csv)
* data_processing/multiple_repos_table.py (creates a table of the file and which repos it links to)
* data_processing/pdf_stats.py (calculates mean, median, and quartiles for the number of repo URLs in a PDF and creates pdf_stats.csv)
* data_processing/repo_url_counts.py (creates repo_url_counts.csv which contains the URL count for each directory and repo)
* data_processing/urls_per_file.py (creates urls_per_file.csv which contains the average number of URLs per mopnth for each repo)
