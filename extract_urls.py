import concurrent.futures
import hashlib
import io
import json
import os

import flask
import requests

from extractor import Extractor
from util import APIUtil

pdf_path = "/home/mklein/pdf/0704/0704.4003v9.pdf"
extractor = Extractor()
urls = extractor.extract_all_urls(pdf_path)
print(urls)