import json

cat_file = open("arxiv-categories.json", "w")
data = {"ids":{}}

"""
Read list of objects from a JSON lines file.
"""
with open("/arxiv_data/arxiv-metadata-oai.json", 'r', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line.rstrip('\n|\r'))
        data["ids"][d["id"]] = d["categories"]
        print(d["id"])
    
json.dump(data, cat_file)
cat_file.close()
