from xml.etree import ElementTree
import csv
import datetime
import re
import jsonlines
import os
import fnmatch

from extractor import Extractor
from util import APIUtil

def extraction(pdf_path):
    extractor = Extractor()
    urls = extractor.extract_all_urls(pdf_path)
    return urls

done = set(line.strip() for line in open('completed_files.txt'))
completed = open("completed_files.txt", "a")

corpus_path = "/home/emily/sarah-thesis/"
path_contents = os.scandir(corpus_path)
for element in path_contents:
    if element.is_dir():
        metadata_file = corpus_path  + element.name + '/dublin_core.xml'
        dir_contents = os.listdir(corpus_path + element.name)
        for filename in fnmatch.filter(dir_contents,'*.pdf'):
            if 'license' not in filename.lower() and 'copyright' not in filename.lower() and 'permission' not in filename.lower() and ' ' not in filename.strip():
                pdf_file = element.name + '/' + filename

            if pdf_file not in done:
                completed.write(pdf_file + "\n")

            tree = ElementTree.parse(metadata_file)
            root = tree.getroot()

            dir = '000000'
            for child in root:
                if child.attrib['qualifier'] == 'created':
                    created = child.text
                    if len(created) == 7:
                        dir = created.replace('-', '')
                    elif len(created) == 10:
                        dir = created.replace('-', '')[:6]

            data = {}
            try:
                url_dict = extraction(corpus_path + pdf_file)
            except:
                print(pdf_file)
            data[pdf_file] = url_dict

            d = open("raw_data_outputs/tamu_jsonl/" + dir + ".json", "a")
            jsonl_writer = jsonlines.Writer(d)
            jsonl_writer.write(data)
            jsonl_writer.close()
            d.close()

path_contents.close()
completed.close()
