import csv
import os
import re

gh_sitemap = ['github.com/join\?', 'github.com/login', 'github.com/pricing$', 'github.com/pricing/.*' 'github.com/git-guides$', 'github.com/git-guides/.*', 'github.com/team$', 'github.com/team/.*', 'github.com/marketplace$', 'github.com/marketplace/.*', 'github.com/enterprise$', 'github.com/enterprise/.*', 'github.com/features$', 'github.com/features/.*', 'github.com/readme$', 'github.com/readme/.*', 'github.com/about$', 'github.com/about/.*', 'github.com/learn$', 'github.com/learn/.*']
gl_sitemap = ['gitlab.com/users/sign_in$', 'gitlab.com/users/sign_in/.*', 'gitlab.com/users/sign_up$', 'gitlab.com/users/sign_up/.*', 'gitlab.com/explore$', 'gitlab.com/explore/.*', 'gitlab.com/help$', 'gitlab.com/help/.*']
sf_sitemap = ['sourceforge.net/create$', 'sourceforge.net/create/.*', 'sourceforge.net/about$', 'sourceforge.net/about/.*', 'sourceforge.net/top$', 'sourceforge.net/top/.*', 'sourceforge.net/user/newsletters$', 'sourceforge.net/user/newsletters/.*', 'sourceforge.net/user/registration$', 'sourceforge.net/user/registation/.*', 'sourceforge.net/user/registration_business$', 'sourceforge.net/user/registration_business/.*', 'sourceforge.net/software/vendors$', 'sourceforge.net/software/vendors/.*', 'sourceforge.net/software/reviews$', 'sourceforge.net/software/reviews/.*', 'sourceforge.net/p/forge$', 'sourceforge.net/p/forge/.*', 'sourceforge.net/p/add_project$', 'sourceforge.net/p/add_project/.*', 'sourceforge.net/auth$', 'sourceforge.net/auth/.*', 'sourceforge.net/directory$', 'sourceforge.net/directory/.*', 'sourceforge.net/software/?', 'sourceforge.net/blog$', 'sourceforge.net/blog/.*', 'sourceforge.net/about$', 'sourceforge.net/about/.*']
bb_sitemap = ['bitbucket.org/product$', 'bitbucket.org/product/.*', 'bitbucket.org/blog$', 'bitbucket.org/blog/.*']
sitemaps = gh_sitemap + gl_sitemap + sf_sitemap + bb_sitemap

# with open("timemap_map.txt", "r") as f:
#     lines = f.readlines()
# with open("temp_timemap_map.txt", "w") as f:
#     for line in lines:
#         data = line.strip().split()
#         url = data[0]
#         timemap = data[2]
#         # if re.search(r"(?=("+"|https?:\/\/".join(sitemaps)+r"))", url) is not None:
#             # os.remove(timemap)
#         if re.search(r"(?=("+"|https?:\/\/".join(sitemaps)+r"))", url) is None:
#             f.write(line)

# with open("timemap_results.csv", "r") as f:
#     lines = f.readlines()
# with open("temp_timemap_results.csv", "w") as f:
#     for line in lines:
#         data = line.strip().split()
#         url = data[0]
#         timemap = data[2]
#         if re.search(r"(?=("+"|https?:\/\/".join(sitemaps)+r"))", url) is None:
#             f.write(line)

with open("timemap_results.csv", "r") as f:
    file = csv.DictReader(f, delimiter=' ')
    timemaps = []
    
    for col in file:
        timemaps.append(col['File'])
    
for filename in os.listdir('timemap/'):
    if "timemap/" + filename not in timemaps:
        os.remove("timemap/" + filename)