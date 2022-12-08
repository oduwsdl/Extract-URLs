import jsonlines
import os
import re
import csv
import subprocess
import sys

auth_token = sys.argv[1]

gh_stats = {'incorrect_url': 0, 'correct_url': 0, 'missing_swh': 0, 'found_swh': 0}
gl_stats = {'incorrect_url': 0, 'correct_url': 0, 'missing_swh': 0, 'found_swh': 0}
bb_stats = {'incorrect_url': 0, 'correct_url': 0, 'missing_swh': 0, 'found_swh': 0}
sf_stats = {'incorrect_url': 0, 'correct_url': 0, 'missing_swh': 0, 'found_swh': 0}
rate_limit_remaining = '1'
rate_limit_reset = '0'

host = os.uname()[1]
if host == 'terra':
   input_file = 'part_dedupe_surt_1.jsonl'
   output_file = 'part_swh_results_1.csv'
elif host == 'wsdl-docker':
   input_file = 'part_dedupe_surt_2.jsonl'
   output_file = 'part_swh_results_2.csv'
elif host == 'wsdl-docker-private':
   input_file = 'part_dedupe_surt_3.jsonl'
   output_file = 'part_swh_results_3.csv'

swh_results_file = open("./data_processing/" + output_file, "w")
swh_results_csv = csv.writer(swh_results_file, delimiter=',')
# swh_results_csv.writerow(['SURT', 'URL', 'GHP', 'HeaderFile', 'ResponseFile', 'CorrectURL?', 'InSWH?'])


with jsonlines.open('data_processing/' + input_file, 'r') as jsonl_f:
   for line in jsonl_f:
      surt = str(line['surt'])
      url = str(line['info'][0]['url'])
      ghp = str(line['GHP'])

      if ghp == "GitHub":
         result = re.match(r'(http|https|git):\/\/(www.|)github.com\/([^\/]+)\/([^\/(\.)]+)', url)
         try: 
            repo_url = result[0]
            file = 'github-' + result[3] + '-' + result[4] + '.txt'
            output = subprocess.check_output('./swh_api_scrape.sh https://archive.softwareheritage.org/api/1/origin/' + repo_url + '/visits/ ' + rate_limit_reset + ' ' + rate_limit_remaining + ' swh_headers/' + file + ' swh_response/' + file + ' ' + auth_token, shell=True, text=True).strip().split()
            http_code = output[0]
            rate_limit_reset = output[1]
            rate_limit_remaining = output[2]
            gh_stats['correct_url'] += 1
            if  http_code == "200":
               swh_results_csv.writerow([surt, repo_url, ghp, 'swh_headers/' + file, 'swh_response/' + file, 'Yes', 'Yes'])
               gh_stats['found_swh'] += 1
            else:
               swh_results_csv.writerow([surt, repo_url, ghp, 'swh_headers/' + file, 'swh_response/' + file, 'Yes', 'No'])
               gh_stats['missing_swh'] += 1
         except: 
            swh_results_csv.writerow([surt, url, ghp, ' ', ' ', 'No', 'No'])
            gh_stats['incorrect_url'] += 1
      elif ghp == "GitLab":
         result = re.match(r'(http|https):\/\/(www.|)gitlab.com\/([^\/]+)\/([^\/(\.)]+)', url)
         try: 
            repo_url = result[0] + '.git'
            file = 'gitlab-' + result[3] + '-' + result[4] + '.txt'
            output = subprocess.check_output('./swh_api_scrape.sh https://archive.softwareheritage.org/api/1/origin/' + repo_url + '/visits/ ' + rate_limit_reset + ' ' + rate_limit_remaining + ' swh_headers/' + file + ' swh_response/' + file + ' ' + auth_token, shell=True, text=True).strip().split()
            http_code = output[0]
            rate_limit_reset = output[1]
            rate_limit_remaining = output[2]
            gl_stats['correct_url'] += 1
            if  http_code == "200":
               swh_results_csv.writerow([surt, repo_url, ghp, 'swh_headers/' + file, 'swh_response/' + file, 'Yes', 'Yes'])
               gl_stats['found_swh'] += 1
            else:
               swh_results_csv.writerow([surt, repo_url, ghp, 'swh_headers/' + file, 'swh_response/' + file, 'Yes', 'No'])
               gl_stats['missing_swh'] += 1
         except: 
            swh_results_csv.writerow([surt, url, ghp, ' ', ' ', 'No', 'No'])
            gl_stats['incorrect_url'] += 1
      elif ghp == "Bitbucket":
         result = re.match(r'(http|https):\/\/(www.|\w+@|)bitbucket.org\/([^\/]+)\/([^\/(\.)]+)', url)
         try: 
            repo_url = result[0]
            file = 'bitbucket-' + result[3] + '-' + result[4] + '.txt'
            output = subprocess.check_output('./swh_api_scrape.sh https://archive.softwareheritage.org/api/1/origin/' + repo_url + '/visits/ ' + rate_limit_reset + ' ' + rate_limit_remaining + ' swh_headers/' + file + ' swh_response/' + file + ' ' + auth_token, shell=True, text=True).strip().split()
            http_code = output[0]
            rate_limit_reset = output[1]
            rate_limit_remaining = output[2]
            bb_stats['correct_url'] += 1
            if  http_code == "200":
               swh_results_csv.writerow([surt, repo_url, ghp, 'swh_headers/' + file, 'swh_response/' + file, 'Yes', 'Yes'])
               bb_stats['found_swh'] += 1
            else:
               swh_results_csv.writerow([surt, repo_url, ghp, 'swh_headers/' + file, 'swh_response/' + file, 'Yes', 'No'])
               bb_stats['missing_swh'] += 1
         except: 
            swh_results_csv.writerow([surt, url, ghp, ' ', ' ', 'No', 'No'])
            bb_stats['incorrect_url'] += 1
      elif ghp == "SourceForge":
         result = re.match(r'(http|https):\/\/(www.|)sourceforge.net\/(projects|p)\/([^\/(\.)]+)', url)
         try: 
            repo = result[4]
            repo_url = r"https://svn.code.sf.net/p/" + repo + r"/code"
            file = 'sourceforge-' + repo + '.txt'
            output = subprocess.check_output('./swh_api_scrape.sh https://archive.softwareheritage.org/api/1/origin/' + repo_url + '/visits/ ' + rate_limit_reset + ' ' + rate_limit_remaining + ' swh_headers/' + file + ' swh_response/' + file + ' ' + auth_token, shell=True, text=True).strip().split()
            http_code = output[0]
            rate_limit_reset = output[1]
            rate_limit_remaining = output[2]
            sf_stats['correct_url'] += 1
            if  http_code == "200":
               swh_results_csv.writerow([surt, repo_url, ghp, 'swh_headers/' + file, 'swh_response/' + file, 'Yes', 'Yes'])
               sf_stats['found_swh'] += 1
            else:
               swh_results_csv.writerow([surt, repo_url, ghp, 'swh_headers/' + file, 'swh_response/' + file, 'Yes', 'No'])
               sf_stats['missing_swh'] += 1
         except:
            swh_results_csv.writerow([surt, url, ghp, ' ', ' ', 'No', 'No'])
            sf_stats['incorrect_url'] += 1

print(gh_stats)
print(gl_stats)
print(bb_stats)
print(sf_stats)