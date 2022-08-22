# Input: [pmc_]repo_urls.json
# Output: [pmc_]file_url_counts.csv (file name, URL count, category), [pmc_]ecdf_number.csv (URLCount, ecdf, category), and [pmc_]ccdf_number.csv (URLCount, cdf, category)
# Notes: 

import json
import csv
import re
from statsmodels.distributions.empirical_distribution import ECDF
import numpy as np

def CCDF(data, category):
    data_size=len(data)

    # Set bins edges
    data_set=sorted(set(data))
    bins=np.append(data_set, data_set[-1]+1)

    # Use the histogram function to bin the data
    counts, bin_edges = np.histogram(data, bins=bins, density=False)

    counts=counts.astype(float)/data_size

    # Find the cdf
    cdf = np.cumsum(counts)
    for i in range(len(cdf)):
        csvwriter3.writerow([bin_edges[i], cdf[i]*100, category])

corpora = ['pmc', 'arxiv']

for corpus in corpora:
    if corpus == "pmc":
        prefix = "pmc_"
    elif corpus == "arxiv":
        prefix = ""
    repo_file = open("./repo_results/" + prefix + "repo_urls.json")
    repo_json = json.load(repo_file)
    repo_file.close()

    csv_file = open("./data_processing/" + prefix + "file_url_counts.csv", "w")
    csvwriter = csv.writer(csv_file)
    csvwriter.writerow(['Filename', 'URLCount', 'Category', 'Year', 'Date'])

    csv_file2 = open("./data_processing/" + prefix + "ecdf_numbers.csv", "w")
    csvwriter2 = csv.writer(csv_file2)
    csvwriter2.writerow(['URLCount', 'ecdf', 'Category'])

    csv_file3 = open("./data_processing/" + prefix + "ccdf_numbers.csv", "w")
    csvwriter3 = csv.writer(csv_file3)
    csvwriter3.writerow(['URLCount', 'cdf', 'Category'])

    sf = []
    gh = []
    gl = []
    bb = []

    for dir in repo_json:
        year = dir[0:4]
        date = dir[0:4] + "-" + dir[4:]
        for file in repo_json[dir]["files"]:
            try:
                sourceforge_count = repo_json[dir]["files"][file]["sourceforge"]["url_count"]
                csvwriter.writerow([file, sourceforge_count, "SourceForge", year, date])
                sf.append(sourceforge_count)
            except:
                pass
            try:
                github_count = repo_json[dir]["files"][file]["github"]["url_count"]
                csvwriter.writerow([file, github_count, "GitHub", year, date])
                gh.append(github_count)
            except:
                pass
            try:
                gitlab_count = repo_json[dir]["files"][file]["gitlab"]["url_count"]
                csvwriter.writerow([file, gitlab_count, "GitLab", year, date])
                gl.append(gitlab_count)
            except:
                pass
            try:
                bitbucket_count = repo_json[dir]["files"][file]["bitbucket"]["url_count"]
                csvwriter.writerow([file, bitbucket_count, "Bitbucket", year, date])
                bb.append(bitbucket_count)
            except:
                pass

    sf_ecdf = ECDF(sf)
    gh_ecdf = ECDF(gh)
    gl_ecdf = ECDF(gl)
    bb_ecdf = ECDF(bb)

    CCDF(sf, "SourceForge")
    CCDF(gh, "GitHub")
    CCDF(gl, "GitLab")
    CCDF(bb, "Bitbucket")

    csvwriter2.writerow([0, 0, "SourceForge"])
    for i in range(len(sf_ecdf.x)):
        csvwriter2.writerow([sf_ecdf.x[i], sf_ecdf.y[i]*100, "SourceForge"])

    csvwriter2.writerow([0, 0, "GitHub"])
    for i in range(len(gh_ecdf.x)):
        csvwriter2.writerow([gh_ecdf.x[i], gh_ecdf.y[i]*100, "GitHub"])

    csvwriter2.writerow([0, 0, "GitLab"])
    for i in range(len(gl_ecdf.x)):
        csvwriter2.writerow([gl_ecdf.x[i], gl_ecdf.y[i]*100, "GitLab"])

    csvwriter2.writerow([0, 0, "Bitbucket"])
    for i in range(len(bb_ecdf.x)):
        csvwriter2.writerow([bb_ecdf.x[i], bb_ecdf.y[i]*100, "Bitbucket"])

    csv_file.close()
    csv_file2.close()
    csv_file3.close()