import jsonlines
import os
import re
import csv
import subprocess
import sys

# input_file = "data_processing/dedupe_swh_results.csv"
# output_file = "swh_curl_map.csv"

# host = os.uname()[1]
# host = 'test'
host = "sf"
if host == 'terra':
	input_file = 'part_dedupe_surt_0.jsonl'
	output_file = 'swh_curl_map_0.csv'
elif host == 'wsdl-docker':
    input_file = 'part_dedupe_surt_1.jsonl'
    output_file = 'swh_curl_map_1.csv'
elif host == 'wsdl-docker-private':
    input_file = 'part_dedupe_surt_2.jsonl'
    output_file = 'swh_curl_map_2.csv'
elif host == "test":
    input_file = 'test_surt.jsonl'
    output_file = "test_curl_map.csv"   
elif host == 'sf':
	input_file = 'sf_surt.jsonl'
	output_file = 'sf_curl_map.csv'

curl_results_file = open("./data_processing/" + output_file, "a")
curl_results_csv = csv.writer(curl_results_file, delimiter=',')
# curl_results_csv.writerow(['URL', 'GHP', 'RepoURL', 'File'])

with jsonlines.open('data_processing/' + input_file, 'r') as jsonl_f:
	for line in jsonl_f:
		url = str(line['info'][0]['url']).lower()
		ghp = str(line['GHP'])

		if ghp == "GitHub":
			result = re.match(r'(http|https|git):\/\/(www.|)github.com\/([^\/]+)\/([^\/(\.)][a-zA-Z0-9-_]+)', url)
			if result != None and result != "":
				repo_url = result[0]
			else:
				repo_url = ' '
			whole_url = re.match(r'(http|https|git):\/\/(www.|)github.com\/(.*)', url)
			file = 'swh_curl/github' + '-'.join(whole_url[3].split('/')) + '.txt'
			os.system('./curl_url.sh ' + url + ' ' + file)
			curl_results_csv.writerow([url, ghp, repo_url, file])
		elif ghp == "GitLab":
			result = re.match(r'(http|https):\/\/(www.|)gitlab.com\/([^\/]+)\/([^\/(\.)][a-zA-Z0-9-_]+)', url)
			if result != None and result != "":
				repo_url = result[0] + '.git'
			else: 
				repo_url = ' '
			whole_url = re.match(r'(http|https):\/\/(www.|)gitlab.com\/(.*)', url)
			file = 'swh_curl/gitlab' + '-'.join(whole_url[3].split('/')) + '.txt'
			os.system('./curl_url.sh ' + url + ' ' + file)
			curl_results_csv.writerow([url, ghp, repo_url, file])
		elif ghp == "Bitbucket":
			result = re.match(r'(http|https):\/\/(www.|\w+@|)bitbucket.org\/([^\/]+)\/([^\/(\.)][a-zA-Z0-9-_]+)', url)
			if result != None and result != "": 
				repo_url = result[0]
			else: 
				repo_url = ' '
			whole_url = re.match(r'(http|https):\/\/(www.|\w+@|)bitbucket.org\/(.*)', url)
			file = 'swh_curl/bitbucket' + '-'.join(whole_url[3].split('/')) + '.txt'
			os.system('./curl_url.sh ' + url + ' ' + file)
			curl_results_csv.writerow([url, ghp, repo_url, file])
		elif ghp == "SourceForge":
			result = re.match(r'(http|https):\/\/(www.|)sourceforge.net\/(projects|p)\/([^\/(\.)][a-zA-Z0-9-_]+)', url)
			if result != None and result != "": 
				repo = result[4]
				repo_url = r"https://svn.code.sf.net/p/" + repo + r"/code"
			else:
				repo_url = ' '
			# Check if URL type is sourceforge.net/p/project_name or sourceforge.net/project/project_name
			url_1 = re.match(r'(http|https):\/\/(www.|)sourceforge.net\/(projects|p)\/([^\/(\.)][a-zA-Z0-9\-_]+)', url)
			if url_1 != None and url_1 != "":
				file = 'swh_curl/sourceforge' + '-'.join(url_1[4].split('/')) + '.txt'
			else:
				# Check if URL type is project_name.sourceforge.net/extra
				url_2 = re.match(r'(http|https):\/\/([a-zA-Z0-9\-_]+).sourceforge.net\/?(.*)', url)
				if url_2 != None and url_2 != "":
					prefix = url_2[2]
					suffix = url_2[3]
					if suffix != "":
						file = 'swh_curl/sourceforge-' + prefix + '-' + '-'.join(suffix.split('/')) + '.txt'
					else:
						file = 'swh_curl/sourceforge-' + prefix + '.txt'
				else:
					url_3 = re.match(r'(http|https):\/\/www.([a-zA-Z0-9\-_]+).sourceforge.net\/?(.*)', url)
					# Check if URL type is www.project_name.sourceforge.net/extra
					if url_3 != None and url_3 != "":
						prefix = url_3[2]
						suffix = url_3[3]
						if suffix != "":
							file = 'swh_curl/sourceforge-' + prefix + '-' + '-'.join(suffix.split('/')) + '.txt'
						else:
							file = 'swh_curl/sourceforge-' + prefix + '.txt'
					else:
						url_4 = re.match(r'(http|https):\/\/(www.|)sourceforge.net\/([^\/(\.)][a-zA-Z0-9\-_]+)', url)
						if url_4 != None and url_4 != "":
							file = 'swh_curl/sourceforge-' + '-'.join(url_4[3].split('/')) + '.txt'
			os.system('./curl_url.sh ' + url + ' ' + file)
			curl_results_csv.writerow([url, ghp, repo_url, file])

curl_results_file.close()

