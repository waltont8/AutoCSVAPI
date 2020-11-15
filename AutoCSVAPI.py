#!/usr/bin/env python3

import getopt
import sys
import csv
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import re
from urllib.parse import parse_qs, urlparse

IP = "127.0.0.1"
PORT = 8888

argv = sys.argv[1:]
 
opts, args = getopt.getopt(argv, 'x:y:')

if len(args) != 1:
    print("Usage is `AutoCSVAPI file.csv`")
    exit(-1)

fileName = args[0]

headers = []
rows = []

with open(fileName, newline='') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    try:
        headers = next(reader, None)
        for row in reader:
            rows.append(row)
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(fileName, reader.line_num, e))

def MakeHandlerClassFromArgv(rows):
    class CustomHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
             super(CustomHandler, self).__init__(*args, **kwargs)
             self.rows = rows       

        def do_GET(self):
            queries = parse_qs(urlparse(self.path).query, keep_blank_values=False)
            rowResult = rows
            for i, k in enumerate(queries.keys()):
                rowResult = [n for n in rowResult if n[i] in queries[k]]

            data = json.dumps(rowResult)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(data.encode('utf8'))
           
    return CustomHandler

HandlerClass = MakeHandlerClassFromArgv(rows)    
server = HTTPServer((IP, PORT), HandlerClass)
server.serve_forever()
