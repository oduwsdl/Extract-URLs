# Input: 
# Output: 
# Notes: 

import csv
from statsmodels.distributions.empirical_distribution import ECDF
import numpy as np

def CCDF(data):
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
        csvwriter2.writerow([bin_edges[i], cdf[i]*100])

input_file_name = "count_oads_non_ghp_hostnames.csv"
counts = []
with open(input_file_name) as input_file:
    hostname_input = csv.reader(input_file, delimiter=' ')
    next(hostname_input)
    for row in hostname_input:
        counts.append(int(row[0]))

csv_file = open("hostname_ecdf_numbers.csv", "w")
csvwriter = csv.writer(csv_file)
csvwriter.writerow(['URLCount', 'ecdf'])

csv_file2 = open("hostname_ccdf_numbers.csv", "w")
csvwriter2 = csv.writer(csv_file2)
csvwriter2.writerow(['URLCount', 'cdf'])

count_ecdf = ECDF(counts)
print(count_ecdf)

CCDF(counts)

csvwriter.writerow([0, 0])
for i in range(len(count_ecdf.x)):
    csvwriter.writerow([count_ecdf.x[i], count_ecdf.y[i]*100])

csv_file.close()
csv_file2.close()