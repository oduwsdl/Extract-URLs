#!/bin/bash
sort swh_curl_map_0.csv | uniq -i > dedupe_curl_map.csv
sort swh_curl_map_1.csv | uniq -i >> dedupe_curl_map.csv
sort swh_curl_map_2.csv | uniq -i >> dedupe_curl_map.csv
sort sf_curl_map.csv | uniq -i >> dedupe_curl_map.csv 
