# Input: all_repo_urls.json (JSON of all URLs and their URL counts for each repo)
# Output: pdf_stats.csv (CSV with mean, median, stdev, and quartiles for each category and directory)
# Notes: Calculates statistics including every PDF in the corpus

import json
import csv
import statistics as s

repo_file = open("./repo_results/all_repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

csv_file = open("pdf_stats.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['Directory', 'Category', 'Mean', 'Median', 'StDev', 'Cut1', 'Cut2', 'Cut3', 'Percentage'])

for dir in repo_json:
    dir_file = open("parsed/" + dir + ".json")
    dir_json = json.load(dir_file)
    dir_file.close()
    sf = []
    gh = []
    gl = []
    bb = []
    file_count = 0
    sf_count = 0
    gh_count = 0
    gl_count = 0
    bb_count = 0
    for file in repo_json[dir]["files"]:
        sf.append(repo_json[dir]["files"][file]["sourceforge"]["url_count"])
        gh.append(repo_json[dir]["files"][file]["github"]["url_count"])
        gl.append(repo_json[dir]["files"][file]["gitlab"]["url_count"])
        bb.append(repo_json[dir]["files"][file]["bitbucket"]["url_count"])
        if repo_json[dir]["files"][file]["sourceforge"]["url_count"] != 0:
            sf_count = sf_count + 1
        if repo_json[dir]["files"][file]["github"]["url_count"] != 0:
            gh_count = gh_count + 1
        if repo_json[dir]["files"][file]["gitlab"]["url_count"] != 0:
            gl_count = gl_count + 1
        if repo_json[dir]["files"][file]["bitbucket"]["url_count"] != 0:
            bb_count = bb_count + 1
        file_count = file_count + 1
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], "SourceForge", s.mean(sf), s.median(sf), s.pstdev(sf)] + s.quantiles(sf, n=4) + [sf_count/file_count])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], "GitHub", s.mean(gh), s.median(gh), s.pstdev(gh)] + s.quantiles(gh, n=4) + [gh_count/file_count])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], "GitLab", s.mean(gl), s.median(gl), s.pstdev(gl)] + s.quantiles(gl, n=4) + [gl_count/file_count])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], "Bitbucket", s.mean(bb), s.median(bb), s.pstdev(bb)] + s.quantiles(bb, n=4) + [bb_count/file_count])
csv_file.close()