import json
import re

repo_file = open("./repo_results/repo_urls.json")
repo_json = json.load(repo_file)
repo_file.close()

cat_file = open("arxiv-categories.json")
cat_json = json.load(cat_file)
cat_file.close()

econ = [0, 0, 0, 0]
eess = [0, 0, 0, 0]
stat = [0, 0, 0, 0]
qufi = [0, 0, 0, 0]
qubi = [0, 0, 0, 0]
cs = [0, 0, 0, 0]
math = [0, 0, 0, 0]
phys = [0, 0, 0, 0]
cat_filler = [0, 0, 0, 0, 0, 0, 0, 0]
ghp_filler = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

econ_cats = 'econ'
eess_cats = 'eess'
stat_cats = 'stat'
qufi_cats = 'q-fin'
qubi_cats = 'q-bio'
cs_cats = 'cs'
math_cats = 'math'
phys_cats = ['astro-ph', 'cond-mat', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th', 'math-ph', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'quant-ph']

def add_matrix(a, file_name):
    try:
        a[0] = a[0] + repo_json[dir]["files"][file_name]['bitbucket']["url_count"]
    except: 
        pass
    try:
        a[1] = a[1] + repo_json[dir]["files"][file_name]['github']["url_count"]
    except:
        pass
    try:
        a[2] = a[2] + repo_json[dir]["files"][file_name]['gitlab']["url_count"]
    except:
        pass
    try:
        a[3] = a[3] + repo_json[dir]["files"][file_name]['sourceforge']["url_count"]
    except:
        pass
    
    return a

for dir in repo_json:
    for file_name in repo_json[dir]["files"]:
        parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0][0]
        try:
            cats = cat_json["ids"][parsed_file][0].split()
        except:
            pass
        primary_cat = cats[0]
        primary_prefix = primary_cat.split('.')[0]
        if primary_prefix == econ_cats:
            econ = add_matrix(econ, file_name)
        elif primary_prefix == eess_cats:
            eess = add_matrix(eess, file_name)
        elif primary_prefix == stat_cats:
            stat = add_matrix(stat, file_name)
        elif primary_prefix == qufi_cats:
            qufi = add_matrix(qufi, file_name)
        elif primary_prefix == qubi_cats:
            qubi = add_matrix(qubi, file_name)
        elif primary_prefix == cs_cats:
            cs = add_matrix(cs, file_name)
        elif primary_prefix == math_cats:
            math = add_matrix(math, file_name)
        elif primary_prefix in phys_cats:
            phys = add_matrix(phys, file_name)
        else:
            print(primary_prefix)

matrix = [econ, eess, stat, qufi, qubi, cs, math, phys]
print(matrix)
names = ["Economics", "Electrical Engineering and Systems Science", "Statistics", "Quantitative Finance", "Quantitative Biology", "Computer Science", "Mathematics", "Physics", "Bitbucket", "GitHub", "GitLab", "SourceForge"]
