import json
import csv
import statistics as s

repo_file = open("./repo_results/all_repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

csv_file = open("pdf_stats.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['Directory', 'Category', 'Mean', 'Median', 'StDev', 'Cut1', 'Cut2', 'Cut3'])

for dir in repo_json:
    # sourceforge_count = repo_json[dir]["sourceforge"]["url_count"]
    # github_count = repo_json[dir]["github"]["url_count"]
    # gitlab_count = repo_json[dir]["gitlab"]["url_count"]
    # bitbucket_count = repo_json[dir]["bitbucket"]["url_count"]
    # total_sourceforge_count = total_sourceforge_count + sourceforge_count
    # total_github_count = total_github_count + github_count
    # total_gitlab_count = total_gitlab_count + gitlab_count
    # total_bitbucket_count = total_bitbucket_count + bitbucket_count
    dir_file = open("parsed/" + dir + ".json")
    dir_json = json.load(dir_file)
    dir_file.close()
    # dir_count = 0
    # file_count = 0
    sf = []
    gh = []
    gl = []
    bb = []
    for file in repo_json[dir]["files"]:
        sf.append(repo_json[dir]["files"][file]["sourceforge"]["url_count"])
        gh.append(repo_json[dir]["files"][file]["github"]["url_count"])
        gl.append(repo_json[dir]["files"][file]["gitlab"]["url_count"])
        bb.append(repo_json[dir]["files"][file]["bitbucket"]["url_count"])
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], "SourceForge", s.mean(sf), s.median(sf), s.stdev(sf)] + s.quantiles(sf, n=4))
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], "GitHub", s.mean(gh), s.median(gh), s.stdev(gh)] + s.quantiles(gh, n=4))
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], "GitLab", s.mean(gl), s.median(gl), s.stdev(gl)] + s.quantiles(gl, n=4))
    csvwriter.writerow(["20" + dir[0:2] + "-" + dir[2:], "Bitbucket", s.mean(bb), s.median(bb), s.stdev(bb)] + s.quantiles(bb, n=4))
csv_file.close()