import csv

import surt

github_surt = open("repo_results/github_surt.csv", "r")
github_surt_csv = csv.reader(github_surt, delimiter=' ')

total = 0
repo = 0
user = 0
tree = 0
blob = 0
wiki = 0
pull = 0
issues = 0
commit = 0
raw = 0
releases = 0
tags = 0
graphs = 0
# archive link automatically downloads a ZIP of the code
archive = 0
# blame points to detail on the contributer, modifications, and messages in a commit (https://arxiv.org/pdf/2107.04712v2.pdf)
blame = 0
stats = 0
stats_urls = ["stargazers", "watchers", "pulls", "projects", "network", "pulse"]
discussions = 0
compare = 0
search = 0
actions = 0
branches = 0
other = 0

for row in github_surt_csv:
    surt_pieces = row[1].split('/')
    total = total + 1
    if len(surt_pieces) == 2:
        user = user + 1
    elif len(surt_pieces) == 3:
        repo = repo + 1
    else:
        if surt_pieces[3] == "tree":
            tree = tree + 1
        elif surt_pieces[3] == "blob":
            blob = blob + 1
        elif surt_pieces[3] == "wiki":
            wiki = wiki + 1
        elif surt_pieces[3] == "pull":
            pull = pull + 1
        elif "issues" in surt_pieces[3]:
            issues = issues + 1
        elif "commit" in surt_pieces[3]:
            commit = commit + 1
        elif surt_pieces[3] == "raw":
            raw = raw + 1
        elif surt_pieces[3] == "release" or surt_pieces[3] == "releases":
            releases = releases + 1
        elif surt_pieces[3] == "graphs":
            graphs = graphs + 1
        elif surt_pieces[3] == "archive":
            archive = archive + 1
        elif surt_pieces[3] == "blame":
            blame = blame + 1
        elif surt_pieces[3] in stats_urls:
            stats = stats + 1
        elif surt_pieces[3] == "discussions":
            discussions = discussions + 1
        elif surt_pieces[3] == "compare":
            compare = compare + 1
        elif "search?" in surt_pieces[3]:
            search = search + 1
        elif surt_pieces[3] == "tags":
            tags = tags + 1
        elif surt_pieces[3] == "actions":
            actions = actions + 1
        elif surt_pieces[3] == "branches":
            branches = branches + 1
        else:
            other = other + 1

print("Total: " + str(total))
print("User: " + str(user))
print("Repo: " + str(repo))
# print("Tree: " + str(tree))
# print("Blob: " + str(blob))
# print("Wiki: " + str(wiki))
# print("Pull: " + str(pull))
# print("Issues: " + str(issues))
print("Commit: " + str(commit))
# print("Raw: " + str(raw))
# print("Releases: " + str(releases))
# print("Graphs: " + str(graphs))
# print("Archive: " + str(archive))
# print("Blame: " + str(blame))
# print("Stats: " + str(stats))
# print("Discussions: " + str(discussions))
# print("Compare: " + str(compare))
# print("Search: " + str(search))
# print("Tags: " + str(tags))
# print("Actions: " + str(actions))
# print("Branches: " + str(branches))
print("Unique to GH: " + str(user + tree + blob + wiki + pull + issues + raw + releases + graphs + archive + blame + stats + discussions + compare + search + tags + actions))
print("Other: " + str(other))