from scipy.stats import mannwhitneyu
from cliffs_delta import cliffs_delta
import json

forks_in_swh_file = open('./github_api/forks_in_swh.json')
forks_in_swh = json.load(forks_in_swh_file)
forks_not_in_swh_file = open('./github_api/forks_not_in_swh.json')
forks_not_in_swh = json.load(forks_not_in_swh_file)

# mwu = mannwhitneyu(forks_not_in_swh, forks_in_swh, alternative="less", method="asymptotic")
mwu = mannwhitneyu(forks_not_in_swh, forks_in_swh)
d, res = cliffs_delta(forks_not_in_swh, forks_in_swh)
print("SWH Fork")
print(mwu)
print(d,res)

forks_in_ia_file = open('./github_api/forks_in_ia.json')
forks_in_ia = json.load(forks_in_ia_file)
forks_not_in_ia_file = open('./github_api/forks_not_in_ia.json')
forks_not_in_ia = json.load(forks_not_in_ia_file)

# mwu = mannwhitneyu(forks_not_in_ia, forks_in_ia, alternative="less", method="asymptotic")
mwu = mannwhitneyu(forks_not_in_ia, forks_in_ia)
d, res = cliffs_delta(forks_not_in_ia, forks_in_ia)
print("IA Fork")
print(mwu)
print(d,res)

stars_in_swh_file = open('./github_api/stars_in_swh.json')
stars_in_swh = json.load(stars_in_swh_file)
stars_not_in_swh_file = open('./github_api/stars_not_in_swh.json')
stars_not_in_swh = json.load(stars_not_in_swh_file)

# mwu = mannwhitneyu(stars_not_in_swh, stars_in_swh, alternative="less", method="asymptotic")
mwu = mannwhitneyu(stars_not_in_swh, stars_in_swh)
d, res = cliffs_delta(stars_not_in_swh, stars_in_swh)
print("SWH Stargazers")
print(mwu)
print(d,res)

stars_in_ia_file = open('./github_api/stars_in_ia.json')
stars_in_ia = json.load(stars_in_ia_file)
stars_not_in_ia_file = open('./github_api/stars_not_in_ia.json')
stars_not_in_ia = json.load(stars_not_in_ia_file)

# mwu = mannwhitneyu(stars_not_in_ia, stars_in_ia, alternative="less", method="asymptotic")
mwu = mannwhitneyu(stars_not_in_ia, stars_in_ia)
d, res = cliffs_delta(stars_not_in_ia, stars_in_ia)
print("IA Stargazers")
print(mwu)
print(d,res)

subs_in_swh_file = open('./github_api/subs_in_swh.json')
subs_in_swh = json.load(subs_in_swh_file)
subs_not_in_swh_file = open('./github_api/subs_not_in_swh.json')
subs_not_in_swh = json.load(subs_not_in_swh_file)

# mwu = mannwhitneyu(subs_not_in_swh, subs_in_swh, alternative="less", method="asymptotic")
mwu = mannwhitneyu(subs_not_in_swh, subs_in_swh)
d, res = cliffs_delta(subs_not_in_swh, subs_in_swh)
print("SWH Subscribers")
print(mwu)
print(d,res)

subs_in_ia_file = open('./github_api/subs_in_ia.json')
subs_in_ia = json.load(subs_in_ia_file)
subs_not_in_ia_file = open('./github_api/subs_not_in_ia.json')
subs_not_in_ia = json.load(subs_not_in_ia_file)

# mwu = mannwhitneyu(subs_not_in_ia, subs_in_ia, alternative="less", method="asymptotic")
mwu = mannwhitneyu(subs_not_in_ia, subs_in_ia)
d, res = cliffs_delta(subs_not_in_ia, subs_in_ia)
print("IA Subscribers")
print(mwu)
print(d,res)
