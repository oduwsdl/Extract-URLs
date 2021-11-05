import concurrent.futures
import hashlib
import io
import json
import os

import flask
import requests

from extractor import Extractor
from util import APIUtil

dir_path = "/home/mklein/pdf/0704/"
for filename in os.listdir(dir_path):
    pdf_path = os.path.join(dir_path, filename)
    extractor = Extractor()
    urls = extractor.extract_all_urls(pdf_path)
    print(urls)