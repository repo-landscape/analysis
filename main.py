#!/usr/bin/env python
# -*- conding: utf-8

"""
filter gitlab repo metadata
"""

import pandas as pd
import flask
import sys
from antlr4 import ParseTreeWalker, CommonTokenStream, InputStream
from antlr4 import *
from antlr4.InputStream import InputStream
from pathlib import Path

# from GitConfLexer import GitConfLexer
# from GitConfParser import GitConfParser
# from GitConfListener import GitConfListener

KEY = 'glpat-xinShZakar9yrWvpYK2_'
URL = 'https://gitlab.com/api/v4/projects?visibility=private&per_page=300&private_token=' + KEY
OUTPUTFILE = Path('./output') / 'outputfile.json'

def main():
    filtermetadata = FilterMetadata()
    gittableapi = Gittableapi()
    gittableapi.app.run(host='0.0.0.0', port=5000)
    return 0

class FilterMetadata:
    df = pd.read_json(URL, orient='tight')[[
        'name',
        'id',
        'http_url_to_repo',
        'description',
        'name']]

    def __init__(self):
        df = pd.read_json(URL, orient='tight')[['description', 'name']]
        self.write(self.df)

    def read(self):
        pass
        return 0

    def write(self, df):
        df.to_json(OUTPUTFILE, orient='split')

class Gittableapi():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    def routes(self):
        @self.app.route('/', methods=['GET'])
        def home():
            return FilterMetadata.df

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        # input_stream = InputStream(sys.stdin.read())
        pass
    main()

