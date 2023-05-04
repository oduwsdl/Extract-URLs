import json
import jsonlines
from xml.etree import ElementTree

filename = "raw_data_outputs/tamu_parsed/000000.json"
with open(filename, 'r', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line.rstrip('\n|\r'))
        pdf_file = list(d.keys())[0]
        metadata_file = "/home/emily/sarah-thesis/" + pdf_file.split('/')[0] + "/dublin_core.xml"

        tree = ElementTree.parse(metadata_file)
        root = tree.getroot()
        for child in root:
            if child.attrib['qualifier'] == 'created':
                created = child.text
                if len(created) == 7:
                    dir = created.replace('-', '')
                elif len(created) == 10:
                    dir = created.replace('-', '')[:6]
        print(pdf_file + " " + dir)

        output = open("raw_data_outputs/tamu_parsed/" + dir + ".json", "a")
        jsonl_writer = jsonlines.Writer(output)
        jsonl_writer.write(d)
        jsonl_writer.close()
        output.close()
