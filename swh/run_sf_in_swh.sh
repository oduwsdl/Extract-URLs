#!/bin/bash

python3 swh/get_sf_projects.py
cat swh/sf_projects.csv | (sed -u 1q; sort -k1 -t ' ' -o swh/sorted_sf_projects.csv)
python3 swh/get_sf_api_output.py
python3 swh/get_sf_repo_uris.py
python3 swh/check_sf_swh.py
